from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes


key = b'1111111111111111'#get_random_bytes(16)


def encrypt_data(data):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(pad(data, 16, style='pkcs7'))
    return iv + enc


def decrypt_data(enc):
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_params = cipher.decrypt(enc[16:])
    return unpad(padded_params, 16, style='pkcs7')