import smtplib
from .Email import Email

class SMTPServer:
    def __init__(self, debug = False) -> None:
        self.is_debug_on = debug
        self.port = 587
        self.session = None
        self.SMTPServers = {
            "gmail.com": "smtp.gmail.com",
            "hotmail.com": "smtp.office365.com",
            "telenet.be": "smtp.telenet.be",
            "outlook.com": "smtp-mail.outlook.com",
        }

    def debug(self, text: str) -> None:
        if self.is_debug_on:
            print(f"\n{text}\n")

    def log_in(self, username: str, password: str) -> bool:
        self.debug("Login started!")
        if not self.session and username.split("@")[1] in self.SMTPServers:
            server = self.SMTPServers.get(username.split("@")[1])
            self.session = smtplib.SMTP(server, self.port)

            if self.is_debug_on: 
                self.session.set_debuglevel(1)

            self.debug("Testing server start!")
            ehlo_response = self.session.ehlo()
            if b"STARTTLS" in ehlo_response[1]:
                self.debug("TLS is available!")
                self.session.starttls()
            self.debug("Testing server end!")
            
            self.session.login(username, password)
            self.debug(f"Successfully logged into {username}!")
            return True
        
        elif self.session: 
            raise ConnectionError("Close your previous session first before starting a new one!")
        
        elif username.split("@")[1] not in self.SMTPServers:
            raise ValueError("This email isn't supported unfortunately!")

    def log_out(self) -> bool:
        self.debug("Log out start!")

        if self.session:
            self.session.quit()
            self.session = None
            self.debug(f"Successfully logged out!")
            return True
        
        else:
            raise ConnectionError("Unable to log out, you weren't logged in!")

    def send_email(self, email: Email) -> bool:
        self.debug("Send email start!")

        if not email.msg["From"]:
            self.log_out()
            raise ValueError("You must set a sender email")
        
        if not email.msg["To"]:
            self.log_out()
            raise ValueError("You must set a receiver email")
        
        self.debug("Testing if connection is available!")
        if self.session.noop()[0] != 250:
            raise ConnectionError("Server is offline")
        self.debug("Connection is still available!")

        self.session.send_message(email.msg)
        self.debug(f'Sent an email from {email.msg["From"]} to {email.msg["To"]}')
        return True


