import os
import ssl
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_TO = os.getenv("SMTP_TO") or SMTP_USER

def send_contact_email(name: str, email: str, subject: str, message: str):
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_TO

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, SMTP_TO, msg.as_string())
