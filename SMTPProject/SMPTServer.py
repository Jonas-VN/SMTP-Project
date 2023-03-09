import smtplib
from .Email import Email

class SMTPServer:
    def __init__(self, debug = False) -> None:
        self.debug = debug
        self.port = 587
        self.session = None
        self.SMTPServers = {
            "gmail.com": "smtp.gmail.com",
            "hotmail.com": "smtp.office365.com",
            "telenet.be": "smtp.telenet.be",
            "outlook.com": "smtp-mail.outlook.com",
        }

    def log_in(self, username: str, password: str) -> bool:
        if self.debug:
            print("\nLogin started!\n")
        if not self.session and username.split("@")[1] in self.SMTPServers:
            self.session = smtplib.SMTP(self.SMTPServers.get(username.split("@")[1]), self.port)
            if self.debug: 
                self.session.set_debuglevel(1)

            if self.debug:
                print("\nTesting server start!\n")
            ehlo_response = self.session.ehlo()
            if b"STARTTLS" in ehlo_response[1]:
                if self.debug:
                    print("\nTLS is available!\n")
                self.session.starttls()
            if self.debug:
                print("\nTesting server end!\n")
            
            self.session.login(username, password)
            if self.debug:
                print(f"\nSuccessfully logged into {username}!\n")
            return True
        elif self.session: 
            raise ConnectionError("Close your previous session first before starting a new one!")
        elif username.split("@")[1] not in self.SMTPServers:
            raise ValueError("This email isn't supported unfortunately!")

    def log_out(self) -> bool:
        if self.debug:
            print("\nLog out start!\n")
        if self.session:
            self.session.quit()
            self.session = None
            if (self.debug):
                print(f"\nSuccessfully logged out!\n")
            return True
        else:
            raise ConnectionError("Unable to log out, you weren't logged in!")

    def send_email(self, email: Email) -> bool:
        if self.debug:
            print("\nSend email start!\n")
        if not email.msg["From"]:
            raise ValueError("You must set a sender email")
        if not email.msg["To"]:
            raise ValueError("You must set a receiver email")
        if self.debug:
            print("\nTesting if connection is available!\n")
        if self.session.noop()[0] != 250:
            raise ConnectionError("Server is offline")
        if self.debug:
            print("\nConnection is still available!\n")

        self.session.send_message(email.msg)
        if self.debug:
            print(f'\nSent an email from {email.msg["From"]} to {email.msg["To"]}\n')
        return True


