# Amogh NG
# Tickd main

from authcustomTk import Auth
from app import App


auth = Auth()
try:
    email = auth.loggedInEmail
except:
    email = ""
if email == "":
    print("No email. Cannot sign in to main program.")
else:
    #today = Today(email,userPath=auth.userPath,theme=auth.theme)
    app = App(email,userPath=auth.userPath,theme=auth.theme)

