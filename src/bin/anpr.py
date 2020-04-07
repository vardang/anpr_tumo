import argparse
from lib.commons.config_loader import load_config_module

if __name__ == '__main__':

    help_info = '''
        Automatic Number Plate Recognition (ANPR)
        '''

    parser = argparse.ArgumentParser(description=help_info, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--config", required=True, help="Configuration module name, by which ANPR is performed")
    parser.add_argument("--image", required=True, help="Image path")
    args = parser.parse_args()

    config = args.config
    image = args.image

    config_modlue = load_config_module(config)

    print('\033[94m' + config_modlue.recognise(image) + '\033[0m')