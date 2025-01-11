import ttkbootstrap as ttk
from tkinter import messagebox


def open_add_subject_form(conn):
    add_subject_window = ttk.Toplevel()  # Create a new top-level window
    add_subject_window.title("Add subject")
    add_subject_window.geometry("400x300")

    width = 400
    height = 450

    # Get the screen width and height to center the window
    screen_width = add_subject_window.winfo_screenwidth()
    screen_height = add_subject_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_subject_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    subject_types=["theory","practical"]

    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM course")
    courses = cursor.fetchall()

    course_names = [course[1] for course in courses]
    course_ids = {course[1]: course[0] for course in courses}

    # Add subject Form Labels and Entries
    subject_name_label = ttk.Label(add_subject_window, text="subject Name:", font=("Helvetica", 12))
    subject_name_label.pack(pady=10)
    subject_name_entry = ttk.Entry(add_subject_window, width=30)
    subject_name_entry.pack(pady=5)

    subject_semester_label = ttk.Label(add_subject_window, text="Semester:", font=("Helvetica", 12))
    subject_semester_label.pack(pady=10)
    subject_semester_entry = ttk.Entry(add_subject_window, width=30)
    subject_semester_entry.pack(pady=5)

    subject_type_label = ttk.Label(add_subject_window, text="Room Type:", font=("Helvetica", 12))
    subject_type_label.pack(pady=10)
    subject_type_combobox = ttk.Combobox(add_subject_window, values=subject_types, width=30)
    subject_type_combobox.set(subject_types[0])  # Default selection
    subject_type_combobox.pack(pady=5)

    course_name_label = ttk.Label(add_subject_window, text="Course Name:", font=("Helvetica", 12))
    course_name_label.pack(pady=10)
    course_type_combobox = ttk.Combobox(add_subject_window, values=course_names, width=30)
    course_type_combobox.set(course_names[0])  # Default selection
    course_type_combobox.pack(pady=5)


    # Add subject Button
    def submit_subject():
        subject_name = subject_name_entry.get()
        semester=subject_semester_entry.get()
        subject_type=subject_type_combobox.get()
        course=course_type_combobox.get()

        if subject_name:
            course_id=course_ids.get(course)
            if course_id:
                cursor=conn.cursor();
                cursor.execute("INSERT INTO subjects (subject_name,semester,subject_type,course_id)  VALUES (%s,%s,%s,%s)",(subject_name,semester,subject_type,course_id))
                conn.commit()
                messagebox.showinfo("Success", "subject Added Successfully!")
                add_subject_window.destroy()
            else:
                messagebox.showwarning("Course Error", "Selected course does not exist.")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    submit_button = ttk.Button(add_subject_window, text="Add subject", bootstyle="success", command=submit_subject)
    submit_button.pack(pady=20)


    add_subject_window.mainloop()
