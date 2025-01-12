import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox


def open_add_teacher_form(conn):
    add_teacher_window = ttk.Toplevel()  # Create a new top-level window
    add_teacher_window.title("Add teacher")
    add_teacher_window.geometry("700x500")

    width = 700
    height = 500

    # Get the screen width and height to center the window
    screen_width = add_teacher_window.winfo_screenwidth()
    screen_height = add_teacher_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_teacher_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM course")
    courses = cursor.fetchall()

    course_names = [course[1] for course in courses]
    course_ids = {course[1]: course[0] for course in courses}

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    day_vars = {}

    #input values
    teacher_name_label = ttk.Label(add_teacher_window, text="Teacher Name:", font=("Helvetica", 12))
    teacher_name_label.pack(pady=10)
    teacher_name_entry = ttk.Entry(add_teacher_window, width=30)
    teacher_name_entry.pack(pady=5)

    course_name_label = ttk.Label(add_teacher_window, text="Course Name:", font=("Helvetica", 12))
    course_name_label.pack(pady=10)
    course_type_combobox = ttk.Combobox(add_teacher_window, values=course_names, width=30)
    course_type_combobox.set(course_names[0])  # Default selection
    course_type_combobox.pack(pady=5)

    available_days_label = ttk.Label(add_teacher_window, text="Select Available Days:", font=("Helvetica", 12))
    available_days_label.pack(pady=10)
    checkbox_frame = ttk.Frame(add_teacher_window)
    checkbox_frame.pack(pady=10)

    for day in days_of_week:
        day_vars[day] = tk.BooleanVar()
        checkbox = ttk.Checkbutton(checkbox_frame, text=day, variable=day_vars[day], bootstyle="info")
        checkbox.pack(side='left',padx=6)

    def get_selected_days():
        selected_days = []
        for day, var in day_vars.items():
            if var.get():
                selected_days.append(day)
        return selected_days

    def select_all_days():
        select_all = select_all_var.get()  # Get the state of the "Select All" checkbox
        for var in day_vars.values():
            var.set(select_all)  # Set each day checkbox to the "Select All" state

    # Create "Select All" checkbox
    select_all_var = tk.BooleanVar()  # Variable to hold the state of the "Select All" checkbox
    select_all_checkbox = ttk.Checkbutton(checkbox_frame, text="Select All", variable=select_all_var,
                                          command=select_all_days)
    select_all_checkbox.pack(side='left', padx=10)
    # Add Course Button
    def submit_teacher():
        teacher_name=teacher_name_entry.get()
        selected_course_name = course_type_combobox.get()
        selected_days = get_selected_days()
        days_string = ', '.join(selected_days)



        if teacher_name and selected_course_name:
            course_id = course_ids.get(selected_course_name)
            if course_id :
                cursor=conn.cursor();
                cursor.execute("INSERT INTO teachers (teacher_name,available_days,course_id)  VALUES (%s,%s,%s)",(teacher_name,days_string,course_id))
                conn.commit()
                messagebox.showinfo("Success", "Teacher Added Successfully!")
                add_teacher_window.destroy()
            else:
                messagebox.showwarning("Course Error", "Selected course does not exist.")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    submit_button = ttk.Button(add_teacher_window, text="Add Course", bootstyle="primary", command=submit_teacher)
    submit_button.pack(pady=20)
    add_teacher_window.mainloop()
