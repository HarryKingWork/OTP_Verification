from imapclient import IMAPClient

email = "Litvatest1@gmail.com"
app_password = "Bs#1122331"

with IMAPClient("imap.gmail.com", ssl=True) as client:
    client.login(email, app_password)
    print("Login successful!")