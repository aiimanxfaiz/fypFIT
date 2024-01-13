import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def on_treeview_select(event):
    selected_item = Course_tree.selection()[0]
    values = Course_tree.item(selected_item, 'values')

    # Update entry widgets with selected values
    Name_entry.delete(0, END)
    Name_entry.insert(0, values[0])

    Code_entry.delete(0, END)
    Code_entry.insert(0, values[1])

    Faculty_entry.delete(0, END)
    Faculty_entry.insert(0, values[2])

    # Enable the "Update" and "Remove" buttons
    update_button.config(state=NORMAL)
    remove_button.config(state=NORMAL)

def add_course():
    name = Name_entry.get()
    code = Code_entry.get()
    faculty = Faculty_entry.get()

    if name and code and faculty:
        # Add new course to the Treeview with the appropriate tag for row coloring
        new_item_id = Course_tree.insert("", "end", values=(name, code, faculty))
        tags = ('evenrow' if Course_tree.index(new_item_id) % 2 == 0 else 'oddrow',)
        Course_tree.item(new_item_id, tags=tags)

        # Clear entry widgets
        clear_entries()
    else:
        messagebox.showwarning("Warning", "Please enter values for Name, Code, and Faculty.")

def update_course():
    selected_item = Course_tree.selection()[0]
    values = (Name_entry.get(), Code_entry.get(), Faculty_entry.get())
    Course_tree.item(selected_item, values=values)

def remove_course():
    selected_item = Course_tree.selection()[0]
    Course_tree.delete(selected_item)
    clear_entries()

def clear_entries():
    Name_entry.delete(0, END)
    Code_entry.delete(0, END)
    Faculty_entry.delete(0, END)

    # Disable the "Update" and "Remove" buttons
    update_button.config(state=DISABLED)
    remove_button.config(state=DISABLED)

root = Tk()
root.title('Admin Course Menu')
root.iconbitmap('')
root.geometry("1200x800") 

# Top frames
Label(root, text="Admin Course Page", width=1, height=3, bg='blue').pack(side=TOP, fill=X)

# Bottom frames
Label(root, width=1, height=2, bg='#bcbcbc', anchor='e').pack(side=BOTTOM, fill=X)

# Cosmetic
# Treeview Colors
style = ttk.Style()
style.theme_use('default')
style.configure("treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', "#347083")])

# Tree Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10, side=RIGHT)

# Scroll function
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create a Treeview instance
Course_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll, selectmode='extended', columns=["Name", "Code", "Faculty"])
tree_scroll.config(command=Course_tree.yview)

# Format our columns
Course_tree.column("#0", width=0, stretch=NO)
Course_tree.column("Name", anchor=W, width=200, minwidth=25)
Course_tree.column("Code", anchor=CENTER, width=120, minwidth=25)
Course_tree.column("Faculty", anchor=W, width=120, minwidth=25)

# Create headings
Course_tree.heading("#0", text="", anchor=W)
Course_tree.heading("Name", text="Name", anchor=W)
Course_tree.heading("Code", text="Code", anchor=CENTER)
Course_tree.heading("Faculty", text="Faculty", anchor=W)

# Add Course Data
data = [
    ["Mathematics III", "PMT0301", "FCI"],
    ["Principles of Physics", "PPP0101", "FCI"],
    ["Mini IT Project", "PSP0201", "FCI"],
    ["Intro to Digital Systems", "PDS0101", "FCI"],
    ["Critical Thinking", "PCR0025", "FCI"],
    ["Academic English", "PEN0065", "FCI"]
]

# Row colors
Course_tree.tag_configure('oddrow', background="white")
Course_tree.tag_configure('evenrow', background="lightblue")

count = 0
for record in data:
    if count % 2 == 0:
        Course_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]),
                           tags=('evenrow'))
    else:
        Course_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]),
                           tags=('oddrow'))
    count += 1

# Data entry boxes
data_frame = LabelFrame(root,  bg="#89CFF0")
data_frame.pack(fill="y", padx=20, pady=10)

Name_label = Label(data_frame, text="Name", bg="#89CFF0")
Name_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)
Name_entry = Entry(data_frame)
Name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

Code_label = Label(data_frame, text="Code", bg="#89CFF0")
Code_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)
Code_entry = Entry(data_frame)
Code_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W)

Faculty_label = Label(data_frame, text="Faculty", bg="#89CFF0")
Faculty_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)
Faculty_entry = Entry(data_frame)
Faculty_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

# Button frame
Button_frame = LabelFrame(root, bg="#89CFF0")
Button_frame.pack(fill="y",expand='N', padx=20, pady=10)

add_button = Button(Button_frame, text="Add", bg="#89CFF0", command=add_course)
add_button.grid(row=5, column=0, padx=10, pady=5)

update_button = Button(Button_frame, text="Update", bg="#89CFF0", state=DISABLED, command=update_course)
update_button.grid(row=5, column=1, padx=10, pady=5)

remove_button = Button(Button_frame, text="Remove", bg="#89CFF0", state=DISABLED, command=remove_course)
remove_button.grid(row=5, column=2, padx=10, pady=5)

cancel_button = Button(Button_frame, text="Cancel", bg="#89CFF0", command=clear_entries)
cancel_button.grid(row=5, column=3, padx=10, pady=5)

# Bind the on_treeview_select function to the Treeview's <<TreeviewSelect>> event
Course_tree.bind('<<TreeviewSelect>>', on_treeview_select)

Course_tree.pack(pady=20, fill=BOTH, expand=YES)

root.mainloop()
