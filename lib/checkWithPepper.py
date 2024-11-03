import hashlib
import string
from random import choice


def checkWithPepper(password,correctHash):
    chars = string.ascii_letters

    for i in range(len(chars)):
        passwordToCheck = password + chars[i]
        if hashlib.sha256(passwordToCheck.encode("utf-8")).hexdigest() == correctHash:
            return True
    
    return False