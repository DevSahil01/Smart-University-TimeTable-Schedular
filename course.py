import ttkbootstrap as ttk
from tkinter import messagebox


def open_add_course_form(conn):
    add_course_window = ttk.Toplevel()  # Create a new top-level window
    add_course_window.title("Add Course")
    add_course_window.geometry("400x300")

    width = 400
    height = 300

    # Get the screen width and height to center the window
    screen_width = add_course_window.winfo_screenwidth()
    screen_height = add_course_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_course_window.geometry(f"{width}x{height}+{x_position}+{y_position}")

    # Add Course Form Labels and Entries
    course_name_label = ttk.Label(add_course_window, text="Course Name:", font=("Helvetica", 12))
    course_name_label.pack(pady=10)
    course_name_entry = ttk.Entry(add_course_window, width=30)
    course_name_entry.pack(pady=5)


    # Add Course Button
    def submit_course():
        course_name = course_name_entry.get()
        print(course_name)

        if course_name:
            cursor=conn.cursor();
            cursor.execute("INSERT INTO course (course_name)  VALUES (%s)",(course_name,))
            conn.commit()
            messagebox.showinfo("Success", "Course Added Successfully!")
            add_course_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    submit_button = ttk.Button(add_course_window, text="Add Course", bootstyle="primary", command=submit_course)
    submit_button.pack(pady=20)


    add_course_window.mainloop()
