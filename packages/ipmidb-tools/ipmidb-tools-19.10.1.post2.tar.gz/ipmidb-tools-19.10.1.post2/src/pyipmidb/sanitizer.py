"""Tool for IPMIDB sanitization"""

import re
from logging import DEBUG, ERROR, INFO, Formatter, StreamHandler, getLogger
from ConfigParser import SafeConfigParser
from socket import gethostbyname, gaierror
from subprocess import Popen, PIPE
from urllib3.request import urlencode

from ironicclient import client as ironic_client
from keystoneauth1.extras.kerberos import MappedKerberos as auth_k
from keystoneauth1 import session as keystone_session
from aitools.foreman import ForemanClient
from aitools.errors import AiToolsForemanError

from helpers import read_config_file
from pyipmidb.client import IPMIDBClient, IPMIDBError
from infoream.client import InforEamClient
from pylandb import LanDB


class IPMIDBSanitizerError(Exception):
    """Generic IPMIDB Sanitizer error"""
    pass


class IPMIDBSanitizer(object):
    """Tool for IPMIDB sanitization"""
    LOGGER_NAME = 'ipmidb-sanitizer'

    def __init__(self, endpoint='ipmidb.cern.ch', debug=False,
                 config_file='/etc/ipmidb-tools/config.json'):
        # Start logging
        if debug:
            loglevel = DEBUG
        else:
            loglevel = ERROR
        self.logger = self._get_logger(loglevel)
        self.config_file = config_file
        # Create IPMIDB, LanDB, Ironic, InforEAM and Foreman objects
        self.ipmidb = IPMIDBClient(debug=False, endpoint=endpoint)
        self.landb = LanDB(debug=False)
        self.landb_service = self.landb.get_service()
        self.ironic = self._get_ironic_client()
        self.infoream = self._get_infoream_client()
        self.foreman = self._get_foreman_client()

        # Get factorized LanDB Search object
        self.devicesearch = self.landb.get_factory('types:DeviceSearch')

        # Initialise Ironic UUID to host rainbow table
        self.ironic_uuid_map = []

    def _get_foreman_client(self, config_file='/etc/ai/ai.conf'):
        """Retrieve Foreman Client."""
        self.logger.info('called')
        # Loading the aitools configuration file
        config = SafeConfigParser()
        with open(config_file) as handler:
            config.readfp(handler)

        return ForemanClient(
            host=config.get('foreman', 'foreman_hostname'),
            port=config.get('foreman', 'foreman_port'),
            timeout=config.get('foreman', 'foreman_timeout'),
            deref_alias=config.get('foreman', 'dereference_alias'))

    def _get_infoream_client(self):
        """Retrieve InforEAM client."""
        self.logger.info('called')
        config = read_config_file(self.config_file)
        return InforEamClient(config['infoream']['username'],
                              config['infoream']['password'])

    def _get_ironic_client(self):
        """Retrieve Openstack Ironic client."""
        self.logger.info('called')
        cfg = read_config_file(self.config_file)
        auth = auth_k(auth_url=cfg['ironic']['auth_url'],
                      project_name=cfg['ironic']['project_name'],
                      project_domain_id=cfg['ironic']['project_domain_id'],
                      identity_provider=cfg['ironic']['identity_provider'],
                      protocol=cfg['ironic']['protocol'],
                      mutual_auth=cfg['ironic']['mutual_auth'])
        session = keystone_session.Session(auth=auth)
        return ironic_client.get_client(api_version=1, session=session)


    def _get_logger(self, loglevel=ERROR):
        """Set a logger and configure it."""
        logger = getLogger(self.LOGGER_NAME)
        logger.propagate = False
        logger.setLevel(loglevel)
        if not logger.handlers:
            console_handler = StreamHandler()
            console_handler.setLevel(INFO)
            formatter = Formatter(
                '%(name)s:%(funcName)22s() '
                '%(levelname)s - '
                '%(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        logger.info('Logger initialized')
        return logger

    def _test_ipmi(self, bmc_ip, username, password):
        """Retrieve SEL info to test the connection"""
        self.logger.info('called')
        self.logger.info('IP: %s U: %s P: %s', bmc_ip, username, password)

        cmd_str = '/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s sel' \
                  % (bmc_ip, username, password)
        cmd = Popen(cmd_str, shell=True, executable='/bin/bash',
                    stdout=PIPE, stderr=PIPE)
        cmd_rpl, dummy = cmd.communicate()

        # Check for a valid reply from BMC
        valid_cn = re.compile(r"SEL\sInformation\nVersion\s+:")
        if valid_cn.search(cmd_rpl) is None:
            return False

        return True


    def _sanitize_ipmidb(self, host, serial, bmc_ip,
                         username, password, records=None):
        """Verify integrity of IPMIDB records, take corrective actions"""
        self.logger.info('called')

        debug = 'Row to insert: %s %s %s %s %s' % (host, serial, bmc_ip,
                                                   username, password)

        if len(records) != 1:
            self.logger.info('more than one record in IPMIDB')
        elif records[0][1] != '%s.cern.ch' % host.lower() or \
             records[0][2] != serial.lower() or \
             records[0][3] != bmc_ip or \
             records[0][4] != username or \
             records[0][5] != password:
            self.logger.info('record in IPMIDB is not correct')
        else:
            self.logger.info('no need for sanitization')
            return True

        # Delete all the rows in IPMIDB
        for row in records:
            self.logger.info('deleting row %s', row[0])
            query = 'del_ipmi/?%s' % urlencode({'rowid': row[0]})
            response = self.ipmidb.query_ipmidb(query)
            if response['rowcount'] != 1:
                self.logger.error('ERROR DELETING: %s', debug)
                return False

        # Insert a the good one
        try:
            self.logger.info('saving correct row')
            query = 'add_ipmi/?%s' % urlencode(
                {'hostname': '%s.cern.ch' % host.lower(),
                 'bmcip':    bmc_ip,
                 'serial':   serial.lower(),
                 'username': username,
                 'password': password})
            response = self.ipmidb.query_ipmidb(query)
        except IPMIDBError as excpt:
            self.logger.error('ERROR ADDING: %s %s', query, excpt)
            return False

        self.logger.info('completed')
        return True

    def get_all_ipmidb_rows(self, bmc_ip, hostname, serial):
        """ Returns all rows present in IPMIDB for IP, Hostname and Serial."""

        try:
            # Check if creds in IPMIDB by IP, Hostname and Serial
            query = 'get_row/?%s' % urlencode({'bmcip': bmc_ip})
            res = self.ipmidb.query_ipmidb(query)
            query = 'get_row/?%s' % urlencode({'hostname': '%s.cern.ch' % hostname})
            res_hostname = self.ipmidb.query_ipmidb(query)
            query = 'get_row/?%s' % urlencode({'serial': serial})
            res_serial = self.ipmidb.query_ipmidb(query)
        except ValueError:
            # No JSON object could be decoded, log it
            self.logger.error('ERROR IPMIDB QUERY!')
            return []

        # Search for result duplicates among the queries
        for row in res_hostname:
            for exisiting_row in res:
                if exisiting_row[0] == row[0]:
                    break
            else:
                res.append(row)

        for row in res_serial:
            for exisiting_row in res:
                if exisiting_row[0] == row[0]:
                    break
            else:
                res.append(row)

        return res

    def handle_node_by_serial(self, serial):
        """ Sanitize a node by its serial number """
        # Search node in LanDB
        self.devicesearch.Location = None
        self.devicesearch.SerialNumber = serial

        try:
            hostname = self.landb_service.searchDevice(self.devicesearch)[0]
        except IndexError:
            raise IPMIDBSanitizerError('no LanDB entry for %s' % serial)

        node = self.landb_service.getDeviceBasicInfo(hostname)
        bmc_hostname = '%s-ipmi' % node.SerialNumber
        bmc_username = None
        bmc_password = None

        # Retrieve BMC IP
        try:
            bmc_ip = gethostbyname(bmc_hostname)
        except gaierror:
            raise IPMIDBSanitizerError('No BMC IP for %s %s' %
                                       (node.DeviceName, node.SerialNumber))

        self.logger.info('checking %s %s', node.DeviceName, node.SerialNumber)

        # Get all IPMIDB rows
        res = self.get_all_ipmidb_rows(bmc_ip,
                                       node.DeviceName,
                                       node.SerialNumber)

        # Set found state to False
        found = False

        # Test the credentials for a good match
        for tmp_creds in res:
            if self._test_ipmi(bmc_ip, tmp_creds[4], tmp_creds[5]):
                bmc_username, bmc_password = tmp_creds[4], tmp_creds[5]
                found = self._sanitize_ipmidb(node.DeviceName,
                                              node.SerialNumber, bmc_ip,
                                              bmc_username, bmc_password,
                                              records=res)
                break
        else:
            self.logger.info('no good rows in IPMIDB for %s %s',
                             node.DeviceName, node.SerialNumber)

        if not found:
            # Fetch from Openstack
            self.logger.info('trying in Ironic')
            if node.SerialNumber.lower() in self.ironic_uuid_map:
                self.logger.info('found in Ironic')
                uuid = self.ironic_uuid_map[node.SerialNumber.lower()]
                console = self.ironic.node.get_console(uuid)
                if self._test_ipmi(bmc_ip,
                                   console['console_info']['username'],
                                   console['console_info']['password']):
                    bmc_username = console['console_info']['username']
                    bmc_password = console['console_info']['password']
                    found = self._sanitize_ipmidb(node.DeviceName,
                                                  node.SerialNumber, bmc_ip,
                                                  bmc_username, bmc_password,
                                                  records=res)

        if not found:
            # Fetch from Foreman
            self.logger.info('trying in Foreman')
            try:
                f_username, f_password = self.foreman.get_ipmi_credentials(
                    '%s.cern.ch' % node.DeviceName.lower())
                if self._test_ipmi(bmc_ip, f_username, f_password):
                    bmc_username, bmc_password = f_username, f_password
                    found = self._sanitize_ipmidb(node.DeviceName,
                                                  node.SerialNumber,
                                                  bmc_ip,
                                                  bmc_username,
                                                  bmc_password,
                                                  records=res)
            except AiToolsForemanError as excpt:
                self.logger.error('AiTools exception: %s', excpt)
                found = False

        if not found:
            raise IPMIDBSanitizerError('no creds found for %s %s' %
                                       (node.DeviceName, node.SerialNumber))

    def run(self):
        """Execute sanitization."""
        self.logger.info('called')

        # Get list of nodes from Ironic (Openstack)
        ironic_list = self.ironic.node.list(fields=['uuid', 'name'])
        self.ironic_uuid_map = {x.name:x.uuid for x in ironic_list}
        self.logger.info('total Ironic nodes: %s', len(self.ironic_uuid_map))

        # Get list of nodes from InforEAM
        hosts = self.infoream.extract_hosts()
        self.logger.info('total InforEAM nodes: %s', len(hosts))

        # For each node
        self.logger.info('Entering main loop')
        for serial in hosts:
            try:
                self.handle_node_by_serial(serial)
            except IPMIDBSanitizerError as excpt:
                self.logger.error('unable to sanitize: %s', excpt)
                continue
    
    def run_single_node(self, serial):
        """Execute sanitization."""
        self.logger.info('called')


        # For each node
        self.logger.info('Sanitizing %s' % serial)
        try:
            self.handle_node_by_serial(serial)
        except IPMIDBSanitizerError as excpt:
            self.logger.error('unable to sanitize: %s', excpt)

