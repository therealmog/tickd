# Amogh NG
# Tickd main

# Used for running the program.

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
    app = App(email,userPath=auth.userPath,theme=auth.theme)

