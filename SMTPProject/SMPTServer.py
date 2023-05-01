import smtplib
from .Email import Email

class SMTPServer:
    def __init__(self, ssl_encryption = True, debug = False):
        self.ssl_encryption = ssl_encryption
        self.is_debug_on = debug
        self.session = None

    def debug(self, text: str):
        if self.is_debug_on:
            print(f"\n{text}\n")

    def log_in(self, username: str, password: str):
        self.debug("Login started!")
        self.log_out()
        if self.session: 
            raise ConnectionError("Close your previous session first before starting a new one!")
        
        email_provider = username.split("@")[1]
        if email_provider in SMTP_SERVERS:
            server = SMTP_SERVERS.get(email_provider)
            if self.ssl_encryption and email_provider == "gmail.com": # SSL doesn't work with hotmail? So only when using gmail...
                self.session = smtplib.SMTP_SSL(server, 465)
                if self.is_debug_on: self.session.set_debuglevel(1)
            else:
                self.session = smtplib.SMTP(server, 587)
                if self.is_debug_on: self.session.set_debuglevel(1)
                self.debug("Testing server start!")
                ehlo_response = self.session.ehlo()
                if b"STARTTLS" in ehlo_response[1]:
                    self.debug("TLS is available!")
                    self.session.starttls()
                self.debug("Testing server end!")
            self.session.login(username, password)
            self.debug(f"Successfully logged into {username}!")
        else:
            raise ValueError("This email isn't supported unfortunately!")

    def log_out(self):
        self.debug("Log out start!")
        if self.session:
            self.session.quit()
            self.session = None
            self.debug("Successfully logged out!")
        self.debug("Log out end!")

    def send_email(self, email: Email):
        self.debug("Send email start!")
        if not email.msg["From"]:
            raise ValueError("You must set a sender email") 
        if not email.msg["To"]:
            raise ValueError("You must set a receiver email")
        self.debug("Testing if connection is available!")
        if self.session.noop()[0] != 250:
            raise ConnectionError("Server is offline")
        self.debug("Connection is still available!")
        self.session.send_message(email.msg)
        self.debug(f'Sent an email from {email.msg["From"]} to {email.msg["To"]}')


SMTP_SERVERS = {
    'gmail.com': 'smtp.gmail.com',
    'yahoo.com': 'smtp.mail.yahoo.com',
    'outlook.com': 'smtp.office365.com',
    'hotmail.com': 'smtp.office365.com',
    'telenet.be': 'smtp.telenet.be',
}
