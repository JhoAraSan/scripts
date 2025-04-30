from tkinter import *
from tkinter import filedialog
import email
import pyperclip as clipboard

def open_mail():
    # Open a file dialog to select the email file
    mail_path=filedialog.askopenfilename(title="Select a mail file", filetypes=[("Email files", "*.eml")])
    if not mail_path:
        return
    with open(mail_path, 'r') as f:
        msg = email.message_from_file(f)
    clipboard.copy(msg) # Copy the email content to clipboard
    # Display a message to the user
    label=Label(window, text="Email copied to clipboard!")
    label.pack()
    label.after(3000, label.destroy) # Destroy the label after 3 seconds

window = Tk()
window.title("Email to Clipboard")

boton = Button(window, text="Open email", command=open_mail)
boton.pack()
window.geometry("300x200")
window.mainloop()