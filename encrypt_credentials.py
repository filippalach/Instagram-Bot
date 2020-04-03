#!/usr/local/bin/python3

import getpass

import credentials

if __name__ == '__main__':
    login = getpass.getpass('Provide your email: ')
    password = getpass.getpass('Provide your password: ')
    credentials.encrypt_credentials(login, password)