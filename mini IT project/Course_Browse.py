from tkinter import *
from tkinter import ttk, StringVar, messagebox
from tkinter import PhotoImage, Label
from PIL import Image, ImageTk
from tkinter import ttk
from subprocess import call



def page_1():
    FONT_STYLE = ('TkDefaultFont', 10)

    background = '#FFFFFF'
    framebg = '#EDEDED'
    framefg = '#06283D'

    root = Tk()
    root.title("Browse Course")
    root.resizable(False,False)
    root.geometry("1366x768")
    root.config(bg=background)

    # top frames
    Label(root, width=1, height=3, bg='#a0caf0', anchor='e', borderwidth=1, relief="solid").pack(side=TOP, fill=X)

    # Bottom frames
    Label(root, width=1, height=2, bg='#bcbcbc', anchor='e').pack(side=BOTTOM, fill=X)

    #frame for Finding Course 
    frame_behind = Label(root, width=80, bg='#6393bf', fg=framefg, height = 10, borderwidth=1, relief="solid")
    frame_behind.place(x=401, y=88)
    frame_find = Label(root, width=80, bg='#78a7d2', fg=framefg, height = 10, borderwidth=1, relief="solid")
    frame_find.place(x=395, y=82)


    # Add MMU to the top left corner 
    image_MMU = Image.open("image_1.png")
    image_1 = ImageTk.PhotoImage(image_MMU)
    image_1_label = Label(root, width=0, height=30, image=image_1, bg='#a0caf0', anchor='w')
    image_1_label.place(x=4, y=5)

    #add menu icon
    image_menu = Image.open("3 line.png")
    image_6 = ImageTk.PhotoImage(image_menu)
    image_6_label = Label(root, width=0, height=30, image=image_6, bg='#a0caf0', anchor='e')
    image_6_label.place(x=1200, y=5)

    # home image 
    image_Home = Image.open("home button.png")
    image_2 = ImageTk.PhotoImage(image_Home)
    image_2_label = Label(root, width=0, text='.', height=30, image=image_2, bg='#a0caf0', anchor='w')
    image_2_label.place(x=160, y=5)

    # Graduation hat 
    image_hat = Image.open("image hat graduation.png")
    image_5 = ImageTk.PhotoImage(image_hat)
    image_5_label = Label(root, width=30, height=30,bg='#78a7d2', image=image_5)
    image_5_label.place(x=660, y=90)        

    # Title Label (centered in the middle)
    title_label = Label(root, text='Find A Course For You', bg='#78a7d2',fg ='white',font=('TkDefaultFont', 12, 'bold'))
    title_label.place(x=585, y=125)

    # Combobox to select courses
    clicked = StringVar()
    clicked.set('Select courses')
    browse_combobox = ttk.Combobox(root, textvariable=clicked, values=['Foundation in IT (foundation in Information Technology)', 'Foundation in Engineer (foundation in Engineering)'])
    browse_combobox.place(x=510, y=155, width=340)
    
    root.image_IT_course = Image.open("2022_1196_NH_016.png")
    image_IT_course= ImageTk.PhotoImage(root.image_IT_course)
    
    root.image_IT_course = Image.open("mechanicalengineering.png")
    image_ENGINEER_course= ImageTk.PhotoImage(root.image_IT_course)



    #frame for course IT
    def frame_IT():
        frame_course = Label(root, width=25, bg = framebg, fg=framefg, height = 13, borderwidth=1, relief="solid").place(x=240, y = 330)
        frame_course2 = Label(root, text = 'Foundation in IT', font=('TkDefaultFont', 10,"bold"), width=22, bg = '#2596be', fg='#FFFFFF', height = 3, borderwidth=1, relief="solid").place(x=240, y = 510)
        image_3_label = Label(root, width=180, height=175, image=image_IT_course, borderwidth=1, relief="solid").place(x=240, y = 330)      
            
    #frame for course Engineer
    def frame_Engineer():
        frame_course3 = Label(root, width=25, bg = framebg, fg=framefg, height = 13,borderwidth=1, relief="solid").place(x=935, y = 330)
        frame_course4 = Label(root, text = 'Foundation in Engineering', font=('TkDefaultFont', 10,"bold"), width=22, bg = '#2596be', fg='#FFFFFF', height = 3, borderwidth=1, relief="solid").place(x=935, y = 510)

    
        image_4_label = Label(root, width=180, height=175, image=image_ENGINEER_course, borderwidth=1, relief="solid").place(x=935, y = 330)  
            
    #initially display both
    frame_IT()
    frame_Engineer()

    def show_tab():
        selected_course = clicked.get()
            #Check if a course has been selected 

        if selected_course == 'Select courses':
                messagebox.showerror('Error', 'Please select a course before clicking "Show Programme".')
                return

        if 'Foundation in IT' in selected_course:
                frame_IT()
                tab_IT()

        elif 'Foundation in Engineer' in selected_course:
                frame_course3 = Label(root, width=25, bg = framebg, fg=framefg, height = 13).place(x=240, y = 330)
                frame_course4 = Label(root, text = 'Foundation in Engineering', font=('TkDefaultFont', 10,"bold"), width=22, bg = '#2596be', fg='#FFFFFF', height = 3).place(x=240, y = 510)
                image_4_label = Label(root, width=180, height=175, image=image_ENGINEER_course).place(x=240, y = 330) 
                tab_Engineer()
            

    # Button 'show programme'
    button_show = ttk.Button(root, text='Show Programme Offered', command=show_tab, style='TButton')
    button_show.place(x=600, y=185)


    #tab for IT
    def tab_IT():
        notebook = ttk.Notebook(root)
        tab_1_IT = Frame(root,borderwidth=1, relief="solid")
        tab_2_IT = Frame(root,borderwidth=1, relief="solid")
        tab_3_IT = Frame(root,borderwidth=1, relief="solid")

        notebook.add(tab_1_IT, text  = 'Details')
        notebook.add(tab_2_IT, text  = 'Entry Requirements')
        notebook.add(tab_3_IT, text  = 'Program Structure')

        notebook.place( x=450, y = 330, height= 270,width = 800)

        # Text for the Details tab
        tab1_text_IT = """
        In an ever-changing, technologically dependent world,our one-year Foundation in Information Technology
        programme aims to produce students who are well-equipped with computer skills as well as mathematical 
        and physics skills.The Foundation in Information Technology programme is delivered through engaging 
        lectures and laboratory work which serve to build knowledge and help develop practical skills.
        After completion of the foundation programme you can opt for a degree programme from either 
        Faculty of Computing and Informatics (FCI) or Faculty of Information, Science and Technology (FIST).
        """
        tab2_text_IT = """
        Pass SPM/O-Level or its equivalent with a minimum of Grade C in at least five (5) subjects inclusive of 
        Mathematics and English; OR Pass UEC with a minimum of Grade B in at least three (3) subjects 
        inclusive of Mathematics and English. Additional Requirement to pursue Bachelor of Computer Science (Honours):
        A Credit in Additional Mathematics at SPM Level or its equivalent; OR Credit in Mathematics AND 
        one Science/Technology/Engineering subject at SPM Level or its equivalent.
        """
        tab3_text_IT = """

        Trimester 1                                                                  Trimester 2
        Introduction to Business Management                            Critical Thinking                                                   
        Introduction to Computing Technologies                          Essential English
        Communicative English                                                 Multimedia Fundamentals
        Mathematics 1                                                             Mathematics II
        Problem Solving and Programme Design                        Principles of Physics
                                                                                        Introduction to Digital Systems                              
        Trimester 3
        Academic English
        Mathematics III
        Mini IT Project
            """

        tab1_label_IT = Label(tab_1_IT, text=tab1_text_IT, wraplength=710, font=('TkDefaultFont', 11) ).pack(padx=10, pady=10)
        tab2_label_IT = Label(tab_2_IT, text=tab2_text_IT, wraplength=710, font=('TkDefaultFont', 11)).pack(padx=10, pady=10)
        tab3_label_IT = Label(tab_3_IT, text=tab3_text_IT, wraplength=670, width =80, height= 13, justify= 'left', font=('TkDefaultFont', 10)).pack(padx=10, pady=10)
        return()

    def tab_Engineer():
        notebook = ttk.Notebook(root)
        tab_1_Engineer = Frame(root,borderwidth=1, relief="solid")
        tab_2_Engineer = Frame(root,borderwidth=1, relief="solid")
        tab_3_Engineer = Frame(root,borderwidth=1, relief="solid")

        notebook.add(tab_1_Engineer, text  = 'Details')
        notebook.add(tab_2_Engineer, text  = 'Entry Requirements')
        notebook.add(tab_3_Engineer, text  = 'Program Structure')

        notebook.place( x=450, y = 330, height= 270, width = 800)

        tab1_text_engineer = """
        The one-year Foundation in Engineering programme is the preferred route for many Malaysians 
        and international students to access engineering courses in Multimedia University. Set in a 
        campus environment that enriches their preparation fordegree studies, the programme’s 
        curriculum focuses on delivering preparatory engineering subjects to equip students with 
        strong fundamentals in order to excel with confidence. In addition to analytical and technical
        knowledge, the programme also focuses on equipping students with critical thinking and interpersonal 
        skills to succeed not only in their undergraduate studies, but more importantly, as independent life-long learners.

        After completion of the foundation programme you can opt for a degree programme from either Faculty of Engineering (FOE) or Faculty of Engineering & Technology (FET).
        """
    
        tab2_text_engineer ="""
        Pass SPM/O-Level or its equivalent with a minimum of Grade C in at least five (5) subjects
        inclusive of English, Mathematics or Add. Mathematics and one Engineering-related subject; OR
        Pass UEC with a minimum of Grade B in at least three (3) subjects 
        inclusive of Mathematics, English and one Engineering-related subject.
        """

        tab3_text_engineer ="""
        Trimester 1                                                             Trimester 2
        Basic Computing & Programming                         Calculus
        Pre-Calculus                                                           Electricity & Magnetism
        Trigonometry & Coordinate Geometry                    Chemistry
        Mechanics                                                               Introduction to Business Management
        Communicative English                                          Critical Thinking
                                                                                        Essential English
        Trimester 3
        Introduction to Probability & Statistics
        Modern Physics & Thermodynamics
        Academic English
        """

        tab1_label_Engineer = Label(tab_1_Engineer, text= tab1_text_engineer,  wraplength=730, font=('TkDefaultFont', 11)).pack()
        tab2_label_Engineer = Label(tab_2_Engineer, text=tab2_text_engineer,  wraplength=730,font=('TkDefaultFont', 11)).pack()
        tab3_label_Engineer = Label(tab_3_Engineer, text=tab3_text_engineer,  wraplength=730,  justify= 'left', font=('TkDefaultFont', 11)).pack()
        return()


    def course_registration():
        root.destroy()  # Close the current window (page 1)
        call(['python', 'Course_registeration.py'])


    course_registeration_page = Button(root, text = 'Register Course', command= course_registration, width= 20, height = 2, bg='#FF290B')
    course_registeration_page.place(x=1100, y =660) 

    def clickable_label(event):
            clicked_label_text = event.widget["text"]

            if clicked_label_text == '.':
                root.destroy()
                call(['python', 'HomePage2.py'])

    root.bind("<Button-1>", clickable_label)

    
    root.mainloop()


def page_2():
    call(['python', 'reg.py'])


page_1()

