import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import sqlite3

class StudentList(tk.Tk):
    def __init__(self, username):
        super().__init__()

        self.username = username
        
        self.title("Student List")
        self.geometry("1366x768+0+0")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1366
        window_height = 768
        x_position = (screen_width - 1366) // 2
        y_position = (screen_height - 768) // 2

        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        #================================Logo MMU=========================================

        # Title label with borderwidth set to 0
        title = Label(self, text="Student List", bd=0, relief=GROOVE, font=("Algerian", 30, 'bold'),
                      bg='#a0caf0', fg='white', height=1)
        title.pack(side=TOP, fill=X)

        # Load and display the image on the Canvas
        image_image_2 = Image.open("image_1.png")
        self.image_2 = ImageTk.PhotoImage(image_image_2)

        # Create a Canvas widget with a border (highlightthickness)
        canvas_border_height = 4  # Adjust the border height as needed
        canvas = Canvas(self, width=150, height=50 + canvas_border_height,
                        highlightthickness=0, bg='#a0caf0')  # Adjust the width and height as needed
        canvas.create_image(0, canvas_border_height, anchor=NW, image=self.image_2)
        canvas.place(x=0, y=title.winfo_height() - canvas_border_height)  # Position the Canvas below the title label
            
#================================Variables=========================================
        self.SID_var = StringVar()
        self.name_var = StringVar()
        self.section_var = StringVar()
        self.rcourse_var = StringVar()
        self.tri_var = StringVar()
        self.email_var = StringVar()
        

        self.pay_month_var = StringVar()
        self.pay_amount_var = StringVar()

    
        self.search_by = StringVar()
        self.search_txt = StringVar()


        detail_frame = Frame(self,bd=4,relief=RIDGE,bg='light blue')
        detail_frame.place(x=30,y=80,width=1300,height=645)

        lbl_search = Label(detail_frame,text="Search By",bg="light blue",fg="black",font=("times new roman",16,'bold'))
        lbl_search.grid(row=0,column=0,pady=10,padx=20,sticky='w')

  
        combo_search = ttk.Combobox(detail_frame,width=14,textvariable=self.search_by,font=("times new roman",12,'bold'),state='readonly')
        combo_search['values']=("Student ID","Name","Section","Email" )
        combo_search.grid(row=0,column=1,pady=10,padx=20)

        txt_search = Entry(detail_frame,width=30,textvariable=self.search_txt,font=('times new roman',14),bd=2,relief=GROOVE)
        txt_search.grid(row=0,column=2,pady=10,padx=20,sticky='w')

        searchbtn = Button(detail_frame,text="Search",width=10,command=self.search_data).grid(row=0,column=3,padx=10,pady=10)
        showallbtn = Button(detail_frame,text="Show All",width=10,command=self.fetch_data).grid(row=0,column=4,padx=10,pady=10)

#==================================Table Frame==============================
        table_frame = Frame(detail_frame,bd=2,relief=RIDGE,bg='light blue')
        table_frame.place(x=10,y=80,width=1273,height=540)

        scroll_x = Scrollbar(table_frame,orient="horizontal")
        scroll_y = Scrollbar(table_frame,orient="vertical")
        self.student_table = ttk.Treeview(table_frame,columns=("SID","name","section","rcourse","tri", 'email'),
                                                              xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set) 
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        self.student_table.heading("SID",text="Student ID")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("section",text="Section")
        self.student_table.heading("rcourse",text="Registered Course")
        self.student_table.heading("tri",text="Trimester")
        self.student_table.heading("email",text="Email")

        self.student_table['show']='headings'

        self.student_table.column("SID",width=80)
        self.student_table.column("name",width=200)
        self.student_table.column("section",width=140)
        self.student_table.column("rcourse",width=140)
        self.student_table.column("tri",width=140)
        self.student_table.column("email",width=140)
        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()

#================================Popularity Button =========================================

        sort_by_popularity_btn = Button(detail_frame, text="Sort by Popularity", width=15, command=self.sort_by_popularity)
        sort_by_popularity_btn.grid(row=0, column=5, padx=10, pady=10)

    def sort_by_popularity(self):
        conn = sqlite3.connect("timetable.db")
        cur = conn.cursor()

        # Fetch data sorted by the popularity of the sections
        cur.execute("""
            SELECT "Section", COUNT(*) AS popularity
            FROM student
            GROUP BY "Section"
            ORDER BY popularity DESC
        """)
        rows = cur.fetchall()

        if len(rows) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for index, row in enumerate(rows, start=1):
                section_name = row[0]
                popularity = row[1]
                section_display = f"{section_name} ({popularity} student)"
                self.student_table.insert("", END, values=(index, "", section_display))
            conn.commit()        
        else:
            messagebox.showerror("Error", "No records found")

        conn.close()

    def add_student(self):

        if self.SID_var.get()=="" or self.name_var.get()=="" or self.section_var.get()=="":
            messagebox.showerror("Error","All fields are required!")
        else:
            conn=sqlite3.connect("timetable.db")
            cur=conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS student(SID integer,name TEXT, section TEXT,rcourse TEXT,
                            tri TEXT)""")

            self.set_data()
            cur.execute("insert into student values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
                                                                        int(self.SID_var.get()),
                                                                        self.name_var.get(),
                                                                        self.section_var.get(),
                                                                        self.rcourse_var.get(),
                                                                        self.tri.get(), self.email_var.get()))
                                                                                                                                                             
            conn.commit()
            self.fetch_data()
            self.clear()
            conn.close()
            messagebox.showinfo("Success","Record has been inserted successfully.")
            
    def fetch_data(self):
        conn = sqlite3.connect("timetable.db")
        cur = conn.cursor()

        # Fetch the section for the provided username
        cur.execute("SELECT SECTION FROM STUDENT WHERE SID = ?", (self.username,))
        section_result = cur.fetchone()

        if section_result:
            # Get the section value from the result
            section_value = section_result[0]

            # Print the values being used for the query
            print("Section:", section_value)
            print("Username:", self.username)

            cur.execute("SELECT * FROM STUDENT WHERE SECTION = ?", (section_value,))
            rows = cur.fetchall()

            if len(rows) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in rows:
                    # Extract data from each column in the database
                    SID = row[0]
                    name = row[2]
                    section = row[4]
                    email = row[5]
                    trimester = row[6]
                    registered_course = row[7]

                    # Insert values into the Treeview with each column specified
                    self.student_table.insert("", END, values=(SID, name, section, registered_course, trimester, email))
                conn.commit()

        conn.close()


    def clear(self):
        self.SID_var.set("")
        self.name_var.set("")
        self.section_var.set("")
        self.rcourse_var.set("")
        self.tri.set("")
        self.pay_month_var.set("")
        self.pay_amount_var.set("")
        
    def get_cursor(self, event):
        cursor_row = self.student_table.focus()
        contents = self.student_table.item(cursor_row)
        row = contents['values']

        self.SID_var.set(row[0])
        self.name_var.set(row[1])
        self.section_var.set(row[2])
        self.rcourse_var.set(row[3])
        self.tri_var.set(row[4])
        self.email_var.set(row[5])

    def search_data(self):
        # ==================================for sqlite3==================
        conn = sqlite3.connect("timetable.db")
        cur = conn.cursor()
        search_column = str(self.search_by.get())

        if search_column == "Student ID":
            # Use 'SID' for searching by student ID
            search_query = 'SELECT * FROM student WHERE SID = ?'
        else:
            # For other columns, use 'LIKE' with wildcards
            search_query = f'SELECT * FROM student WHERE "{search_column}" LIKE ?'

        cur.execute(search_query, ('%' + str(self.search_txt.get()) + '%',))

        rows = cur.fetchall()
        if len(rows) != 0:
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                # Extract data from each column in the database
                SID = row[0]
                name = row[2]
                section = row[4]
                email = row[5]
                trimester = row[6]
                registered_course = row[7]

                # Insert values into the Treeview with each column specified
                self.student_table.insert("", END, values=(SID, name, section, registered_course, trimester, email))
            conn.commit()
        else:
            messagebox.showerror("Error", "Record not found")
        conn.close()

if __name__ == "__main__":
    app = StudentList("1221104408")
    app.mainloop()
