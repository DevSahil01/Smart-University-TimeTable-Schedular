from ttkbootstrap import ttk
from tkinter import Toplevel, messagebox
from tkinter.simpledialog import askstring

def open_manage_subject_UI(conn):
    def edit_subject(subject_id):
        # Prompt user to enter new data for the subject
        subject_name = askstring("Edit Subject", "Enter the new subject name:")
        semester = askstring("Edit Subject", "Enter the new semester:")
        subject_type = askstring("Edit Subject", "Enter the new subject type:")
        
        # Fetch available courses for selection
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name FROM course")
        courses = cursor.fetchall()
        
        # Create a dictionary of course names and their IDs
        course_dict = {course[1]: course[0] for course in courses}
        course_name = askstring("Edit Subject", "Enter the course name from the following: \n" + "\n".join(course_dict.keys()))

        # If the user provided valid values, proceed with updating the subject record
        if subject_name and semester and subject_type and course_name and course_name in course_dict:
            course_id = course_dict[course_name]  # Get the course_id from course name
            try:
                cursor.execute("""
                    UPDATE subjects
                    SET subject_name = %s, semester = %s, subject_type = %s, course_id = %s
                    WHERE subject_id = %s
                """, (subject_name, semester, subject_type, course_id, subject_id))
                conn.commit()
                messagebox.showinfo("Success", "Subject updated successfully!")
                refresh_treeview()  # Refresh the Treeview to show updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update subject: {e}")
        else:
            messagebox.showerror("Error", "Invalid input or course name not found.")

    def delete_subject(subject_id):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete Subject", "Are you sure you want to delete this subject?")
        if confirm:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM subjects WHERE subject_id = %s", (subject_id,))
                conn.commit()
                messagebox.showinfo("Success", "Subject deleted successfully!")
                refresh_treeview()  # Refresh the Treeview to remove the deleted row
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete subject: {e}")

    def refresh_treeview():
        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data and repopulate the Treeview
        cursor = conn.cursor()
        query = """
            SELECT 
                subject_id, 
                subject_name, 
                semester, 
                subject_type, 
                course.course_name 
            FROM 
                subjects 
            LEFT JOIN 
                course 
            ON 
                subjects.course_id = course.course_id
        """
        cursor.execute(query)
        subject_data = cursor.fetchall()

        if not subject_data:
            messagebox.showinfo("No Data", "No records found in the subjects table.")
            return

        for row in subject_data:
            # Add the Edit and Delete buttons in front of each row
            tree.insert("", "end", values=(row[1], row[2], row[3], row[4], "Edit", "Delete"), tags=(row[0],))

    # Create a new window for managing subjects
    manage_subject_window = Toplevel()
    manage_subject_window.title("Manage Subjects")
    manage_subject_window.geometry("700x500")

    # Add a frame to hold the Treeview
    frame = ttk.Frame(manage_subject_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a Treeview widget to display subject data
    columns = ("Subject Name", "Semester", "Subject Type", "Course Name", "Edit", "Delete")
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

        # Get the subject ID and clicked column
        subject_id = tree.item(selected_item)["tags"][0]
        column = tree.identify_column(event.x)

        if column == "#5":  # Edit button clicked
            edit_subject(subject_id)
        elif column == "#6":  # Delete button clicked
            delete_subject(subject_id)

    # Bind the Treeview click event
    tree.bind("<Button-1>", on_tree_click)

    # Populate the Treeview with data
    refresh_treeview()

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    close_button = ttk.Button(manage_subject_window, text="Close", bootstyle="danger", command=manage_subject_window.destroy)
    close_button.pack(pady=10)
