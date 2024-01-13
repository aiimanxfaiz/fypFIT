
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import sys

days = 9
periods = 5
recess_break_aft = 0 # recess after 3rd Period
section = None
butt_grid = []


period_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
day_names = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM' , '3PM' , '4PM']


def update_p(d, p, tree, parent):
    # print(section, d, p, str(sub.get()))

    try:
        if len(tree.selection()) > 1:
            messagebox.showerror("Bad Select", "Select one subject at a time!")
            parent.destroy()
            return
        row = tree.item(tree.selection()[0])['values']
        if row[0] == 'NULL' and row[1] == 'NULL':
            conn.execute(f"DELETE FROM SCHEDULE WHERE ID='{section+str((d*periods)+p)}'")
            conn.commit()
            update_table()
            parent.destroy()
            return

        conn.commit()
        print(row)
        conn.execute(f"REPLACE INTO SCHEDULE (ID, DAYID, PERIODID, SUBCODE, SECTION, FINI)\
            VALUES ('{section+str((d*periods)+p)}', {d}, {p}, '{row[1]}', '{section}', '{row[0]}')")
        conn.commit()
        update_table()

    except IndexError:
        messagebox.showerror("Bad Select", "Please select a subject from the list!")
        parent.destroy()
        return

    parent.destroy()



def process_button(d, p):
    print(d, p)
    add_p = tk.Tk()
    # add_p.geometry('200x500')

    # get subject code list from the database
    cursor = conn.execute("SELECT SUBCODE FROM SUBJECTS")
    subcode_li = [row[0] for row in cursor]
    subcode_li.insert(0, 'NULL')

    # Label10
    tk.Label(
        add_p,
        text='Select Subject',
        font=('Consolas', 12, 'bold')
    ).pack()

    tk.Label(
        add_p,
        text=f'Day: {day_names[d]}',
        font=('Consolas', 12)
    ).pack()

    tk.Label(
        add_p,
        text=f'Period: {p+1}',
        font=('Consolas', 12)
    ).pack()

    tree = ttk.Treeview(add_p)
    tree['columns'] = ('one', 'two')
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("one", width=70, stretch=tk.NO)
    tree.column("two", width=80, stretch=tk.NO)
    tree.heading('#0', text="")
    tree.heading('one', text="Faculty")
    tree.heading('two', text="Subject Code")
    
    cursor = conn.execute("SELECT FACULTY.INI, FACULTY.SUBCODE1, FACULTY.SUBCODE2, SUBJECTS.SUBCODE\
    FROM FACULTY, SUBJECTS\
    WHERE FACULTY.SUBCODE1=SUBJECTS.SUBCODE OR FACULTY.SUBCODE2=SUBJECTS.SUBCODE")
    for row in cursor:
        print(row)
        tree.insert(
            "",
            0,
            values=(row[0],row[-1])
        )
    tree.insert("", 0, value=('NULL', 'NULL'))
    tree.pack(pady=10, padx=30)

    tk.Button(
        add_p,
        text="OK",
        padx=15,
        command=lambda x=d, y=p, z=tree, d=add_p: update_p(x, y, z, d)
    ).pack(pady=20)

    add_p.mainloop()


def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table()


def update_table():
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{section}'")
            cursor = list(cursor)
            print(cursor)
            if len(cursor) != 0:
                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()
            

# connecting database
conn = sqlite3.connect(r'timetable.db')

# creating Tabe in the database
conn.execute('CREATE TABLE IF NOT EXISTS SCHEDULE\
(ID CHAR(10) NOT NULL PRIMARY KEY,\
DAYID INT NOT NULL,\
PERIODID INT NOT NULL,\
SUBCODE CHAR(10) NOT NULL,\
SECTION CHAR(5) NOT NULL,\
FINI CHAR(10) NOT NULL)')
# DAYID AND PERIODID ARE ZERO INDEXED


tt = tk.Tk()

tt.title('Scheduler')

# Create a label for the title
#title_label = Label(tt, bd=0, relief=GROOVE, font=("Algerian", 30, 'bold'), fg='white', height=1)
#title_label.pack(side=TOP, fill=X)

def set_background_image(window, image_path):
    # Open the image file using PIL
    img = Image.open(image_path)
    
    # Convert the image to a PhotoImage object
    img = ImageTk.PhotoImage(img)
    
    # Create a label widget to display the image and place it on the window
    background_label = tk.Label(window, image=img)
    background_label.img = img  # Store a reference to the image to prevent it from being garbage collected
    background_label.place(relwidth=1, relheight=1)  # Cover the entire window

set_background_image(tt, 'background_2.png')


def create_image_label(tt, bg_color="#ffffff"):
    # Load the image for the label
    image = Image.open('image_1.png')
    image = ImageTk.PhotoImage(image)

    # Create the image label and display the image at the top
    image_label = tk.Label(tt, image=image, bg=bg_color)
    image_label.image = image  # Store a reference to the image to prevent it from being garbage collected
    image_label.pack(side="top", expand="false")

    # Prevent the label from changing its size based on its content
    image_label.pack_propagate(0)

# Adjust bg_color based on your preferences (default is white)
create_image_label(tt, bg_color="#bbd2f1")

# Load and display the image on the Canvas
#image_image_2 = Image.open("image_1.png")
#image_2 = ImageTk.PhotoImage(image_image_2)

#canvas_border_height = 4  # Adjust the border height as needed
#canvas = Canvas(tt, width=150, height=50 + canvas_border_height,
#                highlightthickness=0)  # Adjust the width and height as needed
#canvas.create_image(0, canvas_border_height, anchor=NW, image=image_2)
#canvas.place(x=265, y=title_label.winfo_height() - canvas_border_height)  # Position the Canvas below the title label

#label_university = tk.Label(
#    text="Multimedia University",
#    font=("Inter ExtraLight", 16),
#    fg="black",
#    bg="#a0caf0"
#)
#label_university.place(x=155, y=10)

table = tk.Frame(tt)
table.pack()

first_half = tk.Frame(table)
first_half.pack(side='left')

recess_frame = tk.Frame(table)
recess_frame.pack(side='left')

second_half = tk.Frame(table)
second_half.pack(side='left')

for i in range(days):
    b = tk.Label(
        first_half,
        text=day_names[i],
        font=('Consolas', 12, 'bold'),
        width=9,
        height=2,
        bd=5,
        relief='flat'
    )
    b.grid(row=i+1, column=0)

for i in range(periods):
    if i < recess_break_aft:
        b = tk.Label(first_half)
        b.grid(row=0, column=i+1)
    else:
        b = tk.Label(second_half)
        b.grid(row=0, column=i)

    b.config(
        text=period_names[i],
        font=('Consolas', 12, 'bold'),
        width=9,
        height=1,
        bd=5,
        relief='flat'
    )

for i in range(days):
    b = []
    for j in range(periods):
        if j < recess_break_aft:
            bb = tk.Button(first_half)
            bb.grid(row=i+1, column=j+1)
        else:
            bb = tk.Button(second_half)
            bb.grid(row=i+1, column=j)

        bb.config(
            bg='white',
            text='Hello World!',
            font=('Consolas', 10),
            width=13,
            height=3,
            bd=5,
            relief='flat',
            wraplength=80,
            justify='center',
            command=lambda x=i, y=j: process_button(x, y)
        )
        b.append(bb)

    butt_grid.append(b)
    # print(b)
    b = []
sec_select_f = tk.Frame(tt, pady=15, padx=108)
sec_select_f.pack()

tk.Label(
    sec_select_f,
    text='Select section:  ',
    font=('Consolas', 12, 'bold')
).pack(side=tk.LEFT, padx=20)

cursor = conn.execute("SELECT DISTINCT SECTION FROM STUDENT")
sec_li = [row[0] for row in cursor]
# sec_li.insert(0, 'NULL')
print(sec_li)
combo1 = ttk.Combobox(
    sec_select_f,
    values=sec_li,
)
combo1.pack(side=tk.LEFT)
combo1.current(0)

b = tk.Button(
    sec_select_f,
    text="OK",
    font=('Consolas', 12, 'bold'),
    padx=10,
    command=select_sec
)
b.pack(side=tk.LEFT, padx=10)
b.invoke()


print(butt_grid[0][1], butt_grid[1][1])
update_table()

tt.mainloop()