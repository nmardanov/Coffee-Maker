from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, HTMLBody


def Email(to, cc_mail, body, attachmentspath=None):
    creds = Credentials(
        #login information for where email is being sent from
        username='lamarhstech@outlook.com',
        password='DiyaIsAmazing!2023!'
    )
    account = Account(
        primary_smtp_address='lamarhstech@outlook.com',
        credentials=creds,
        autodiscover=True,
        access_type=DELEGATE
    )

    m = Message(
        account=account,
        cc_recipients=cc_mail,
        subject='Information Regarding Your Student',
        body=HTMLBody(body),
        to_recipients=[Mailbox(email_address=to)]
    )
    m.send()


print("email sent")