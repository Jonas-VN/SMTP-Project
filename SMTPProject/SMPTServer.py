import smtplib
from .Email import Email

class SMTPServer:
    def __init__(self) -> None:
        self.port = 587
        self.session = None
        self.SMTPServers = {
            "gmail.com": "smtp.gmail.com",
            "hotmail.com": "smtp.office365.com",
            "telenet.be": "smtp.telenet.be",
            "outlook.com": "smtp-mail.outlook.com",
        }

    def log_in(self, username: str, password: str) -> bool:
        if (not self.session and username.split("@")[1] in self.SMTPServers):
            self.session = smtplib.SMTP(self.SMTPServers.get(username.split("@")[1]), self.port)

            ehlo_response = self.session.ehlo()
            if b"STARTTLS" in ehlo_response[1]:
                self.session.starttls()

            self.session.login(username, password)
            print(f"\nSuccessfully logged into {username}!")
            return True
        elif (self.session): 
            raise ConnectionError("Close your previous session first before starting a new one!")
        elif (username.split("@")[1] not in self.SMTPServers):
            raise ValueError("This email isn't supported unfortunately!")

    def log_out(self) -> bool:
        if (self.session):
            self.session.quit()
            self.session = None
            print(f"Successfully logged out!\n")
            return True
        else:
            print("Unable to log out, you weren't logged in!")
            return False

    def send_email(self, email: Email):
        if (not email.msg["From"]):
            raise ValueError("You must set a sender email")
        if (not email.msg["To"]):
            raise ValueError("You must set a receiver email")
        if self.session.noop()[0] != 250:
            raise ConnectionError("Server is offline")

        self.session.send_message(email.msg)
        print(f'Sent an email from {email.msg["From"]} to {email.msg["To"]}')


