import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

days = 8
periods = 5
recess_break_aft = 3 # recess after 3rd Period
section = None
butt_grid = []


period_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']
day_names = ['8AM', '9AM', '10AM', '11AM', '12PM', '1PM', '2PM' , '3PM' , '4PM']



def select_sec():
    global section
    section = str(combo1.get())
    print(section)
    update_table(section)



def update_table(sec):
    for i in range(days):
        for j in range(periods):
            cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE DAYID={i} AND PERIODID={j} AND SECTION='{sec}'")
            cursor = list(cursor)
            print(cursor)
            
            butt_grid[i][j]['bg'] = 'white'
            if len(cursor) != 0:
                subcode = cursor[0][0]
                cur1 = conn.execute(F"SELECT SUBTYPE FROM SUBJECTS WHERE SUBCODE='{subcode}'")
                cur1 = list(cur1)
                subtype = cur1[0][0]
                butt_grid[i][j]['fg'] = 'white'
                if subtype == 'T':
                    butt_grid[i][j]['bg'] = 'green'
                elif subtype == 'L':
                    butt_grid[i][j]['bg'] = 'blue'

                butt_grid[i][j]['text'] = str(cursor[0][0]) + '\n' + str(cursor[0][1])
                butt_grid[i][j].update()
                print(i, j, cursor[0][0])
            else:
                butt_grid[i][j]['fg'] = 'black'
                butt_grid[i][j]['text'] = "No Class"
                butt_grid[i][j].update()



def process_button(d, p, sec):
    details = tk.Tk()
    cursor = conn.execute(f"SELECT SUBCODE, FINI FROM SCHEDULE\
                WHERE ID='{section+str((d*periods)+p)}'")
    cursor = list(cursor)
    if len(cursor) != 0:
        subcode = str(cursor[0][0]) 
        fini =  str(cursor[0][1])

        cur1 = conn.execute(f"SELECT SUBNAME, SUBTYPE FROM SUBJECTS\
            WHERE SUBCODE='{subcode}'")
        cur1 = list(cur1)
        subname = str(cur1[0][0])
        subtype = str(cur1[0][1])

        cur2 = conn.execute(f"SELECT NAME, EMAIL FROM FACULTY\
            WHERE INI='{fini}'")
        cur2 = list(cur2)
        fname = str(cur2[0][0])
        femail = str(cur2[0][1]) 

        if subtype == 'T':
            subtype = 'Theory'
        elif subtype == 'P':
            subtype = 'Practical'

    else:
        subcode = fini = subname = subtype = fname = femail = 'None'

    print(subcode, fini, subname, subtype, fname, femail)
    tk.Label(details, text='Class Details', font=('Consolas', 15, 'bold')).pack(pady=15)
    tk.Label(details, text='Day: '+day_names[d], font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Period: '+str(p+1), font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Code: '+subcode, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subect Name: '+subname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Subject Type: '+subtype, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Initials: '+fini, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Name: '+fname, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)
    tk.Label(details, text='Faculty Email: '+femail, font=('Consolas'), anchor="w").pack(expand=1, fill=tk.X, padx=20)

    tk.Button(
        details,
        text="OK",
        font=('Consolas'),
        width=10,
        command=details.destroy
    ).pack(pady=10)

    details.mainloop()



def student_tt_frame(tt, sec):

    tt.state('zoomed')
    
    global butt_grid
    global section
    section = sec

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

    second_half = tk.Frame(table)
    second_half.pack(side='left')

    legend_f = tk.Frame(pady=10, padx=142)
    legend_f.pack()
    tk.Label(
        legend_f,
        text='Legend: ',
        font=('Consolas', 10, 'italic')
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Tutorial Classes',
        bg='green',
        fg='white',
        relief='flat',
        font=('Consolas', 10, 'italic'),
        height=0,
        bd=0
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Lecture Classes',
        bg='blue',
        fg='white',
        relief='flat',
        font=('Consolas', 10, 'italic'),
        height=0,
        bd=0
    ).pack(side=tk.LEFT)

    for i in range(days):
        b = tk.Label(
            first_half,
            text=day_names[i],
            font=('Consolas', 12, 'bold'),
            width=9,
            height=2,
            bd=0,
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
            bd=0,
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
                text='Hello World!',
                font=('Consolas', 10),
                width=13,
                height=3,
                bd=0,
                relief='flat',
                wraplength=80,
                justify='center',
                command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(sec)
    
def student_tt_frame_v2(tt, sec):
    title_lab = tk.Label(
        tt,
        text='T  I  M  E  T  A  B  L  E',
        font=('Consolas', 20, 'bold'),
        pady=5,
        fg='white',
        bg='#a0caf0'
    )
    title_lab.pack()

    legend_f = tk.Frame(tt, bg='#a0caf0')
    legend_f.pack()
    tk.Label(
        legend_f,
        text='Legend: ',
        font=('Consolas', 10, 'italic'),
        bg='#a0caf0'
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Lecture Classes',
        bg='green',
        fg='white',
        relief='flat',
        font=('Consolas', 10, 'italic'),
        height=2,
    ).pack(side=tk.LEFT)

    tk.Label(
        legend_f,
        text='Tutorial Classes',
        bg='blue',
        fg='white',
        relief='flat',
        font=('Consolas', 10, 'italic'),
        height=2,
    ).pack(side=tk.LEFT)
    
    global butt_grid
    global section
    section = sec

    table = tk.Frame(tt)
    table.pack()

    first_half = tk.Frame(table)
    first_half.pack(side='left')

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
                text='Hello World!',
                font=('Consolas', 10),
                width=13,
                height=3,
                bd=5,
                relief='flat',
                wraplength=80,
                justify='center',
                command=lambda x=i, y=j, z=sec: process_button(x, y, z)
            )
            b.append(bb)

        butt_grid.append(b)
        # print(b)
        b = []

    print(butt_grid[0][1], butt_grid[1][1])
    update_table(sec)


    tt.configure(bg='#a0caf0')

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

def set_background_image(window, image_path):
    # Open the image file using PIL
    img = Image.open('background_2.png')
    
    # Convert the image to a PhotoImage object
    img = ImageTk.PhotoImage(img)
    
    # Create a label widget to display the image and place it on the window
    background_label = tk.Label(window, image=img)
    background_label.img = img  # Store a reference to the image to prevent it from being garbage collected
    background_label.place(relwidth=1, relheight=1)  # Cover the entire window


conn = sqlite3.connect(r'timetable.db')

if __name__ == "__main__":
    # connecting database
    conn = sqlite3.connect(r'timetable.db')
    
    tt = tk.Tk()
    tt.title('Student Timetable')

    # Set the background image (replace 'background.png' with your image file path)
    set_background_image(tt, 'file/background_2.png')

    # Adjust bg_color based on your preferences (default is white)
    create_image_label(tt, bg_color="#bbd2f1")

    student_tt_frame(tt, section)

    ttk.Style().configure("TLabel", background='blue')
  
    sec_select_f = tk.Frame(tt, pady=10, padx=98)
    sec_select_f.pack()

    tk.Label(
        sec_select_f,
        text='Select section:  ',
        font=('Consolas', 12, 'bold')
    ).pack(side=tk.LEFT)

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



    tt.mainloop()