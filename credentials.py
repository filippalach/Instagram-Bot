import json
import os
from dataclasses import dataclass

from cryptography.fernet import Fernet

import logger
import exceptions

log = logger.create_logger('ig_bot.credentials')

CONFIG_PATH = 'config.json'

# TODO: implement proper configuartion mechanism.
try:
    with open(CONFIG_PATH) as config:
        data = json.load(config)
except(FileNotFoundError):
    log.exception(f'Configuration file config.json was not found in root directory.')
    raise exceptions.NoConfig

try:
    PATH = data['encryption']['path']
except(KeyError):
    log.exception(f'Specify encryption.path fields in {CONFIG_PATH}')
    raise exceptions.BadConfig

KEY_PATH = f'{PATH}/symmetric_key'
CREDS_PATH = f'{PATH}/creds'

@dataclass
class Credentials():
    """Dataclass for storing credentials: login & password."""

    __slots__ = ['login', 'password']
    login: str
    password: str

def encrypt_credentials(login: str, password: str) -> None:
    """
    Encrypts given login & password. Stores: key in encryption.path/symmetric_key,
    login and password in enryption.path/creds.

    :param login: login to be encrypted
    :param password: password to be encrypted

    :return: None
    """

    fernet_key = Fernet.generate_key()
    fernet = Fernet(fernet_key)

    try:
        with open(KEY_PATH, 'w+') as key:
            key.write(fernet_key.decode())

        with open(CREDS_PATH, 'w+') as creds:
            creds.write(f'{(fernet.encrypt(login.encode())).decode()}\n')
            creds.write((fernet.encrypt(password.encode())).decode())
    except(PermissionError):
        log.exception(f'You dont have permissions to write to {KEY_PATH} or {CREDS_PATH}. Run with sudo.')
    finally:
        os.chmod(KEY_PATH, 0o600)
        os.chmod(CREDS_PATH, 0o600)

def read_credentials() -> Credentials:
    """
    Reads Credentials from path provided in config.

    :return: credentials; login & password
    """

    try:
        with open(KEY_PATH) as key:
            fernet_key = key.read()
    except(PermissionError):
        log.exception(f'You dont have permissions to read from {KEY_PATH}. Run with sudo.')

    fernet = Fernet(fernet_key.encode())

    with open(CREDS_PATH) as creds:
        lines = creds.readlines()
        decrypted_login: str = fernet.decrypt(lines[0].encode()).decode()
        decrypted_password: str = fernet.decrypt(lines[1].encode()).decode()
    
    return Credentials(decrypted_login, decrypted_password)