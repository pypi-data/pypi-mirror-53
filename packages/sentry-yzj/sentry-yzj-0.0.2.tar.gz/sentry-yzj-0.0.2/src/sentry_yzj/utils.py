import hashlib


def str_encrypt(str):
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts