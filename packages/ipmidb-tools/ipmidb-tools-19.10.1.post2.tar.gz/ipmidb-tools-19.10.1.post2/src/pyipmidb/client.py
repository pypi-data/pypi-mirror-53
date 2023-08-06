"""Snippet for IPMIDB APIs interaction"""
import json
from cookielib import MozillaCookieJar
from logging import DEBUG, ERROR, INFO, Formatter, StreamHandler, getLogger
from subprocess import PIPE, Popen
from tempfile import mkstemp
import urllib3
from requests import Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3 import disable_warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

disable_warnings(InsecureRequestWarning)
class IPMIDBError(Exception):
    """An error occurred while interacting with IPMIDB."""
    pass


class GetSSOCookieError(Exception):
    """An error occurred while retrieving SSO cookie."""

    pass


class IPMIDBClient(object):
    """Snippet for IPMIDB APIs interaction"""
    LOGGER_NAME = 'ipmidb'

    def __init__(self, endpoint='ipmidb.cern.ch', cookie_path=None, debug=False):

        if debug:
            loglevel = DEBUG
        else:
            loglevel = ERROR

        self._set_logger(loglevel)

        self.endpoint = endpoint
        self.endpoint_url = 'https://%s' % self.endpoint

        self._set_cookie_path(cookie_path)
        self.cookiejar = MozillaCookieJar(self.cookie_path)
        self._get_cookie()

    def _set_logger(self, loglevel=None):
        """Set a logger and configure it."""
        self.logger = getLogger(self.LOGGER_NAME)
        self.logger.setLevel(loglevel)
        if not self.logger.handlers:
            console_handler = StreamHandler()
            console_handler.setLevel(INFO)
            formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.info('Logger initialized')

    def _set_cookie_path(self, cookie_path):
        """Check and create folder for temporary and safe token storage."""
        self.logger.info('Setting cookie path')
        if not cookie_path:
            # Default cookie path
            _, self.cookie_path = mkstemp(prefix='ipmidb_sso_cookie_')
        else:
            # User specified folder
            _, self.cookie_path = mkstemp(prefix='ipmidb_sso_cookie_',
                                          dir=cookie_path)

        self.logger.info('Cookie path set to %s', self.cookie_path)

    def _get_cookie(self):
        """Retrieve and write authentication cookie."""
        self.logger.info('Setting cookie')

        # Getting the cookie through cern-get-sso-cookie,
        cmd_str = 'cern-get-sso-cookie --krb -r -u "%s/get_row" -o "%s"' \
                  % (self.endpoint_url, self.cookie_path)
        cmd = Popen(cmd_str, shell=True,
                    executable='/bin/bash',
                    stdout=PIPE, stderr=PIPE)
        cmd_rpl, _ = cmd.communicate()
        if cmd_rpl:
            raise GetSSOCookieError('Unexpected output for: %s' % cmd_str)

        # Loading loading cookiejar
        self.cookiejar.load()

    def query_ipmidb(self, query):
        self.logger.debug('called')
        # Check cookie jar for expired cookies
        if not self.cookiejar:
            self._get_cookie()

        # Opening IPMIDB requests Session for cookie persistency
        session = Session()
        session.cookies = self.cookiejar

        req = session.get('%s/%s' % (self.endpoint_url, query), verify=False)

        ipmidb_result = json.loads(req.text)
        if ipmidb_result['code'] is not 0:
            raise IPMIDBError('IPMIDB returned error code %s'
                              % ipmidb_result['code'])

        return ipmidb_result['result']
