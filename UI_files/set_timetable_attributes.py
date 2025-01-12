import ttkbootstrap as ttk



def open_timetable_attributes(root,conn):
    add_timetable_window = ttk.Toplevel(root)  # Create a new top-level window
    add_timetable_window.title("Add timetable")
    add_timetable_window.geometry("400x300")

    width = 900
    height = 700

    # Get the screen width and height to center the window
    screen_width = add_timetable_window.winfo_screenwidth()
    screen_height = add_timetable_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_timetable_window.geometry(f"{width}x{height}+{x_position}+{y_position}")


    # Configure grid columns to expand equally
    add_timetable_window.grid_columnconfigure(0, weight=3)
    add_timetable_window.grid_columnconfigure(1, weight=3)
    add_timetable_window.grid_columnconfigure(2, weight=3)
    add_timetable_window.grid_columnconfigure(3,weight=3)


    #left frame for subject input
    left_frame = ttk.Frame(add_timetable_window, padding=10)
    left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)



    #right frame for teacher input
    right_frame = ttk.Frame(add_timetable_window, padding=10)
    right_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)




    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM course")
    courses = cursor.fetchall()

    course_names = [course[1] for course in courses]
    course_ids = {course[1]: course[0] for course in courses}

    # middle frame for normal inputs
    middle_frame = ttk.Frame(add_timetable_window, padding=10)
    middle_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


    semester_label = ttk.Label(middle_frame, text="Select Semester:", font=("Helvetica", 12))
    semester_label.grid(pady=10)
    semester_combobox = ttk.Combobox(middle_frame, values=[1,2,3,4,5,6,7,8], width=30)
    semester_combobox.set(1)  # Default selection
    semester_combobox.grid(pady=5)

    course_label = ttk.Label(middle_frame, text="Course Name:", font=("Helvetica", 12))
    course_label.grid(pady=10)
    course_combobox = ttk.Combobox(middle_frame, values=course_names, width=30)
    course_combobox.set(course_names[0])  # Default selection
    course_combobox.grid(pady=5)

    def getSubjectAndTeacher():
        course_id=course_ids.get(course_combobox.get())
        cursor = conn.cursor()
        cursor.execute("select subject_id,subject_name from subjects where course_id=(%s) and semester=(%s)",
                       (course_id, semester_combobox.get()))
        subjects_data = cursor.fetchall()

        cursor=conn.cursor()
        cursor.execute("select teacher_id,teacher_name from teachers where course_id=(%s)",(course_id,))
        teachers_data=cursor.fetchall()
        teachers_names=[teacher[1] for teacher in teachers_data]
        teachers_ids={teacher_id[1]:teacher_id[0] for teacher_id in teachers_data}

        subject_names = [subject[1] for subject in subjects_data]
        subject_ids = {subjectID[1]: subjectID[0] for subjectID in subjects_data}

        subject_label = ttk.Label(left_frame, text="Select Subject:", font=("Helvetica", 12))
        subject_label.grid(pady=10)
        subject_combobox = ttk.Combobox(left_frame, values=subject_names, width=30)
        subject_combobox.set(subject_names[0])  # Default selection
        subject_combobox.grid(pady=5)

        teacher_label = ttk.Label(right_frame, text="Select teacher :", font=("Helvetica", 12))
        teacher_label.grid(pady=10)
        teacher_combobox = ttk.Combobox(right_frame, values=teachers_names, width=30)
        teacher_combobox.set(teachers_names[0])  # Default selection
        teacher_combobox.grid(pady=5)

    submit_button = ttk.Button(middle_frame, text="Get Fields", bootstyle="primary", command=getSubjectAndTeacher)
    submit_button.grid(pady=20)


    # subject_label = ttk.Label(input_frame, text="Subject Name:")
    # subject_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    #
    # subject_name = ttk.Entry(input_frame)
    # subject_name.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    #
    # # Create a label and combobox for Teacher Selection
    # teacher_label = ttk.Label(input_frame, text="Select Teacher:")
    # teacher_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # Sample list of teachers (can be dynamically fetched from the database)
    # teachers_list = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4"]
    #
    # teacher_combobox = ttk.Combobox(input_frame, values=teachers_list, state="readonly")
    # teacher_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ew")



    # Add timetable Button
    def set_timetable_attributes():
            pass


    submit_button = ttk.Button(add_timetable_window, text="Set Attributes", bootstyle="primary", command=set_timetable_attributes)
    submit_button.grid(pady=20)


    add_timetable_window.mainloop()
