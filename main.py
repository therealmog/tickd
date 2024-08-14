# Amogh NG
# Tickd main

from authcustomTk import Auth
from today import Today

auth = Auth()
try:
    email = auth.loggedInEmail
except:
    email = ""
if email == "":
    print("No email. Cannot sign in to main program.")
else:
    today = Today(email,imgBGPath=auth.imgBGPath,userPath=auth.userPath)


