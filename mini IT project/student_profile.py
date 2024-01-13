import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3

class StudentProfilePage:
    def __init__(self, root, student_data):
        self.root = root
        self.root.title("Student Profile")

        # Connect to the SQLite database
        self.conn = sqlite3.connect("profile.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Ensure the 'students' table exists
        self.create_table()

        # Student data (replace with actual data)
        self.student_data = student_data

        # Create and configure widgets
        self.create_widgets()

    def create_table(self):
        # Create the 'students' table if it doesn't exist
        with self.conn:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT,
                    dob TEXT,
                    email TEXT,
                    address TEXT,
                    profile_picture TEXT
                )
            ''')

    def close_database(self):
        # Close the database connection
        self.conn.close()

    def create_widgets(self):
        # Frame for general information
        self.general_info_frame = ttk.Frame(self.root, padding="20")
        self.general_info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Display profile picture
        ttk.Label(self.general_info_frame, text="Profile Picture:").grid(row=0, column=0, sticky=tk.W)
        self.update_profile_picture()

        # Display general information
        ttk.Label(self.general_info_frame, text="Student ID:").grid(row=1, column=0, sticky=tk.W)
        self.student_id_label = ttk.Label(self.general_info_frame, text=self.student_data.get("student_id", ""))
        self.student_id_label.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(self.general_info_frame, text="Name:").grid(row=2, column=0, sticky=tk.W)
        self.name_label = ttk.Label(self.general_info_frame, text=self.student_data.get("name", ""))
        self.name_label.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(self.general_info_frame, text="Date of Birth:").grid(row=3, column=0, sticky=tk.W)
        self.dob_label = ttk.Label(self.general_info_frame, text=self.student_data.get("dob", ""))
        self.dob_label.grid(row=3, column=1, sticky=tk.W)

        ttk.Label(self.general_info_frame, text="Email:").grid(row=4, column=0, sticky=tk.W)
        self.email_label = ttk.Label(self.general_info_frame, text=self.student_data.get("email", ""))
        self.email_label.grid(row=4, column=1, sticky=tk.W)

        ttk.Label(self.general_info_frame, text="Address:").grid(row=5, column=0, sticky=tk.W)
        self.address_label = ttk.Label(self.general_info_frame, text=self.student_data.get("address", ""))
        self.address_label.grid(row=5, column=1, sticky=tk.W)

        # Button to edit profile
        ttk.Button(self.root, text="Edit Profile", command=self.edit_profile).grid(row=1, column=0, sticky=tk.E)

    def update_profile_picture(self):
        # Update the profile picture label with the selected image
        image_path = self.student_data.get("profile_picture", "background_2.png")
        image = Image.open(image_path)
        # Resize the image to have a width of 208 and a height of 148
        image = image.resize((208, 148), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        profile_picture_label = ttk.Label(self.general_info_frame, image=photo)
        profile_picture_label.image = photo  # to prevent image from being garbage collected
        profile_picture_label.grid(row=0, column=1, sticky=tk.W)

    def edit_profile(self):
        # Create a new window for editing
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")

        # Create and configure widgets for editing
        ttk.Label(edit_window, text="Name:").grid(row=0, column=0, sticky=tk.W)
        name_entry = ttk.Entry(edit_window)
        name_entry.insert(0, self.student_data.get("name", ""))
        name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(edit_window, text="Date of Birth:").grid(row=1, column=0, sticky=tk.W)
        dob_entry = ttk.Entry(edit_window)
        dob_entry.insert(0, self.student_data.get("dob", ""))
        dob_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Label(edit_window, text="Email:").grid(row=2, column=0, sticky=tk.W)
        email_entry = ttk.Entry(edit_window)
        email_entry.insert(0, self.student_data.get("email", ""))
        email_entry.grid(row=2, column=1, sticky=tk.W)

        ttk.Label(edit_window, text="Address:").grid(row=3, column=0, sticky=tk.W)
        address_entry = ttk.Entry(edit_window)
        address_entry.insert(0, self.student_data.get("address", ""))
        address_entry.grid(row=3, column=1, sticky=tk.W)

        # Button to select a new profile picture
        ttk.Label(edit_window, text="Profile Picture:").grid(row=4, column=0, sticky=tk.W)
        ttk.Button(edit_window, text="Select Picture", command=lambda: self.select_picture(edit_window)).grid(row=4, column=1, sticky=tk.W)

        # Button to save changes
        ttk.Button(edit_window, text="Done", command=lambda: self.save_changes(
            name_entry.get(), dob_entry.get(), email_entry.get(), address_entry.get(), edit_window)
        ).grid(row=5, column=1, sticky=tk.E)

    def select_picture(self, edit_window):
        # Open a file dialog to select a new profile picture
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            # Update the profile picture label and store the file path
            self.student_data["profile_picture"] = file_path
            self.update_profile_picture()

    def save_changes(self, name, dob, email, address, edit_window):
        # Update student data
        self.student_data["name"] = name
        self.student_data["dob"] = dob
        self.student_data["email"] = email
        self.student_data["address"] = address

        # Update labels in the main profile page
        self.name_label.config(text=name)
        self.dob_label.config(text=dob)
        self.email_label.config(text=email)
        self.address_label.config(text=address)

        # Update the profile picture
        self.update_profile_picture()

        # Update or insert the student data into the database
        self.save_to_database()

        # Close the editing window
        edit_window.destroy()
        messagebox.showinfo("Success", "Profile updated successfully!")

    def save_to_database(self):
        # Update or insert student data into the 'students' table
        student_id = self.student_data.get("student_id", "")
        name = self.student_data.get("name", "")
        dob = self.student_data.get("dob", "")
        email = self.student_data.get("email", "")
        address = self.student_data.get("address", "")
        profile_picture = self.student_data.get("profile_picture", "")

        with self.conn:
            self.cursor.execute('''
                INSERT OR REPLACE INTO students (student_id, name, dob, email, address, profile_picture)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, name, dob, email, address, profile_picture))

def main():
    # Dummy student data (replace with actual data)
    student_data = {
        "student_id": "123456",
        "name": "John Doe",
        "dob": "01/01/2000",
        "email": "john.doe@example.com",
        "address": "123 Main Street, Cityville",
        "profile_picture": "background_2.png"
    }

    root = tk.Tk()
    app = StudentProfilePage(root, student_data)
    root.mainloop()

    # Close the database connection when the application exits
    app.close_database()

if __name__ == "__main__":
    main()
