from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Email:
    def __init__(self) -> None:
        self.msg = MIMEMultipart()

    def set_sender(self, email: str) -> None:
        self.msg["From"] = email

    def set_receiver(self, email: str) -> None:
        self.msg["To"] = email

    def set_multiple_receivers(self, emails: list[str]) -> None:
        self.msg["To"] = ', '.join(emails)

    def set_subject(self, subject: str) -> None:
        self.msg["Subject"] = subject

    def set_cc(self, email: str) -> None:
        self.msg["Cc"] = email

    def set_multiple_cc(self, emails: list[str]) -> None:
        self.msg["Cc"] = ', '.join(emails)

    def set_bcc(self, email: str) -> None:
        self.msg["Bcc"] = email

    def set_multiple_bcc(self, emails: list[str]) -> None:
        self.msg["Bcc"] = ', '.join(emails)

    def set_body(self, body: str) -> None:
        self.msg.attach(MIMEText(body))

    def add_attachment(self, filename: str) -> None:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            self.msg.attach(part)

    def add_multiple_attachments(self, filenames: list[str]) -> None:
        for filename in filenames:
            self.add_attachment(filename)

    def add_image(self, filename: str) -> None:
        with open(filename, 'rb') as f:
            img_data = f.read()
            image = MIMEImage(img_data, name=filename)
            self.msg.attach(image)

    def add_multiple_images(self, filenames: list[str]) -> None:
        for filename in filenames:
            self.add_image(filename)
