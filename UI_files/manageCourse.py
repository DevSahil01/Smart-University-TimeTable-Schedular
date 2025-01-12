import ttkbootstrap as ttk


def open_manage_course_UI(conn):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM course")
    course_data=cursor.fetchall()
    print(course_data)

    manage_teacher_window = ttk.Toplevel()  # Create a new top-level window
    manage_teacher_window.title("Add teacher")
    manage_teacher_window.geometry("400x300")

    width = 800
    height = 450

    # Get the screen width and height to center the window
    screen_width = manage_teacher_window.winfo_screenwidth()
    screen_height = manage_teacher_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    manage_teacher_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    course_label = ttk.Label(manage_teacher_window, text="courses data", font=("Helvetica", 12))
    course_label.grid(pady=10)


     # UI

    # course_name  |  actions
    # MCA          |   Edit  Delete
    # MMS           | edit    delete


