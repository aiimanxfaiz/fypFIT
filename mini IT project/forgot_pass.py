import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from PIL import Image, ImageTk

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect("timetable.db")
        self.mycursor = self.db.cursor()

        self.title("Student Login")
        self.geometry("1366x768")
        self.resizable(False, False)

        bg_image = Image.open("background_2.png")
        self.bg_image = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(width=1366, height=768)

        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="white")  # Set TFrame background color
        self.style.configure("TLabel", background='white', foreground='black', font=('Helvetica', 12))  # Set TLabel font style
        self.style.configure("TEntry", fieldbackground="#f2f2f2")  # Light grey entry field
        self.style.configure("TButton", background="#66b3ff", foreground="white")  # Light blue button


class PasswordRecoveryForm(tk.Tk):
    def __init__(self, parent, cursor, db):
        super().__init__()

        self.parent = parent
        self.db = db
        self.mycursor = cursor

        self.title("Password Recovery")
        self.geometry("400x200")

        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="white")  # Set TFrame background color
        self.style.configure("TLabel", font=('Helvetica', 12))  # Set TLabel font style
        self.style.configure("TEntry", fieldbackground="#f2f2f2")  # Light grey entry field
        self.style.configure("TButton", background="#66b3ff", foreground="white")  # Light blue button

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, style="TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Enter your username:").grid(row=0, column=0, pady=10, padx=10, sticky='w')
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10, sticky='w')

        ttk.Button(frame, text="Recover Password", command=self.recover_password).grid(row=1, column=0, columnspan=2, pady=15)

    def recover_password(self):
        username = self.username_entry.get()

        try:
            sql = "SELECT PASSW FROM STUDENT WHERE SID = ?"
            values = (username,)
            self.mycursor.execute(sql, values)
            result = self.mycursor.fetchone()

            if result:
                password = result[0]
                tk.messagebox.showinfo("Password Recovery", f"Your password is: {password}")
                self.destroy()  # Close the recovery form after displaying the password
            else:
                tk.messagebox.showerror("Error", "Username not found.")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Password recovery failed: {e}")


if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()
