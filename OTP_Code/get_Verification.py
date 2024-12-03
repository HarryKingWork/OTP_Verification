import imaplib
import email
from email.header import decode_header

# Gmail login credentials
gmail_user = "Litvatest1@gmail.com"
app_password = "Bs#1122331"  # Use App Password if 2FA is enabled

# Set up connection to Gmail
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Login to Gmail
mail.login(gmail_user, app_password)

# Select the mailbox you want to read from
mail.select("inbox")  # You can change this to "Sent" or other folders

# Search for emails from the specific sender
status, messages = mail.search(None, 'FROM', '"donotreply@vfshelpline.com"')

# Get the list of email IDs
email_ids = messages[0].split()

# Loop through each email ID and fetch the email
for email_id in email_ids:
    # Fetch the email by ID
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            # Parse the email content
            msg = email.message_from_bytes(response_part[1])
            
            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Get the sender's email address
            from_ = msg.get("From")
            
            # If the email message is multipart
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    # If the part is plain text
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        body = part.get_payload(decode=True).decode()
                        print("Subject:", subject)
                        print("From:", from_)
                        print("Body:", body)  # This is the SMS text
            else:
                # If the email is not multipart
                body = msg.get_payload(decode=True).decode()
                print("Subject:", subject)
                print("From:", from_)
                print("Body:", body)  # This is the SMS text

# Logout from the email server
mail.logout()
