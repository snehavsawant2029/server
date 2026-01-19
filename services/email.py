import os
import resend

resend.api_key = os.getenv("RESEND_API_KEY")

SMTP_TO = os.getenv("SMTP_TO")  

def send_contact_email(name: str, email: str, subject: str, message: str):
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    
    try:
        params = {
            "from": "onboarding@resend.dev",  # ← Changed this to Resend's test domain
            "to": [SMTP_TO],
            "subject": subject,
            "text": body,
            "reply_to": email
        }
        
        response = resend.Emails.send(params)
        return response
    except Exception as e:
        print(f"Error: {e}")
        raise