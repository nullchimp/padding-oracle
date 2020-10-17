import base64
import time
import requests
import json


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

import random

def _make_key(key_len):
    charset = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&/()%$"-.;[]{}='

    k = b''
    for i in range(key_len):
        k += bytes([charset[random.randint(0, len(charset)-1)]])

    print(k)
    return k


key = _make_key(16)

def _encrypt_data(data):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(pad(data, 16, style='pkcs7'))
    return iv + enc

def _decrypt_data(enc):
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_params = cipher.decrypt(enc[16:])
    return unpad(padded_params, 16, style='pkcs7')

def obtain():
    # Returns the cipher text
    plain = b'{"name": "NULLch' \
            b'imp"}           ' \
            b'                '

    res = {"name": "NULLchimp", "validator": base64.encodebytes(bytes(_encrypt_data(plain))).decode('utf-8')}
    return json.dumps(res)

def send(req):
    data = json.loads(req)
    cipher = base64.decodebytes(data["validator"].encode())

    try:
        d = _decrypt_data(cipher)
    except ValueError: # Throws an error if the padding is incorrect
        return json.dumps({"error": "Invalid Padding"})

    try:
        j_data = json.loads(d.decode("utf-8"))
        if data["name"] == j_data["name"]:
            global key
            key = _make_key(16)
            return json.dumps({"success": data["name"]})
    except:
        return json.dumps({"error": "Something went wrong"})

    return json.dumps({"success": "done"})