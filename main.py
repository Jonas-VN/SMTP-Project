from SMTPProject import EmailApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    email_app = EmailApp(root, debug=True)
    email_app.mainloop()