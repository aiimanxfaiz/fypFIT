import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import sqlite3
from tkinter import PhotoImage, Image
from subprocess import call
from windows import timetable_stud
from LoginPage import *
import sys
from student_list_section import *



class Homepage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = sqlite3.connect("mmu.db")
        self.mycursor = self.db.cursor()

        background = '#FFFFFF'
        framebg = '#EDEDED'
        framefg = '#06283D'

        self.title("Multimedia University")
        self.geometry("1366x768")
        self.config(bg=background)
        self.homescreen()
        

    def homescreen(self):
        # top frames
        Label(self, width=1, height=3, bg='#a0caf0', anchor='e').pack(side=TOP, fill=X)

        # Bottom frames
        Label(self, width=1, height=2, bg='#bcbcbc', anchor='e').pack(side=BOTTOM, fill=X)

        # Add background image
        self.image_background = Image.open('mmu.png')
        self.image_2 = ImageTk.PhotoImage(self.image_background)
        self.image_2_label = Label(self, image=self.image_2,width=1366,height=768)
        self.image_2_label.place(x=0,y=50)

        # Add MMU to the top left corner 
        image_MMU = Image.open('image_1.png')
        image_1 = ImageTk.PhotoImage(image_MMU)
        image_1_label = Label(self, width=0, height=30, image=image_1, bg='#a0caf0', anchor='w')
        image_1_label.place(x=20, y=5)

        # Create non-clickable label
        label_university = tk.Label(
            text="Multimedia University",
            font=("Inter ExtraLight", 16),
            fg="black",
            bg="#a0caf0"
        )
        label_university.place(x=182, y=10)


        def clickable_label(event):
            clicked_label_text = event.widget["text"]
            if clicked_label_text == "Course Offered":
                self.withdraw()
                call(['python', 'Course_Browse.py'])
            if clicked_label_text == "Student List":

                conn = sqlite3.connect(r'timetable.db')

                if "--username" in sys.argv:
                    username_index = sys.argv.index("--username") + 1
                    username = sys.argv[username_index]
                else:
                    username = "1221104865"
        
                # Create an instance of StudentList and call fetch_data
                student_list_instance = StudentList(username)
                student_list_instance.fetch_data()

            if clicked_label_text == "My Weekly Schedule":
                self.schedule()
            if clicked_label_text == "Enrollment/Swap/Drop Classes":
                return
            if clicked_label_text == "Log Out":
                self.log_out()
                
            
        Label(self, text='Student List',bg='#a0caf0', font=('TkDefaultFont', 10 )).place(x=740, y=15 )
        Label(self, text='Course Offered',bg='#a0caf0', font=('TkDefaultFont', 10 )).place(x=850, y=15 )
        Label(self, text='My Weekly Schedule',bg='#a0caf0', font=('TkDefaultFont', 10 )).place(x=980, y=15 )
        Label(self, text='Enrollment/Swap/Drop Classes',bg='#a0caf0', font=('TkDefaultFont', 10 )).place(x=1130, y=15 )
        Label(self, text='Log Out',bg='white', font=('TkDefaultFont', 10 )).place(x=1300, y=60 )
        self.bind("<Button-1>", clickable_label)

        self.mainloop()

    
    def schedule(self):
        conn = sqlite3.connect(r'timetable.db')

        if "--username" in sys.argv:
            username_index = sys.argv.index("--username") + 1
            username = sys.argv[username_index]
        else:
            username = "1221104865"

        if hasattr(self, 'nw') and self.nw and self.nw.winfo_exists():
            self.nw.deiconify()
            self.nw.lift()
        else:
            cursor = conn.execute(f"SELECT SID, SECTION, NAME, ROLL FROM STUDENT WHERE SID='{username}'")
            cursor = list(cursor)

            self.nw = tk.Toplevel(self)
            self.nw.protocol("WM_DELETE_WINDOW", self.hide_window)
            
            tk.Label(
                self.nw,
                text=f'{cursor[0][2]}\tSection: {cursor[0][1]}\tStudent ID: {cursor[0][0]}',
                font=('Consolas', 12, 'italic'),
                bg="#a0caf0"
            ).pack()

            self.nw.state('zoomed')
            timetable_stud.student_tt_frame_v2(self.nw, cursor[0][1])

    def hide_window(self):
        if hasattr(self, 'nw') and self.nw and self.nw.winfo_exists():
            self.nw.withdraw()

    def log_out(self):
        self.destroy()
        if hasattr(self, 'nw') and self.nw:
            try:
                if self.nw.winfo_exists():
                    self.nw.destroy()
            except tk.TclError:
               pass
        call(['python', 'LoginPage.py'])


if __name__ == "__main__":
    app = Homepage()
    app.mainloop()