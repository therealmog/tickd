import hashlib
import string
from random import choice


def genSalt():
        chars = string.ascii_letters + "#£%*!" + "0123456789" # Specifically does not include $ sign.
        # Allows for full selection of characters.
        
        salt = ""
        for each in range(6):
            salt+=choice(chars)
            # Uses random module to choose 6 random characters

        return salt

def genPepper():
    chars = string.ascii_letters
    pepper = choice(chars) # One random character for extra randomness

    return pepper

def genHash(password):
    salt = genSalt()
    pepper = genPepper()

    passwordToHash = salt + password + pepper
    hash = hashlib.sha256(passwordToHash.encode()).hexdigest()
    # Hash is originally is in the bytes datatype, so it is casted to hex using hexdigest()

    passwordToStore = salt+"$"+hash

    return passwordToStore
