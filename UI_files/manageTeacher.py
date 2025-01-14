
from ttkbootstrap import ttk
from tkinter import Toplevel, messagebox
from tkinter.simpledialog import askstring

def open_manage_teacher_UI(conn):
    def edit_teacher(teacher_id):
        # Prompt user to enter new data for the teacher
        teacher_name = askstring("Edit Teacher", "Enter the new teacher name:")
        available_days = askstring("Edit Teacher", "Enter the new available days:")
        # Fetch available courses for selection
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name FROM course")
        courses = cursor.fetchall()
        
        # Create a dictionary of course names and their IDs
        course_dict = {course[1]: course[0] for course in courses}
        course_name = askstring("Edit Teacher", "Enter the course name from the following: \n" + "\n".join(course_dict.keys()))

        # If the user provided valid values, proceed with updating the teacher record
        if teacher_name and available_days and course_name and course_name in course_dict:
            course_id = course_dict[course_name]  # Get the course_id from course name
            try:
                cursor.execute("""
                    UPDATE teachers
                    SET teacher_name = %s, available_days = %s, course_id = %s
                    WHERE teacher_id = %s
                """, (teacher_name, available_days, course_id, teacher_id))
                conn.commit()
                messagebox.showinfo("Success", "Teacher updated successfully!")
                refresh_treeview()  # Refresh the Treeview to show updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update teacher: {e}")
        else:
            messagebox.showerror("Error", "Invalid input or course name not found.")

    def delete_teacher(teacher_id):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete Teacher", "Are you sure you want to delete this teacher?")
        if confirm:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
                conn.commit()
                messagebox.showinfo("Success", "Teacher deleted successfully!")
                refresh_treeview()  # Refresh the Treeview to remove the deleted row
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete teacher: {e}")

    def refresh_treeview():
        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data and repopulate the Treeview
        cursor = conn.cursor()
        query = """
            SELECT 
                teachers.teacher_id, 
                teachers.teacher_name, 
                teachers.available_days, 
                course.course_name 
            FROM 
                teachers 
            LEFT JOIN 
                course 
            ON 
                teachers.course_id = course.course_id
        """
        cursor.execute(query)
        teacher_data = cursor.fetchall()

        if not teacher_data:
            messagebox.showinfo("No Data", "No records found in the teachers table.")
            return

        for row in teacher_data:
            # Add the Edit and Delete buttons in front of each row
            tree.insert("", "end", values=(row[1], row[2], row[3], "Edit", "Delete"), tags=(row[0],))

    # Create a new window for managing teachers
    manage_teacher_window = Toplevel()
    manage_teacher_window.title("Manage Teachers")
    manage_teacher_window.geometry("600x500")

    # Add a frame to hold the Treeview
    frame = ttk.Frame(manage_teacher_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a Treeview widget to display teacher data
    columns = ("Teacher Name", "Available Days", "Course Name", "Edit", "Delete")
    tree = ttk.Treeview(frame, columns=columns, show="headings", bootstyle="info")
    tree.pack(fill="both", expand=True)

    # Set column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    # Handle Treeview clicks for Edit and Delete
    def on_tree_click(event):
        selected_item = tree.identify_row(event.y)
        if not selected_item:
            return

        # Get the teacher ID and clicked column
        teacher_id = tree.item(selected_item)["tags"][0]
        column = tree.identify_column(event.x)

        if column == "#4":  # Edit button clicked
            edit_teacher(teacher_id)
        elif column == "#5":  # Delete button clicked
            delete_teacher(teacher_id)

    # Bind the Treeview click event
    tree.bind("<Button-1>", on_tree_click)

    # Populate the Treeview with data
    refresh_treeview()

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    close_button = ttk.Button(manage_teacher_window, text="Close", bootstyle="danger", command=manage_teacher_window.destroy)
    close_button.pack(pady=10)




