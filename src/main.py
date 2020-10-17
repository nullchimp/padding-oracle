import base64
import server
import exploit
import json

if __name__ == '__main__':
    def is_valid_cipher(cipher):
        data = server.send(json.dumps({"name": "Karl der Grosse", "validator": bytes_to_base64(cipher)}))
        data = json.loads(data)
        return not ('error' in data and data['error'] == "Invalid Padding")

    def bytes_to_base64(data):
        return base64.encodebytes(data).decode('utf-8')

    def base64_to_bytes(b64_data):
        return base64.decodebytes(b64_data.encode())

    print("#")
    res = json.loads(server.obtain())
    print(res)
    
    print("# Got JSON: ", res)
    cipher_text = base64_to_bytes(res["validator"])
    print("# Got Cipher: ", cipher_text)
    print("#")
    plain = exploit.find_plaintext(cipher_text, is_valid_cipher)
    print("# Got Plaintext: ", plain)

    wantd = b'{"name": "Karl d' \
            b'er Grosse"}     ' \
            b'                ' \
            b'               \x01'    

    if len(plain) != len(wantd):
        print(f"# Plain length: {len(plain)} != Wanted lenght: {len(wantd)}")
        exit("Cannot procceed with different length")

    print("# Now change it to ", wantd)
    print("#")

    new_cipher = exploit.change_cipher(bytearray(cipher_text), plain, wantd, is_valid_cipher)
    print("# Changed Chiper: ", new_cipher)
    print("#")
    print("# Sent to Server: ", server.send(json.dumps({"name": "Karl der Grosse", "validator": bytes_to_base64(new_cipher)})))