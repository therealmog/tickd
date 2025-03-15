from string import ascii_letters

def checkEmail(email):
    if "@" in email:
        splitEmail = email.split("@")
        
        accepted = ascii_letters + "."
        noOfDots = 0
        valid = True

        # Checking email suffix.
        for each in splitEmail[1]:
            if each == ".":
                noOfDots += 1
            if each not in accepted:
                # Instantly sets valid to False and breaks loop if a character is not in accepted.
                valid = False
                break
        
        # There cannot be more than 2 dots in an email suffix.
        if noOfDots > 2:
            valid = False
        
        return valid
    else:
        # No "@" in email.
        return False

print(checkEmail("test@gmail./com"))