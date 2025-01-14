
from ttkbootstrap import ttk
from tkinter import Toplevel, messagebox
from tkinter.simpledialog import askstring

def open_manage_course_UI(conn):
    def edit_course(course_id):
        # Prompt user to enter a new course name
        new_name = askstring("Edit Course", "Enter the new course name:")
        if new_name:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE course SET course_name = %s WHERE course_id = %s", (new_name, course_id))
                conn.commit()
                messagebox.showinfo("Success", "Course updated successfully!")
                refresh_treeview()  # Refresh the Treeview to show updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course: {e}")

    def delete_course(course_id):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete Course", "Are you sure you want to delete this course?")
        if confirm:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
                conn.commit()
                messagebox.showinfo("Success", "Course deleted successfully!")
                refresh_treeview()  # Refresh the Treeview to remove the deleted row
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course: {e}")

    def refresh_treeview():
        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data and repopulate the Treeview
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name FROM course")
        course_data = cursor.fetchall()

        for row in course_data:
            # Add the Edit and Delete buttons in front of each row
            tree.insert("", "end", values=row)

    # Create a new window for managing courses
    manage_course_window = Toplevel()
    manage_course_window.title("Manage Courses")
    manage_course_window.geometry("500x500")

    # Add a frame to hold the Treeview
    frame = ttk.Frame(manage_course_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a Treeview widget to display course data
    columns = ("Course ID", "Course Name", "Edit", "Delete")
    tree = ttk.Treeview(frame, columns=columns, show="headings", bootstyle="info")
    tree.pack(fill="both", expand=True)

    # Set column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # Add Edit and Delete buttons in the Treeview
    def insert_buttons():
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name FROM course")
        course_data = cursor.fetchall()

        for course_id, course_name in course_data:
            tree.insert(
                "",
                "end",
                values=(course_id, course_name, "Edit", "Delete"),
                tags=(course_id,),
            )

    def on_tree_click(event):
        selected_item = tree.identify_row(event.y)
        if not selected_item:
            return

        # Get the course ID and clicked column
        course_id = tree.item(selected_item)["values"][0]
        column = tree.identify_column(event.x)

        if column == "#3":  # Edit button clicked
            edit_course(course_id)
        elif column == "#4":  # Delete button clicked
            delete_course(course_id)

    # Bind the Treeview click event
    tree.bind("<Button-1>", on_tree_click)

    # Populate the Treeview with data
    insert_buttons()

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    close_button = ttk.Button(manage_course_window, text="Close", bootstyle="danger", command=manage_course_window.destroy)
    close_button.pack(pady=10)
# =======
# import ttkbootstrap as ttk
#
#
# def open_manage_course_UI(conn):
#     cursor=conn.cursor()
#     cursor.execute("SELECT * FROM course")
#     course_data=cursor.fetchall()
#     print(course_data)
#
#     manage_teacher_window = ttk.Toplevel()  # Create a new top-level window
#     manage_teacher_window.title("Add teacher")
#     manage_teacher_window.geometry("400x300")
#
#     width = 800
#     height = 450
#
#     # Get the screen width and height to center the window
#     screen_width = manage_teacher_window.winfo_screenwidth()
#     screen_height = manage_teacher_window.winfo_screenheight()
#
#     # Calculate the position to center the window
#     x_position = (screen_width // 2) - (width // 2)
#     y_position = (screen_height // 2) - (height // 2)
#
#     # Set the window position and size
#     manage_teacher_window.geometry(f"{width}x{height}+{x_position}+{y_position}")
#
#     course_label = ttk.Label(manage_teacher_window, text="courses data", font=("Helvetica", 12))
#     course_label.grid(pady=10)
#
#
#      # UI
#
#     # course_name  |  actions
#     # MCA          |   Edit  Delete
#     # MMS           | edit    delete
#
#
# >>>>>>> otherUpdates-local
