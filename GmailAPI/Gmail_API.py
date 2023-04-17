#AIzaSyCrCyfLHsXhD_AgbDyE66re2LI9ylX3OKk

import imaplib
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
#username = os.environ.get("username")
#password = os.environ.get("password")
username = "lhsrobobarista@outlook.com"
password = "Coffee1!"

# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for office 365, it's this:
imap_server = "outlook.office365.com"

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# total number of emails
messages = int(messages[0])
rem = messages

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


def SendEmail(to, cc_mail, body, attachmentspath=None):
    # Check if the email address is for a T-Mobile or Verizon number
    if "@tmomail.net" in to or "@vtext.com" in to:
        # Extract the phone number from the email address
        phone_number = re.sub(r"@.*", "", to)
        # Send the SMS using Twilio
        send_sms_twilio(phone_number, body)
    else:
        creds = Credentials(
            # login information for where the email is being sent from
            username="lhsrobobarista@outlook.com",
            password="Coffee1!"
        )
        account = Account(
            primary_smtp_address=username,
            credentials=creds,
            autodiscover=True,
            access_type=DELEGATE
        )

        m = Message(
            account=account,
            cc_recipients=cc_mail,
            subject=None,
            body=HTMLBody(body),
            to_recipients=[Mailbox(email_address=to)]
        )
        print(body)
        m.send()



#Main loop
def checkMail():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    messages = int(messages[0])
    rem = messages
#Have to login each loop to refresh the inbox. Redefine messages to see if any new ones are available.
    while 1:
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        messages = int(messages[0])
        #If there are new messages, read the contents of the newest message
        if messages != rem:
            res, msg = imap.fetch(str(messages), "(RFC822)") 
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    print(msg['From'])
                    
                    return(get_contents(msg), msg['From'])
            rem = messages

        print("Looped")
        time.sleep(5)


# close the connection and logout
imap.close()
imap.logout()
