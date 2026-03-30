import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class OTPManager:
    # SMTP Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "prosthoplanner@gmail.com"
    SENDER_PASSWORD = "nqhv hfbo pjut htmz" 

    @staticmethod
    def generate_otp(length=4):
        """Generates a random numeric OTP"""
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    @classmethod
    def send_otp(cls, email, otp_code):
        """
        Sends an OTP via email using SMTP.
        """
        # console log for debugging
        print("\n" + "="*40)
        print(f"TRIGGERING EMAIL TO: {email}")
        print(f"SECURITY CODE: {otp_code}")
        print("="*40 + "\n")

        try:
            msg = MIMEMultipart()
            msg['From'] = cls.SENDER_EMAIL
            msg['To'] = email
            msg['Subject'] = "Your ProsthoPlanner Verification Code"

            body = f"""
            Hello,

            Thank you for signing up for ProsthoPlanner.
            Your verification code is: {otp_code}

            This code will expire in 10 minutes.

            Best regards,
            ProsthoPlanner Team
            """
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(cls.SMTP_SERVER, cls.SMTP_PORT)
            server.starttls()
            server.login(cls.SENDER_EMAIL, cls.SENDER_PASSWORD)
            text = msg.as_string()
            server.sendmail(cls.SENDER_EMAIL, email, text)
            server.quit()
            
            print(f"Successfully sent email to {email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
