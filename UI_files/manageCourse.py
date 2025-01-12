


def open_manage_course_UI(conn):
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM course")
    course_data=cursor.fetchall()
    print(course_data)
     # UI

    # course_name  |  actions
    # MCA          |   Edit  Delete
    # MMS           | edit    delete


