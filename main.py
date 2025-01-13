
import ttkbootstrap as ttk
import threading
import time
import tkinter as tk
from UI_files.batch_functions import open_add_batch_form
from UI_files.connection import create_connection
from UI_files.course import open_add_course_form
<<<<<<< HEAD
from UI_files.manageBatch import open_manage_batch_UI
from UI_files.manageRoom import open_manage_room_UI
from UI_files.manageSubject import open_manage_subject_UI
=======
>>>>>>> otherUpdates-local
from UI_files.manageTeacher import open_manage_teacher_UI
from UI_files.rooms_functions import open_add_rooms_form
from UI_files.set_timetable_attributes import open_timetable_attributes
from UI_files.subject_functions import open_add_subject_form
from UI_files.teacher_functions import open_add_teacher_form
from UI_files.manageCourse import open_manage_course_UI



def show_loading():
    # Create a Toplevel window for the loading screen
    loading_window = tk.Toplevel(app)
    loading_window.geometry("300x100")
    loading_window.title("Loading...")
    loading_window.transient(app)
    loading_window.grab_set()
    loading_window.resizable(False, False)

    # Center the loading window
    x = (app.winfo_screenwidth() // 2) - (300 // 2)
    y = (app.winfo_screenheight() // 2) - (100 // 2)
    loading_window.geometry(f"+{x}+{y}")

    # Loading Label
    loading_label = ttk.Label(loading_window, text="Loading, please wait...", font=("Arial", 12))
    loading_label.pack(pady=20)

    # Progress Bar (Spinner)
    progress = ttk.Progressbar(loading_window, mode='indeterminate', bootstyle="info")
    progress.pack(pady=10, padx=20, fill='x')
    progress.start(10)  # Start spinning

    return loading_window

def load_data():
    # Show the loading screen
    loading_screen = show_loading()

    # Simulate a long task in a separate thread
    def long_task():
        time.sleep(3)  # Simulate loading time

        # Destroy the loading window after loading
        loading_screen.destroy()

        # Show a message when loading is done
        ttk.Label(app, text="Data Loaded Successfully!", font=("Arial", 14)).pack(pady=20)

    # Run the task in a separate thread to avoid freezing the UI
    threading.Thread(target=long_task).start()


# Initialize the app
app = ttk.Window(title="Smart University Timetable", themename="united", size=(800, 600))

app.iconbitmap('./Media/logo.ico')

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

def open_add_batch():
    open_add_batch_form(conn)

def open_generate_timetable():
<<<<<<< HEAD
    open_timetable_attributes(app,conn)
=======
    open_timetable_attributes(conn)
>>>>>>> otherUpdates-local

def open_manage_course():
    open_manage_course_UI(conn)

def open_manage_teacher():
    open_manage_teacher_UI(conn)

<<<<<<< HEAD
def open_manage_room():
    open_manage_room_UI(conn)

def open_manage_subject():
    open_manage_subject_UI(conn)

def open_manage_batch():
    open_manage_batch_UI(conn)

=======
>>>>>>> otherUpdates-local



app.grid_columnconfigure(0, weight=1, minsize=200)
app.grid_columnconfigure(1, weight=1, minsize=200)
app.grid_columnconfigure(2,weight=1,minsize=200)

# app.rowconfigure(0, weight=1)

right_frame = ttk.Frame(app)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

left_frame = ttk.Frame(app)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

rightmostFrame = ttk.Frame(app)
rightmostFrame.grid(row=0, column=2, padx=10, pady=10, sticky="nswe")


submit_button = ttk.Button(right_frame,padding=(10,20),width=20, text="Add course", bootstyle="success",command=open_course)
submit_button.pack(pady=20)


submit_button = ttk.Button(right_frame,padding=(10,20),width=20, text="Add Teacher", bootstyle="success",command=open_add_teacher)
submit_button.pack(pady=20)

submit_button = ttk.Button(right_frame,padding=(10,20),width=20, text="Add Rooms", bootstyle="success",command=open_add_rooms)
submit_button.pack(pady=20)

submit_button = ttk.Button(right_frame,padding=(10,20),width=20, text="Add Subject", bootstyle="success",command=open_add_subject)
submit_button.pack(pady=20)


submit_button = ttk.Button(right_frame,padding=(10,20),width=20, text="Add Batch", bootstyle="success",command=open_add_batch)
submit_button.pack(pady=20)


#left frame content

submit_button = ttk.Button(left_frame,padding=(10,20),width=20, text="Generate Timetable", bootstyle="warning",command=open_generate_timetable)
submit_button.pack(pady=20)

#right most content

submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage course", bootstyle="primary",command=open_manage_course)
submit_button.pack(pady=20)

<<<<<<< HEAD
submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage Teacher", bootstyle="primary",command=open_manage_teacher)
submit_button.pack(pady=20)

submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage Room", bootstyle="primary",command=open_manage_room)
submit_button.pack(pady=20)

submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage Subjects", bootstyle="primary",command=open_manage_subject)
submit_button.pack(pady=20)

submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage Batches", bootstyle="primary",command=open_manage_batch)
submit_button.pack(pady=20)




=======
submit_button = ttk.Button(rightmostFrame,padding=(10,20),width=20, text="Manage teacher", bootstyle="primary",command=open_manage_teacher)
submit_button.pack(pady=20)

>>>>>>> otherUpdates-local




# Start the GUI
app.mainloop()

