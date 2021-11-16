import base64
import hashlib
import os

import requests as requests
from django.conf import settings
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def get_authorization_header():
    auth = settings.LDAP_USERNAME + ':' + settings.LDAP_PASSWORD

    message_bytes = auth.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message


'''


from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
nonce = os.urandom(16)
algorithm = algorithms.ChaCha20(key, nonce)
cipher = Cipher(algorithm, mode=None)
encryptor = cipher.encryptor()
ct = encryptor.update(b"a secret message")
decryptor = cipher.decryptor()
decryptor.update(ct)
b'a secret message'

'''


def getHash(key, plaintext, associated_data):
    iv = os.urandom(12)

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (iv, ciphertext, encryptor.tag)


def encrypt(plaintext):
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    enc_obj = AES.new(key, AES.MODE_GCM)
    ciphertext, auth_tag = enc_obj.encrypt_and_digest(plaintext)
    return ciphertext, auth_tag, enc_obj.nonce


def auth(username, password):
    auth_header = get_authorization_header()
    # hash_password = encrypt(password)['chippertext']

    sample_string = password
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")

    headers = {'Authorization': 'Basic ' + auth_header, 'user_username': username, 'user_password': base64_string}
    response = requests.post(settings.LDAP_URL + '/api/kullanici/authenticate', headers=headers)

    response_data = response.json()
    is_auth = response_data.get('basariliMi')

    return is_auth


def get_user_information_by_email(username):
    auth_header = get_authorization_header()
    # hash_password = encrypt(password)['chippertext']

    headers = {'Authorization': 'Basic ' + auth_header}
    response = requests.get(settings.LDAP_URL + '/api/kullanici/kullanici-adi/' + username, headers=headers)

    response_data = response.json()
    is_auth = response_data.get('basariliMi')

    if is_auth and len(response_data.get('data')) > 0:
        data_arr = response_data.get('data')
        return data_arr[0]

    return None


def get_user_information_by_username(email):
    auth_header = get_authorization_header()
    # hash_password = encrypt(password)['chippertext']

    headers = {'Authorization': 'Basic ' + auth_header}
    response = requests.get(settings.LDAP_URL + '/api/kullanici/kullanici-email/' + email, headers=headers)

    response_data = response.json()
    is_auth = response_data.get('basariliMi')

    if is_auth and len(response_data.get('data')) > 0:
        data_arr = response_data.get('data')
        return data_arr[0]

    return None
