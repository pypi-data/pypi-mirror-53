import json
def read_config_file(config_file, section=None):
    """Reads the given JSON configuration file.

    :param config_file: the configuration file.
    :type config_file: str
    :param section: a section name, defaults to None.
    :type section: str
    :returns: the configuration data dictionary
    :rtype: dict
    """
    with open(config_file, 'rb') as json_data_file:
        config = json.load(json_data_file)
    return config if section is None else config[section]
