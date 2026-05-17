import base64
import os

import resend
from dotenv import load_dotenv

load_dotenv()


def send_certificate_email(to_email, name, pdf_path):
    resend.api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL")

    if not resend.api_key:
        raise ValueError("RESEND_API_KEY is missing")

    if not from_email:
        raise ValueError("FROM_EMAIL is missing")

    subject = "Your Personal Purpose Card"

    body = f"""Hi {name},

Your Personal Purpose Card is attached! You can take a colour print and pin it at your desk. Will serve as a compass when you are feeling demotivated, unfulfilled or overwhelmed.

You can even take a print on 'certificate paper' at your nearest stationery shop for around Rs. 20.

Hope your new found insights produce a new way of seeing, a new way of being.

If you ever have any questions, feel free to reach out!

Warmly,
Vijayraj Kamat
"""

    pdf_filename = os.path.basename(pdf_path)

    with open(pdf_path, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")

    print("Sending email through Resend...")

    response = resend.Emails.send({
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "text": body,
        "attachments": [
            {
                "filename": pdf_filename,
                "content": pdf_base64
            }
        ]
    })

    print("Resend response:")
    print(response)

    return response