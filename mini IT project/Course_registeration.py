import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import sqlite3
from subprocess import call
from tkinter import *

class CourseRegister(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect("timetable.db")
        self.mycursor = self.db.cursor()

        self.title("Course Registration")
        self.geometry("600x400")

        self.style = ttk.Style(self)
        self.style.configure("TButton", background="#66b3ff", foreground="black")

        self.id = None  # Declare id as an instance variable

        self.create_widgets()

    def schedule(self):
        call(['python', 'windows/timetable_stud.py'])

    def create_widgets(self):
        self.clicked = StringVar()
        self.clicked.set("Select Section")
        Select_combobox = ttk.Combobox(self, textvariable=self.clicked, values=['TT1L', 'TT2L'])
        Select_combobox.place(x=240, y=160, width=123)

        b1 = tk.Button(text='View the section schedule', font=('Consolas', 9), command=self.schedule)
        b1.place(x=210, y=100)

        label1 = tk.Label(self, text='(Select on which section you would like to enroll to)', font=('TkDefaultFont', 8))
        label1.place(x=180, y=190)

        label2 = tk.Label(self, text='Choose Your Course', font=('TkDefaultFont', 15))
        label2.place(x=210, y=40)

        label3 = tk.Label(self, text='(Enter your student id)', font=('TkDefaultFont', 8))
        label3.place(x=240, y=255)

        b2 = tk.Button(self, text='Enroll', command=self.enroll)
        b2.place(x=278, y=290)

        self.username_entry = tk.Entry(self, width=20)
        self.username_entry.place(x=240, y=230)
        #course_registeration_page = Button(self, text = 'Register Course', command= self.Homepage, width= 20, height = 2, bg='#FF290B')
        #course_registeration_page.place(x=200, y = 300) 

    def enroll(self):
       selected_section = self.clicked.get()
       self.id = self.username_entry.get()

       try:
            # Check the number of registered students for the selected section
            count_query = "SELECT COUNT(*) FROM STUDENT WHERE SECTION = ?"
            self.mycursor.execute(count_query, (selected_section,))
            count = self.mycursor.fetchone()[0]

            if count >= 5:
                messagebox.showinfo("Enrollment", f"Sorry, the section {selected_section} is full. Please choose another section.")
            else:
                # Update the SECTION for the specific studenat
                update_query = "UPDATE STUDENT SET SECTION = ? WHERE SID = ?"
                self.mycursor.execute(update_query, (selected_section, self.id))

                self.db.commit()
                messagebox.showinfo("Enrollment", f"You have successfully enrolled in {selected_section}.")
                
       except Exception as e:
            messagebox.showerror("Error", f"Error during enrollment: {str(e)}")

    

if __name__ == "__main__":
    registration_Course = CourseRegister()
    registration_Course.mainloop()
