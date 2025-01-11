
import ttkbootstrap as ttk
import threading
import time
import tkinter as tk
from Adding_Essentials_UI.batch_functions import open_add_batch_form
from Adding_Essentials_UI.connection import create_connection
from Adding_Essentials_UI.course import open_add_course_form
from Adding_Essentials_UI.rooms_functions import open_add_rooms_form
from Adding_Essentials_UI.subject_functions import open_add_subject_form
from Adding_Essentials_UI.teacher_functions import open_add_teacher_form



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

def open_add_batch():
    open_add_batch_form(conn)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.rowconfigure(0, weight=1)

button_frame = ttk.Frame(app)
button_frame.grid(row=0, column=1, sticky="ne", padx=20, pady=20)


submit_button = ttk.Button(button_frame,padding=(10,20),width=20, text="Add course", bootstyle="success",font=("Arial", 12, "bold"),command=open_course)
submit_button.pack(pady=20)


submit_button = ttk.Button(button_frame,padding=(10,20),width=20, text="Add Teacher", bootstyle="success",command=open_add_teacher)
submit_button.pack(pady=20)

submit_button = ttk.Button(button_frame,padding=(10,20),width=20, text="Add Rooms", bootstyle="success",command=open_add_rooms)
submit_button.pack(pady=20)

submit_button = ttk.Button(button_frame,padding=(10,20),width=20, text="Add Subject", bootstyle="success",command=open_add_subject)
submit_button.pack(pady=20)


submit_button = ttk.Button(button_frame,padding=(10,20),width=20, text="Add Batch", bootstyle="success",command=open_add_batch)
submit_button.pack(pady=20)


# Start the GUI
app.mainloop()

