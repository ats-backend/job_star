import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from base64 import b64decode, b64encode


# data = b"My name is Luqman"


def encrypt_data(data):
    data_in_byte = bytes(data, 'utf-8')
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data_in_byte, AES.block_size))
    vector = b64encode(cipher.iv).decode('utf-8')
    data = b64encode(ct_bytes).decode('utf-8')
    json_key = b64encode(key).decode('utf-8')
    result = json.dumps({'key': json_key, 'vector': vector, 'data': data})
    return result


def decrypt_data(options):
    try:
        b64_data = json.loads(options)
    except:
        b64_data = json.loads((json.dumps(options)))
    data = {}
    for key, value in b64_data.items():
        vector = b64decode(value['iv'])
        ct = b64decode(value['ct'])
        encryption_key = b64decode(value['key'])
        cipher = AES.new(encryption_key, AES.MODE_CBC, vector)
        data_in_byte = unpad(cipher.decrypt(ct), AES.block_size)
        data_in_str = data_in_byte.decode('utf-8')
        data.update({key: data_in_str})
    return data


# encrypted_data = encrypt_data(data="BB-FD-0008")
# data = {"key": "IROfMeB+Bxz6uhAALUw97En6g032iWqRHp6mKV91718=", "iv": "RUMN5tWZU33Iocdw15fDaw==", "ct": "s2wjZ77CYgDFgn8/JX9Wdw=="}
# print(encrypted_data)
# print(decrypt_data(encrypted_data))
# print(decrypt_data({"key": "IROfMeB+Bxz6uhAALUw97En6g032iWqRHp6mKV91718=", "iv": "RUMN5tWZU33Iocdw15fDaw==", "ct": "s2wjZ77CYgDFgn8/JX9Wdw=="}))
