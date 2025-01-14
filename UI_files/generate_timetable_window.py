
import ttkbootstrap as ttk
from click.core import batch

from UI_files.generate_timetable_function import generate_timeTable_func

def call_generate_func():
    generate_timeTable_func()



def open_generate_timetable_window_UI(conn,batchid):
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

    cursor=conn.cursor()
    cursor.execute("SELECT b.batch_id, b.batch_year, c.course_name FROM batch b JOIN course c ON b.course_id = c.course_id WHERE b.batch_id =3;")
    batch_details=cursor.fetchall()
    print(batch_details)
    batch_name=batch_details[0][2]+'-'+batch_details[0][1]

    generate_button = ttk.Button(horizontal_frame2, text="Get Timetable for " + batch_name, bootstyle="primary",command=call_generate_func)
    generate_button.pack(side="left", pady=20)











