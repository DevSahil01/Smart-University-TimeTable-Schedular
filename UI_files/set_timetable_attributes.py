import ttkbootstrap as ttk
from tkinter import messagebox
from tkinter import StringVar

from UI_files.generate_timetable_window import open_generate_timetable_window_UI
from util_constants import getPracticalBatches,getDivisions




def open_timetable_attributes(conn):
    add_timetable_window = ttk.Toplevel()  # Create a new top-level window
    add_timetable_window.title("Add timetable")
    add_timetable_window.geometry("1400x700")

    width = 1400
    height = 700

    # Get the screen width and height to center the window
    screen_width = add_timetable_window.winfo_screenwidth()
    screen_height = add_timetable_window.winfo_screenheight()

    # Set the window position and size
    add_timetable_window.geometry(f"{add_timetable_window.winfo_screenwidth()}x{add_timetable_window.winfo_screenheight()}+0+0")

    horizontal_frame1 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame1.pack(pady=5, padx=20, fill="x")

    horizontal_frame2 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame2.pack(pady=5, padx=20, fill="x")

    horizontal_frame3 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame3.pack(pady=5, padx=20, fill="x")

    horizontal_frame4 = ttk.Frame(add_timetable_window, padding=10)
    horizontal_frame4.pack(pady=5, padx=20, fill="x")


    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM course")
    courses = cursor.fetchall()



    course_names = [course[1] for course in courses]
    course_ids = {course[1]: course[0] for course in courses}

    year_label = ttk.Label(horizontal_frame1, text="Select Year:", font=("Helvetica", 12))
    year_label.pack(side="left", padx=5)
    year_combobox = ttk.Combobox(horizontal_frame1, values=[2022,2023,2024,2025], width=30)
    year_combobox.set(2024)  # Default selection
    year_combobox.pack(side="left", padx=5)

    course_label = ttk.Label(horizontal_frame1, text="Course Name:", font=("Helvetica", 12))
    course_label.pack(side="left",padx=5)
    course_combobox = ttk.Combobox(horizontal_frame1, values=course_names, width=30)
    course_combobox.set(course_names[0])
    course_combobox.pack(side="left", padx=5)

    semester_label = ttk.Label(horizontal_frame1, text="Select Semester:", font=("Helvetica", 12))
    semester_label.pack(side="left", padx=5)
    semester_combobox = ttk.Combobox(horizontal_frame1, values=[1, 2, 3, 4, 5, 6, 7, 8], width=30)
    semester_combobox.set(1)  # Default selection
    semester_combobox.pack(side="left", padx=5)

    division_var = StringVar()
    batch_var = StringVar()
    teacher_var=StringVar()
    subject_var = StringVar()
    prac_room_var=StringVar()


    batch_id=[]

    attribute_data_for_teachers=[]
    attribute_data_for_rooms=[]

    def get_subject_type(subjects, subject_name):
        for subject in subjects:
            if subject[1].lower() == subject_name.lower():
                return subject[2]
        return None

    def on_subject_selected(event,subject_data,subject,batch):
        selected_subject = subject.get()
        subject_type = get_subject_type(subject_data, selected_subject)
        divisions=getDivisions(batch[0])
        prac_batches=getPracticalBatches(batch[1])
        cursor=conn.cursor()
        cursor.execute("select room_id,room_no from rooms where room_type=(%s)",("practical_lab",))
        prac_lab_rooms=cursor.fetchall()

        prac_room_num=[room[1] for room in prac_lab_rooms]
        prac_room_ids={room[1]: room[0] for room in prac_lab_rooms}

        if hasattr(on_subject_selected, 'current_dropdown'):
            on_subject_selected.current_dropdown.pack_forget()

        if hasattr(on_subject_selected, 'current_prac_room_dropdown'):
            on_subject_selected.current_prac_room_dropdown.pack_forget()

        if hasattr(on_subject_selected,'current_label'):
            on_subject_selected.current_label.pack_forget()


        if subject_type=="Theory":
            division_combobox = ttk.Combobox(horizontal_frame3,textvariable=division_var, values=divisions, width=30)
            division_combobox.set(divisions[0])  # Default selection
            division_combobox.pack(side="left", pady=5)
            on_subject_selected.current_dropdown = division_combobox
        else:
            batch_combobox = ttk.Combobox(horizontal_frame3,textvariable=batch_var, values=prac_batches, width=30)
            batch_combobox.set(prac_batches[0])  # Default selection
            batch_combobox.pack(side="left", pady=5)
            on_subject_selected.current_dropdown = batch_combobox


            prac_room_combobox = ttk.Combobox(horizontal_frame3, textvariable=prac_room_var, values=prac_room_num, width=30)
            prac_room_combobox.set(prac_room_num[0])
            prac_room_combobox.pack(side="left", pady=5)
            on_subject_selected.current_prac_room_dropdown=prac_room_combobox




    def add_to_table(teacher, subject, division, batch,batch_room):

        newAttribute={}
        # Check if fields are filled
        attribute_data_for_rooms.append({batch:batch_room})

        def getRoomNumber(division,batch):
            if division:
               return next((room[division] for room in attribute_data_for_rooms if division in room), None)
            else:
                return next((room[batch] for room in attribute_data_for_rooms if batch in room ),None)


        newAttribute[subject]=teacher
        if division :
            newAttribute["division"]=division
        else :
            newAttribute["batch"]=batch


        if not teacher or not subject or (not division and not batch):
            messagebox.showwarning("Input Error", "Please fill all fields!",parent=add_timetable_window)
            return

        # Decide between Division or Batch
        group = division if division else batch

        newAttribute['room_no']=getRoomNumber(division,batch)

        # Insert into the Treeview Table
        teacher_table.insert("", "end", values=(teacher, subject, group,getRoomNumber(division,batch)))

        attribute_data_for_teachers.append(newAttribute)

        teacher_var.set("")
        subject_var.set("")
        division_var.set("")
        batch_var.set("")

        # Clear selections after adding

    def allotRoom(division,roomNo):
        if division and roomNo:
            newAllotment={}
            newAllotment[division]=roomNo
            attribute_data_for_rooms.append(newAllotment)
            messagebox.showinfo("Room Allotment","Room "+str(roomNo)+" is alloted to "+ division ,parent=add_timetable_window)
        else:
            messagebox.showwarning("Input Error","Select all fields",parent=add_timetable_window)


    def setBatchId(year,courseId):
         cursor=conn.cursor()
         cursor.execute("select batch_id from batch where batch_year=(%s) and course_id=(%s)",(year,courseId))
         b_id=cursor.fetchall()
         batch_id.append(b_id[0][0])

    def getSubjectAndTeacher():
        course_id=course_ids.get(course_combobox.get())
        cursor = conn.cursor()
        cursor.execute("select subject_id,subject_name,subject_type from subjects where course_id=(%s) and semester=(%s)",
                       (course_id, semester_combobox.get()))
        subjects_data = cursor.fetchall()
        year=year_combobox.get()
        cursor.execute(
            "SELECT * FROM batch WHERE batch_year=(%s) AND course_id=(%s)",(year,course_ids.get(course_combobox.get())))
        batch_data = cursor.fetchall()
        setBatchId(year,course_id)



        if len(subjects_data)>0 and len(batch_data):
            cursor=conn.cursor()
            cursor.execute("select teacher_id,teacher_name from teachers where course_id=(%s)",(course_id,))
            teachers_data=cursor.fetchall()
            teachers_names=[teacher[1] for teacher in teachers_data]
            teachers_ids={teacher_id[1]:teacher_id[0] for teacher_id in teachers_data}

            subject_names = [subject[1] for subject in subjects_data]
            subject_ids = {subjectID[1]: subjectID[0] for subjectID in subjects_data}

            cursor = conn.cursor()
            cursor.execute("select room_id,room_no from rooms where room_type=(%s)", ("lecture_room",))
            rooms = cursor.fetchall()

            room_num = [room[1] for room in rooms]
            room_ids = {room[1]: room[0] for room in rooms}


            #get divisions and practical batches
            divisions=getDivisions(batch_data[0][3])
            prac_batches=getPracticalBatches(batch_data[0][4])

            #select rooms for division
            division_room_label = ttk.Label(horizontal_frame2, text="Select Division :", font=("Helvetica", 12))
            division_room_label.pack(side="left", padx=5)
            division_room_combobox = ttk.Combobox(horizontal_frame2, values=divisions, width=30)
            division_room_combobox.set(divisions[0])
            division_room_combobox.pack(side="left", padx=5)

            room_label = ttk.Label(horizontal_frame2, text="Select Room :", font=("Helvetica", 12))
            room_label.pack(side="left", padx=5)
            room_combobox = ttk.Combobox(horizontal_frame2, values=room_num, width=30)
            room_combobox.set(room_num[0])
            room_combobox.pack(side="left", padx=5)

            allot_room_button = ttk.Button(horizontal_frame2, text="Allot Room", bootstyle="primary",
                                           command=lambda:allotRoom(division_room_combobox.get(),
                                                                    room_combobox.get()))
            allot_room_button.pack(side="left", pady=20)



            #select subject
            subject_label = ttk.Label(horizontal_frame3, text="Select Subject:", font=("Helvetica", 12))
            subject_label.pack(side="left",pady=10,padx=10)
            subject_dropdown = ttk.Combobox(horizontal_frame3, textvariable=subject_var,values=[sub[1] for sub in subjects_data], state="readonly")
            subject_dropdown.pack(side="left",pady=20,padx=10)
            subject_dropdown.bind("<<ComboboxSelected>>",lambda event : on_subject_selected(event,subjects_data,subject_var,[batch_data[0][3],batch_data[0][4]]))

            teacher_label = ttk.Label(horizontal_frame3, text="Select teacher :", font=("Helvetica", 12))
            teacher_label.pack(side="left",pady=10,padx=10)
            teacher_combobox = ttk.Combobox(horizontal_frame3,textvariable=teacher_var, values=teachers_names, width=30)
            teacher_combobox.set(teachers_names[0])  # Default selection
            teacher_combobox.pack(side="left",pady=5,padx=10)

            division_label = ttk.Label(horizontal_frame3, text="Select Division/Batch :", font=("Helvetica", 12))
            division_label.pack(side="left", pady=10)

            add_button = ttk.Button(horizontal_frame3, text="add", bootstyle="primary",
                                    command=lambda :add_to_table(subject_var.get(),teacher_var.get(),division_var.get(),batch_var.get(),prac_room_var.get()))
            add_button.pack(side="right", pady=20,padx=10)


        else:
            messagebox.showwarning("Warning", "subject or batch are not added for this course",parent=add_timetable_window)


    submit_button = ttk.Button(horizontal_frame1, text="Get Fields", bootstyle="primary", command=getSubjectAndTeacher)
    submit_button.pack(side="left", pady=20)


    #<-- table from here --->

    style = ttk.Style()
    style.configure("Treeview",
                    font=("Helvetica", 10),
                    rowheight=30,
                    background="#f0f0f0",
                    foreground="black",
                    fieldbackground="#f0f0f0")
    style.map("Treeview", background=[('selected', '#5DADE2')])
    columns = ("Teacher", "Subject", "Division/Batch","Room Number")
    teacher_table = ttk.Treeview(horizontal_frame4, columns=columns, show="headings")

    for col in columns:
        teacher_table.heading(col, text=col)
        teacher_table.column(col, width=200, anchor="center")

    teacher_table.pack(fill="both", expand=True)


    def open_generate_timetable_window():
        open_generate_timetable_window_UI(conn,batch_id)





    # set Attributes for final timetable
    def set_timetable_attributes():
            cursor=conn.cursor()
            division = ""
            batch = ""

            print(attribute_data_for_rooms)
            # for row in attribute_data_for_rooms:
            #     div_or_batch=list(row.keys())[0]
            #     cursor=conn.cursor()
            #     cursor.execute(
            #         """INSERT INTO rooms_allotment (room_id, batch_id, div_batch, room_type)
            #     SELECT r.room_id, (%s), (%s), r.room_type
            #     FROM rooms r
            #     WHERE r.room_no = (%s)"""
            #     ,(batch_id[0],div_or_batch,row[div_or_batch]))
            #     conn.commit()



            print(attribute_data_for_teachers)

            for row in attribute_data_for_teachers:
                if list(row.keys()).__contains__("division"):
                    division=row['division']
                else:
                    batch=row['batch']
                teacher=list(row.keys())[0]
                subject=row[teacher]
                room_number=row['room_no']

                cursor.execute('''INSERT INTO subjecttoteacher (subject_id, teacher_id, batch_id, division, prac_batch, room_id)
                SELECT s.subject_id, t.teacher_id, (%s), (%s), (%s), r.room_id
                FROM subjects s
                JOIN teachers t ON t.teacher_name = (%s)
                JOIN rooms r ON r.room_no = (%s)
                WHERE s.subject_name = (%s);''',(batch_id[0],division,batch,teacher,room_number,subject))
                conn.commit()
            messagebox.showinfo("Success", "Attributes are set Successfully!",parent=add_timetable_window)
            add_timetable_window.destroy()
            open_generate_timetable_window()






    submit_button = ttk.Button(add_timetable_window, text="Set Attributes", bootstyle="primary", command=set_timetable_attributes)
    submit_button.pack(padx=20)



    add_timetable_window.mainloop()
