import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
import hashlib


def str_encrypt(str):
    sha = hashlib.sha1(str)
    encrypts = sha.hexdigest()
    return encrypts