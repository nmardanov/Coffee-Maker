#AIzaSyCrCyfLHsXhD_AgbDyE66re2LI9ylX3OKk

import imaplib
import email
from email.header import decode_header
from itertools import chain
import webbrowser
import os
import time
import re

#TODO:
#Loop only checks newest email every 30 seconds. If 2 are sent within that window, one is ignored. Fix this.
#Parse text to connect to pump script
#Send texts with drink list to users, or to confirm that orders are received


# account credentials
username = "robobarista@outlook.com"
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
                    return(get_contents(msg))
            rem = messages

        print("Looped")
        time.sleep(10)



# close the connection and logout
imap.close()
imap.logout()