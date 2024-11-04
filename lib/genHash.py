import hashlib
import string
from random import choice


def genSalt():
        chars = string.ascii_letters + "#£%*!" + "0123456789" # Specifically does not include $ sign.
        salt = ""
        for each in range(6):
            salt+=choice(chars)
        print(salt)

        return salt

def genPepper():
    chars = string.ascii_letters
    pepper = choice(chars)

    return pepper

def genHash(password):
    salt = genSalt()
    pepper = genPepper()

    passwordToHash = salt + password + pepper
    hash = hashlib.sha256(passwordToHash.encode()).hexdigest()

    passwordToStore = salt+"$"+hash

    return passwordToStore