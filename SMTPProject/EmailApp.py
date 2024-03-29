from .Email import Email
from .SMPTServer import SMTPServer
import tkinter as tk
from tkinter import filedialog

class EmailApp(tk.Frame):
    def __init__(self, master = None, ssl_encryption = True, debug = False):
        super().__init__(master)
        self.master = master
        self.master.title("Email App")
        self.master.geometry("500x425")
        self.server = SMTPServer(ssl_encryption = ssl_encryption, debug = debug)

        # From/Sender
        self.sender_label = tk.Label(self.master, text="From:")
        self.sender_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.sender_entry = tk.Entry(self.master, width=50)
        self.sender_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.password_entry = tk.Entry(self.master, width=50, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # To/Receiver
        self.receiver_label = tk.Label(self.master, text="To:")
        self.receiver_label.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.receiver_entry = tk.Entry(self.master, width=50)
        self.receiver_entry.grid(row=2, column=1, padx=5, pady=5)

        # Copy
        self.cc_label = tk.Label(self.master, text="Cc:")
        self.cc_label.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.cc_entry = tk.Entry(self.master, width=50)
        self.cc_entry.grid(row=3, column=1, padx=5, pady=5)

        # Blind copy
        self.bcc_label = tk.Label(self.master, text="Bcc:")
        self.bcc_label.grid(row=4, column=0, padx=5, pady=5, sticky="W")
        self.bcc_entry = tk.Entry(self.master, width=50)
        self.bcc_entry.grid(row=4, column=1, padx=5, pady=5)

        # Subject
        self.subject_label = tk.Label(self.master, text="Subject:")
        self.subject_label.grid(row=5, column=0, padx=5, pady=5, sticky="W")
        self.subject_entry = tk.Entry(self.master, width=50)
        self.subject_entry.grid(row=5, column=1, padx=5, pady=5)

        # Body
        self.body_label = tk.Label(self.master, text="Body:")
        self.body_label.grid(row=6, column=0, padx=5, pady=5, sticky="W")
        self.body_entry = tk.Text(self.master, width=50, height=10)
        self.body_entry.grid(row=6, column=1, padx=5, pady=5)

        # Attachments
        self.attachments_label = tk.Label(self.master, text="Attachments:")
        self.attachments_label.grid(row=7, column=0, padx=5, pady=5, sticky="W")
        self.attachments_entry = tk.Entry(self.master, width=50)
        self.attachments_entry.grid(row=7, column=1, padx=5, pady=5)

        # Browse button
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_files)
        self.browse_button.grid(row=8, column=0, padx=5, pady=5, sticky="W")

        # Send button
        self.send_button = tk.Button(self.master, text="Send", command=self.send_email)
        self.send_button.grid(row=8, column=1, padx=5, pady=5)

    def browse_files(self):
        file_path = filedialog.askopenfilename() + '; '
        self.attachments_entry.insert(0, file_path)

    def send_email(self):
        self.server.log_in(self.sender_entry.get(), self.password_entry.get())

        # Put all entries in an email object
        email = Email()
        email.set_sender(self.sender_entry.get())
        email.set_subject(self.subject_entry.get())
        email.set_multiple_receivers(self.receiver_entry.get().split(';'))
        email.set_multiple_cc(self.cc_entry.get().split(';'))
        email.set_multiple_bcc(self.bcc_entry.get().split(';'))
        email.set_body(self.body_entry.get("1.0", tk.END))

        # Last entry in attachments is always empty -> loop over everything but last
        attachment_files = self.attachments_entry.get().split('; ')[:-1]
        if attachment_files:
            for attachment in attachment_files:
                email.add_attachment(attachment)

        self.server.send_email(email)
        self.server.log_out()
        self.reset_fields()

        # Confirmation popup
        popup = tk.Toplevel(self.master)
        popup.title("Email Sent")
        popup.geometry("200x100")
        message_label = tk.Label(popup, text="Email sent successfully!")
        message_label.pack(pady=20)
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()

    def reset_fields(self):
        # Not resetting sender and password -> will probably always be the same -> faster workflow
        # self.sender_entry.delete(0, tk.END)
        # self.password_entry.delete(0, tk.END)
        self.receiver_entry.delete(0, tk.END)
        self.cc_entry.delete(0, tk.END)
        self.bcc_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.body_entry.delete("1.0", tk.END)
        self.attachments_entry.delete(0, tk.END)

