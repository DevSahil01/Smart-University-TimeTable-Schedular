from tkinter import PhotoImage

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from connection import create_connection
from course import open_add_course_form
from rooms_functions import open_add_rooms_form
from subject_functions import open_add_subject_form
from teacher_functions import open_add_teacher_form
# Initialize the app
app = ttk.Window(title="Smart University Timetable", themename="litera", size=(800, 600))

app.iconbitmap('logo.ico')

app.state("zoomed")

conn=create_connection()

def open_course():
    open_add_course_form(conn)

def open_add_teacher():
    open_add_teacher_form(conn)

def open_add_rooms():
    open_add_rooms_form(conn)

def open_add_subject():
    open_add_subject_form(conn)




submit_button = ttk.Button(app, text="Add course", bootstyle=SUCCESS,command=open_course)
submit_button.pack(pady=20)


submit_button = ttk.Button(app, text="Add Teacher", bootstyle=SUCCESS,command=open_add_teacher)
submit_button.pack(pady=20)

submit_button = ttk.Button(app, text="Add Rooms", bootstyle=SUCCESS,command=open_add_rooms)
submit_button.pack(pady=20)

submit_button = ttk.Button(app, text="Add Subject", bootstyle=SUCCESS,command=open_add_subject)
submit_button.pack(pady=20)



# Start the GUI
app.mainloop()

