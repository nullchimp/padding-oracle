import base64
import time
import requests

def _http_get(protocol, host, url, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            res = requests.get(f'{protocol}://{host}/{url}')
            return res.status_code, res.content
        except Exception as e:
            print(e)
            retries += 1
            time.sleep(10)


def is_valid(cipher):
    b64cipher = base64.encodebytes(cipher)
    b64payload = b64cipher.decode('utf-8').replace('=', '~').replace('/', '!').replace('+', '-')

    url = f'4a3b74c54e/?post={b64payload}'
    status, content = _http_get(protocol='http', host='34.74.105.127', url=url)

    utf8c = content.decode('utf-8')

    if 'raise PaddingException()' in utf8c:
        return False

    with open('log.txt', 'a') as fp:
        fp.write(b64payload+'\n'+utf8c+'\n')

    return True


def obtain():
    payload = b'pL8GQgwutB!5o3DuVCgmKkgEPQDV2jGIu8dLkvyKixMD4GASjeKZYp9rIEt!r-uOh20wJ0M2tf97qTSwm9zz6ibHdBLCt!bH3IP6NWXT8bSwo3pEJN8Dd4I!q0asNChjdbQwv4-s69qqCYzKQOHTxk-FR-GHnemeoEZbv0O5vdOkCNxgfdVJITTyJRDgQPKWfy5u1vpbvgnN1YymY2ARrA~~'

    b64payload = payload.decode('utf-8').replace('~', '=').replace('!', '/').replace('-', '+').encode()
    cipher_text = base64.decodebytes(b64payload)

    return cipher_text
