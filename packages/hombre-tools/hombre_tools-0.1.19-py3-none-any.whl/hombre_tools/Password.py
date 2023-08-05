"""
stanislav Vohnik password utility
2019-08-10
"""
import keyring
from argparse import ArgumentParser
from pyperclip import paste, copy as clipcopy

PARSER = ArgumentParser(description='Password Utility version 0.1')

PARSER.add_argument("--user",
                    help='login name',
                    required=False,
                    default='Stanislav_Vohnik')

PARSER.add_argument("--service",
                    help='service name',
                    required=True)

PARSER.add_argument("--action",
                    help='login name',
                    required=True)

if __name__ == 'main':
    ARGS = PARSER.parse_args()
    if ARGS.action == 'set':
        pswd = paste
        keyring.set_password(ARGS.sevice, ARGS.user, pswd)
        print('password setted from clipboard')

    if ARGS.action == 'get':
        clipcopy(keyring.get_password(ARGS.sevice, ARGS.user))
        print('get to clip board')
        