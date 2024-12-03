from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import smtplib

# Configuration
URL = "https://www.vfsglobal.com/lithuania"  # Replace with actual URL
CHROME_DRIVER_PATH = "path/to/chromedriver"  # Update this path
EMAIL = "your-email@example.com"
PASSWORD = "your-email-password"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Email notification function
def send_email(subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL, EMAIL, message)

# Slot-checking function
def check_slots():
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)

    try:
        # Replace the following with the correct element locator
        availability_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Available')]")
        if availability_element:
            print("Slots are available!")
            send_email("VFS Slot Alert", "Slots are now available on VFS Global.")
    except Exception as e:
        print("Slots are not available yet.")
    finally:
        driver.quit()

# Main function
def main():
    while True:
        check_slots()
        time.sleep(300)  # Wait for 5 minutes before checking again

if __name__ == "__main__":
    main()
