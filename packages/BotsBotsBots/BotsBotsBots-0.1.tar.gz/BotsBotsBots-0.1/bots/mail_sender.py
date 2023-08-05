import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass


PROTOCOL = "smtp.gmail.com"
PORT = 465


def get_password(file):
    with open(file, 'r') as handle:
        return handle.read().strip()


# https://realpython.com/python-send-email/
def send_mail(sender_email, sender_password, recipients, subject, body, attachments):
    if sender_password is None:
        # getpass works only on proper terminals, not in PyCharm terminal
        sender_password = getpass("Type password of {} and press enter:".format(sender_email))
        # sender_password = get_password('password.txt')

    recipients_string = ', '.join(recipients)
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipients_string
    message["Subject"] = subject
    message["Bcc"] = recipients_string  # Recommended for mass emails

    message.attach(MIMEText(body, "plain"))

    for file_path in attachments:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            file_name = os.path.basename(file_path)
            part.add_header('Content-Disposition', f"attachment; filename=\"{file_name}\"")
            message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(PROTOCOL, PORT, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, message.as_string())
    print('Email send successfully.')


if __name__ == '__main__':
    send_mail(
        sender_email="alarmmailsenderdsa@gmail.com",
        sender_password=None,
        recipients=["dinusergiuandrei@yahoo.com", 'dinusergiuandrei997@gmail.com', 'gamerwithgirlfriend@gmail.com'],
        subject='Subject from python',
        body='Test from python',
        attachments=['test_attachment', 'at2.txt', '../youtube/youtube_bot.py']
    )
