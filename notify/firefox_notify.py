import requests
from bs4 import BeautifulSoup
import time
import smtplib

# Configuration
URL = "https://www.vfsglobal.com/lithuania"  # Replace with actual URL
HEADERS = {"User-Agent": "Mozilla/5.0"}
EMAIL = "your-email@example.com"
PASSWORD = "your-email-password"

def check_slots():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Replace with actual logic to detect slots
    if "Slots Available" in soup.text:
        notify("Slots are available!")

def notify(message):
    # Email notification
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(
            EMAIL,
            "recipient-email@example.com",
            f"Subject: VFS Slot Alert\n\n{message}"
        )

def main():
    while True:
        check_slots()
        time.sleep(300)  # Wait 5 minutes before rechecking

if __name__ == "__main__":
    main()
