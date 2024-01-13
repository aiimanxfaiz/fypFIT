from tkinter import *
import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import *
from PIL import ImageTk, Image
from reg import *
from subprocess import Popen


class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()


        self.db = sqlite3.connect("timetable.db")
        self.mycursor = self.db.cursor()

        self.title("Student Login")
        self.geometry("1366x768")
        self.resizable(False, False)

        # Load images and keep references as class attributes
        self.bg_image = Image.open("background_2.png")
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
        self.login_image = Image.open("background_3.png")
        self.login_image_tk = ImageTk.PhotoImage(self.login_image)
        self.logo_image = Image.open("image_1.png")
        self.logo_image_tk = ImageTk.PhotoImage(self.logo_image)

        bg_label = tk.Label(self, image=self.bg_image_tk)
        bg_label.place(width=1366, height=768)

        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background='white', foreground='black', font=('Helvetica', 12))
        self.style.configure("TEntry", fieldbackground="#f2f2f2")
        self.style.configure("TButton", background="#66b3ff", foreground="black")

        self.create_widgets()

    
    def create_widgets(self):
        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=426, height=560)

        login_label = tk.Label(self, image=self.login_image_tk)
        login_label.place(width=426, height=190, x=470, y=80)

        logo_label = tk.Label(self, image=self.logo_image_tk)
        logo_label.place(x=620, y=150)

        ttk.Label(frame, text="Sign In", font=('TkDefaultFont', 16)).place(x=180, y=190)

        ttk.Label(frame, text="Student ID:").place(x=40, y=220)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.place(x=40, y=250, width=350, height=25)

        ttk.Label(frame, text="Password:").place(x=40, y=290)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.place(x=40, y=320, width=350, height=25)

        ttk.Button(frame, text="Login", command=self.login, style="TButton").place(x=160, y=360, width=100)

        ttk.Button(frame, text="Recover Password", command=self.open_recovery_form, style="TButton").place(x=300, y=390)

        ttk.Label(frame, text="or", font=('TkDefaultFont', 13)).place(x=200, y=410)

        ttk.Label(frame, text="Didn't have an acc2ount?", font=('TkDefaultFont', 9)).place(x=40, y=440)

        ttk.Button(frame, text="Create your Account", command=self.open_registration_form, style="TButton").place(x=140, y=475, width=140, height=25)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            sql = "SELECT * FROM STUDENT WHERE SID = ? and PASSW = ?"
            values = (username, password)
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()

            if username == "admin" and password == "admin":
                self.withdraw()
                Popen(['python', 'windows/admin_screen.py'])
                self.login_info = {'user_type': 'Admin', 'username': username}

            elif result:
                self.withdraw()
                # Pass username to the HomePage2.py file
                Popen(['python', 'HomePage2.py', '--username', username])
                # Store login information in self.login_info
                self.login_info = {'username': username}
                
            else:
                tk.messagebox.showerror("Error", "Incorrect username or password")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Login failed: {e}")
   

    def open_registration_form(self):
        registration_form = RegistrationForm()
        registration_form.mainloop()

    def open_recovery_form(self):
        if not hasattr(self, 'recovery_form') or not self.recovery_form.winfo_exists():
            self.withdraw()  # Hide the main window
            self.recovery_form = PasswordRecoveryForm(self, self.mycursor, self.db)
            self.recovery_form.protocol("WM_DELETE_WINDOW", self.on_recovery_form_close)
            self.recovery_form.mainloop()

    def on_recovery_form_close(self):
        self.recovery_form.destroy()
        self.deiconify()  # Show the main window again
        self.recovery_form = None

class PasswordRecoveryForm(tk.Tk):
    def __init__(self, parent, cursor, db):
        super().__init__()

        self.parent = parent
        self.db = db
        self.mycursor = cursor

        self.title("Password Recovery")
        self.geometry("400x200")

        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", font=('Helvetica', 12))
        self.style.configure("TEntry", fieldbackground="#f2f2f2")
        self.style.configure("TButton", background="#66b3ff", foreground="black")

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Enter your email:").grid(row=0, column=0, pady=10, padx=10, sticky='w')
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        # Add the button for submitting the email
        ttk.Button(frame, text="Submit", command=self.recover_password).grid(row=1, column=0, columnspan=2, pady=15)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Handle window closure by destroying the window
        self.destroy()
        

    def recover_password(self):
        email = self.email_entry.get()

        # Retrieve the user's password from the database
        password = self.retrieve_password(email)

        if password:
            # Send the recovery email
            self.send_recovery_email(email, password)
        else:
            tk.messagebox.showerror("Error", "Email not found")

    

    def retrieve_password(self, email):
        try:
            # Retrieve the user's password from the database based on their email
            sql_retrieve_password = "SELECT password FROM student_reg WHERE email = ?"
            values_retrieve_password = (email,)
            self.mycursor.execute(sql_retrieve_password, values_retrieve_password)
            result_retrieve_password = self.mycursor.fetchone()

            if result_retrieve_password:
                return result_retrieve_password[0]  # Return the user's password

            return None  # Email not found

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error retrieving password: {e}")

    def send_recovery_email(self, email, password):
        # Configure your email server details
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'nrrnaylis@gmail.com'
        smtp_password = 'dnml bvpa oljq apsq'

        # Create the message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = 'Password Recovery'

        # Attach the password to the message
        body = f'Your password is: {password}\n\nPlease keep it secure.'
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Connect to the SMTP server and send the email
            with smtplib.SMTP(host=smtp_server, port=smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            tk.messagebox.showinfo("Email Sent", "An email has been sent to your address with your password.")
            self.destroy()

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error sending email: {e}")

if __name__ == "__main__":
    try:
        login_form = LoginForm()
        login_form.mainloop()

        # After the mainloop, retrieve and print login information
        login_info = login_form.get_login_info()
        if login_info:
            print("Login Information:", login_info)
        else:
            print("Login not successful.")

    except Exception as e:
        print(f"An error occurred: {e}")
