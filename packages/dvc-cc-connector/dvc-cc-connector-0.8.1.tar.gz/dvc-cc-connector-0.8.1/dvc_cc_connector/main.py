from argparse import ArgumentParser
import json
import os
from shutil import copyfile

def receive_file(access, local_file_path):
    copyfile(access, local_file_path)

def receive_file_validate(access):
    try:
        with open(access) as json_data:
            d = json.load(json_data)
        print('This is a valid file.')

    except ValueError as e:
        print('invalid json: %s' % e)
        exit(1) # or: raise

def cli_version():
    print('0.1')

def main():
    
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    parser_a = subparsers.add_parser('receive-file')
    parser_a.add_argument(
        'access',help='The access_json file see here for more information: https://www.curious-containers.cc/docs/developing-custom-connectors')
    parser_a.add_argument(
        'local_file_path', help='The internal_json file see here for more information: https://www.curious-containers.cc/docs/developing-custom-connectors')

    parser_b = subparsers.add_parser('receive-file-validate')
    parser_b.add_argument(
        'access', help='The access_json file see here for more information: https://www.curious-containers.cc/docs/developing-custom-connectors')



    parser_c = subparsers.add_parser('cli-version')

    parser.parse_args()
    
    kwargs = vars(parser.parse_args())
    
    subparser = kwargs.pop('subparser')

    if subparser == 'receive-file':
        receive_file(**kwargs)
    elif subparser == 'receive-file-validate':
        receive_file_validate(**kwargs)
    elif subparser == 'cli-version':
        cli_version()
    else:
        parser.print_help()
        raise ValueError("You used the dvc-cc-connector with wrong parameters.")
    
