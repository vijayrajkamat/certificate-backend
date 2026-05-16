import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()


def send_certificate_email(to_email, name, pdf_path):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")

    subject = "Your Personal Purpose Card!"

    body = f"""Hi {name},

Your Personal Purpose Card is attached! You can take a colour print and pin it at your desk. Will serve as a compass when you are feeling demotivated, unfulfilled or overwhelmed.

You can even take a print on 'certificate paper' at your nearest stationery shop for around Rs. 20.

Hope your new found insights produce a new way of seeing, a new way of being.

If you every have any questions, feel free to reach out!

Warmly,
Vijayraj Kamat
"""

    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with open(pdf_path, "rb") as file:
        pdf_data = file.read()

    pdf_filename = os.path.basename(pdf_path)

    message.add_attachment(
        pdf_data,
        maintype="application",
        subtype="pdf",
        filename=pdf_filename
    )

    try:
        print("Connecting to SMTP server...")

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            print("Logging in...")
            smtp.login(smtp_user, smtp_password)

            print("Sending email...")
            smtp.send_message(message)

            print("Email sent successfully!")

    except Exception as e:
        print("EMAIL ERROR:")
        print(str(e))
        raise