
import ttkbootstrap as ttk
from click.core import batch

from UI_files.generate_timetable_function import generate_timeTable_func, timetable_generator_for_therotical_batches
from tkinter import messagebox

def call_generate_func(batch,course,year,generatetime):
    print(course)
    if course in ["MCA","BSC-IT","BSC-CS"]:
        generate_timeTable_func(batch,course,year)
        messagebox.showinfo("Success", "Timetable generated successfully!", parent=generatetime)
    elif course in ["BCOM", "MMS", "MBA", "PGDM"]:
        timetable_generator_for_therotical_batches(batch,course,year)
        messagebox.showinfo("Success", "Timetable generated successfully", parent=generatetime)





def open_generate_timetable_window_UI(conn):
    add_timetable_window = ttk.Toplevel()  # Create a new top-level window
    add_timetable_window.title("Add timetable")
    add_timetable_window.geometry("1400x700")

    width = 1400
    height = 700

    # Get the screen width and height to center the window
    screen_width = add_timetable_window.winfo_screenwidth()
    screen_height = add_timetable_window.winfo_screenheight()

    # Set the window position and size
    add_timetable_window.geometry(
        f"{add_timetable_window.winfo_screenwidth()}x{add_timetable_window.winfo_screenheight()}+0+0")

    horizontal_frame1 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame1.pack(pady=5, padx=20, fill="x")

    horizontal_frame2 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame2.pack(pady=5, padx=20, fill="x")

    cur=conn.cursor()
    cur.execute("SELECT DISTINCT batch_id FROM subjecttoteacher")
    batches=[item[0] for item in cur.fetchall()]


    for batch in batches:
        cur=conn.cursor()
        cur.execute(
            "SELECT c.course_name, b.batch_year FROM batch b JOIN course c ON b.course_id = c.course_id WHERE b.batch_id = %s;",
            (batch,)  # Ensuring the paraeter is passed as a tuple
        )
        result = cur.fetchall()
        print('results')
        print(result)

        submit_button = ttk.Button(add_timetable_window, padding=(10, 20), width=20, text=result[0][0]+result[0][1], bootstyle="success",
                                   command=lambda  : call_generate_func(batch,result[0][0],result[0][1],add_timetable_window))
        submit_button.pack(pady=20)












