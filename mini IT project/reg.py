import tkinter as tk
import sqlite3
from tkinter import messagebox
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from LoginPage import * 

class RegistrationForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect("timetable.db")
        self.mycursor = self.db.cursor()

        self.title("Student Registration")
        self.geometry("400x300")

        # Initialize student_sid attribute
        self.student_sid = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Full Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Button(self, text="Register", command=self.register).pack()

    def send_recovery_email(self, username, email, password):
        # Configure your email server details
        smtp_server = 'your_smtp_server'
        smtp_port = 587
        smtp_username = 'your_email@gmail.com'
        smtp_password = 'your_email_password'

        # Create a connection to the SMTP server
        server = smtplib.SMTP(host=smtp_server, port=smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Compose the email
        subject = 'Password Recovery'
        body = f'Hello {username},\n\nYour password is: {password}\n\nRegards,\nYour School Name'

        message = MIMEMultipart()
        message['From'] = smtp_username
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(smtp_username, email, message.as_string())

        # Close the connection
        server.quit()

    def register(self):
        SID = str(122110)+self.username_entry.get()
        user = SID
        PASSW = self.password_entry.get()
        email = self.email_entry.get()
        name = self.name_entry.get()

        try:
            # Generate TOTP secret key
            totp_secret = pyotp.random_base32()

            # Insert user data into the database
            sql = "INSERT INTO STUDENT (SID, PASSW, email, name) VALUES (?, ?, ?, ?)"
            values = (SID, PASSW, email, name)
            self.mycursor.execute(sql, values)
            self.db.commit()

            messagebox.showinfo("Success", "Registration successful!")
            messagebox.showinfo("SAVE THIS",'Your student ID Is '+ SID )

            # Open the login form after successful registration
            self.withdraw()  # Hide the registration form
            #login_form = LoginForm()
            #login_form.protocol("WM_DELETE_WINDOW", self.deiconify)  # Handle window close
            #login_form.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
        
if __name__ == "__main__":
    registration_form = RegistrationForm()
    registration_form.mainloop()
