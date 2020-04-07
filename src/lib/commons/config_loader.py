from lib.commons.constants import ANPR_CONFIGS


def load_config_module(config_name):
    """
    Returns config module

    Args:
        config_name:

    Returns:

    """

    config = __import__(ANPR_CONFIGS + "." + config_name, fromlist=config_name)

    return config
