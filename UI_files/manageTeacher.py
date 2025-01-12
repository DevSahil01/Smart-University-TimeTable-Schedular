

def open_manage_teacher_UI(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    course_data = cursor.fetchall()

    # write query to get all teachers data but course_id which is foreign key get the name of that course instead of id
   # teachername | available days | coursename



