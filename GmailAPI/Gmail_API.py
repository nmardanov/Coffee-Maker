#AIzaSyCrCyfLHsXhD_AgbDyE66re2LI9ylX3OKk

import imaplib

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email
from email.header import decode_header
from itertools import chain
import webbrowser
import os
import time
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody
import re

#twilio set up as backup
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_phone_number= os.environ.get("TWILIO_PHONE_NUMBER")




#TODO:
#Loop only checks newest email every 30 seconds. If 2 are sent within that window, one is ignored. Fix this.
#Parse text to connect to pump script
#Send texts with drink list to users, or to confirm that orders are received


# account credentials
username = os.environ.get("guser")
password = os.environ.get("gpass")


def save_attachment(part):
    filename = part.get_filename()
    if filename:
        with open(filename, 'wb') as f:
            f.write(part.get_payload(decode=True))

#Extracts the text from the .txt file sent to the email
def get_contents(pmsg):
    if not pmsg.is_multipart():
        pass
    for part in pmsg.walk():
        # extract content type of email
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        try:
            # get the email body
            body = part.get_payload(decode=True).decode()
        except:
            pass
        if content_type == "text/plain" and "attachment" not in content_disposition:
            # print text/plain emails and skip attachments, will print here for T-Mobile, but not for AT&T
            return body
        elif "attachment" in content_disposition:
            # print attachment contents, will print here for AT&T. Assumes that file is a .txt, because we should only be receiving texts
            filename = part.get_filename()
            if filename:
                save_attachment(part)
                f = open(filename, 'r')
                file_contents = f.read()
                
                return file_contents
    return "No text contents found"

def send_sms_twilio(to, body):
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        body=body + '\nPlease do not reply to this number',
        from_=twilio_phone_number,
        to=to
    )
    print("Message sent to", to)

def send_email_gmail(to, subject, body):
    # Create an SMTP connection to Gmail's server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Use TLS port
    smtp_username = username
    smtp_password = password

    try:
        smtp_server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_server.starttls()
        smtp_server.login(smtp_username, smtp_password)

        # Create an email message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to
        msg['Subject'] = subject

        # Attach the body
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        smtp_server.sendmail(smtp_username, to, msg.as_string())

        # Close the SMTP connection
        smtp_server.quit()

        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Modify the checkMail function as needed for Gmail, but keep the IMAP connection logic.

#Main loop
def checkMail():
    imap_server = "imap.gmail.com"

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    messages = int(messages[0])
    rem = messages

    while True:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        messages = int(messages[0])

        if messages != rem:
            res, msg = imap.fetch(str(messages), "(RFC822)") 
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    print(msg['From'])
                    return get_contents(msg), msg['From']
            rem = messages

        print("Looped")
        time.sleep(5)

    # Close the connection and logout (you can move this to outside the loop)
    imap.close()
    imap.logout()
