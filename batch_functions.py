import ttkbootstrap as ttk
from tkinter import messagebox


def open_add_batch_form(conn):
    add_batch_window = ttk.Toplevel()  # Create a new top-level window
    add_batch_window.title("Add batch")
    add_batch_window.geometry("400x300")

    width = 400
    height = 300

    # Get the screen width and height to center the window
    screen_width = add_batch_window.winfo_screenwidth()
    screen_height = add_batch_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_batch_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM course")
    courses = cursor.fetchall()

    course_names = [course[1] for course in courses]
    course_ids = {course[1]: course[0] for course in courses}

    batch_year_label = ttk.Label(add_batch_window, text="Year:", font=("Helvetica", 12))
    batch_year_label.pack(pady=10)
    batch_year_entry = ttk.Entry(add_batch_window, width=30)
    batch_year_entry.pack(pady=5)

    batch_noOfStudents_label = ttk.Label(add_batch_window, text="No of students:", font=("Helvetica", 12))
    batch_noOfStudents_label.pack(pady=10)
    batch_noOfStudents_entry = ttk.Entry(add_batch_window, width=30)
    batch_noOfStudents_entry.pack(pady=5)

    batch_noOfDivisions_label = ttk.Label(add_batch_window, text="No of divisions:", font=("Helvetica", 12))
    batch_noOfDivisions_label.pack(pady=10)
    batch_noOfDivisions_entry = ttk.Entry(add_batch_window, width=30)
    batch_noOfDivisions_entry.pack(pady=5)

    batch_noOfBatches_label = ttk.Label(add_batch_window, text="No of practical batches:", font=("Helvetica", 12))
    batch_noOfBatches_label.pack(pady=10)
    batch_noOfBatches_entry = ttk.Entry(add_batch_window, width=30)
    batch_noOfBatches_entry.pack(pady=5)

    course_name_label = ttk.Label(add_batch_window, text="Course Name:", font=("Helvetica", 12))
    course_name_label.pack(pady=10)
    course_type_combobox = ttk.Combobox(add_batch_window, values=course_names, width=30)
    course_type_combobox.set(course_names[0])  # Default selection
    course_type_combobox.pack(pady=5)




    # Add batch Button
    def submit_batch():
        year=batch_year_entry.get()
        noOfStudents=batch_noOfStudents_entry.get()
        noOfDivisions=batch_noOfDivisions_entry.get()
        noOfPracBatches=batch_noOfBatches_entry.get()

        if noOfDivisions and noOfStudents and noOfPracBatches:
            cursor=conn.cursor();
            cursor.execute("INSERT INTO batch (batch_name)  VALUES (%s)",(batch_name,))
            conn.commit()
            messagebox.showinfo("Success", "batch Added Successfully!")
            add_batch_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    submit_button = ttk.Button(add_batch_window, text="Add batch", bootstyle="success", command=submit_batch)
    submit_button.pack(pady=20)


    add_batch_window.mainloop()
