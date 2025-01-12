from ttkbootstrap import ttk
from tkinter import Toplevel, messagebox
from tkinter.simpledialog import askstring

def open_manage_batch_UI(conn):
    def edit_batch(batch_id):
        # Prompt user to enter new data for the batch
        batch_year = askstring("Edit Batch", "Enter the new batch year:")
        no_of_students = askstring("Edit Batch", "Enter the new number of students:")
        no_of_divisions = askstring("Edit Batch", "Enter the new number of divisions:")
        no_of_prac_batches = askstring("Edit Batch", "Enter the new number of practical batches:")
        
        # Fetch available courses for selection
        cursor = conn.cursor()
        cursor.execute("SELECT course_id, course_name FROM course")
        courses = cursor.fetchall()
        
        # Create a dictionary of course names and their IDs
        course_dict = {course[1]: course[0] for course in courses}
        course_name = askstring("Edit Batch", "Enter the course name from the following: \n" + "\n".join(course_dict.keys()))

        # If the user provided valid values, proceed with updating the batch record
        if batch_year and no_of_students and no_of_divisions and no_of_prac_batches and course_name and course_name in course_dict:
            course_id = course_dict[course_name]  # Get the course_id from course name
            try:
                cursor.execute("""
                    UPDATE batch
                    SET batch_year = %s, no_of_students = %s, no_of_divisions = %s, no_of_prac_batches = %s, course_id = %s
                    WHERE batch_id = %s
                """, (batch_year, no_of_students, no_of_divisions, no_of_prac_batches, course_id, batch_id))
                conn.commit()
                messagebox.showinfo("Success", "Batch updated successfully!")
                refresh_treeview()  # Refresh the Treeview to show updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update batch: {e}")
        else:
            messagebox.showerror("Error", "Invalid input or course name not found.")

    def delete_batch(batch_id):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete Batch", "Are you sure you want to delete this batch?")
        if confirm:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM batch WHERE batch_id = %s", (batch_id,))
                conn.commit()
                messagebox.showinfo("Success", "Batch deleted successfully!")
                refresh_treeview()  # Refresh the Treeview to remove the deleted row
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete batch: {e}")

    def refresh_treeview():
        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data and repopulate the Treeview
        cursor = conn.cursor()
        query = """
            SELECT 
                batch.batch_id, 
                batch.batch_year, 
                batch.no_of_students, 
                batch.no_of_divisions, 
                batch.no_of_prac_batches, 
                course.course_name 
            FROM 
                batch 
            LEFT JOIN 
                course 
            ON 
                batch.course_id = course.course_id
        """
        cursor.execute(query)
        batch_data = cursor.fetchall()

        if not batch_data:
            messagebox.showinfo("No Data", "No records found in the batch table.")
            return

        for row in batch_data:
            # Add the Edit and Delete buttons in front of each row
            tree.insert("", "end", values=(row[1], row[2], row[3], row[4], row[5], "Edit", "Delete"), tags=(row[0],))

    # Create a new window for managing batches
    manage_batch_window = Toplevel()
    manage_batch_window.title("Manage Batches")
    manage_batch_window.geometry("800x500")

    # Add a frame to hold the Treeview
    frame = ttk.Frame(manage_batch_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a Treeview widget to display batch data
    columns = ("Batch Year", "No. of Students", "No. of Divisions", "No. of Practical Batches", "Course Name", "Edit", "Delete")
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

        # Get the batch ID and clicked column
        batch_id = tree.item(selected_item)["tags"][0]
        column = tree.identify_column(event.x)

        if column == "#6":  # Edit button clicked
            edit_batch(batch_id)
        elif column == "#7":  # Delete button clicked
            delete_batch(batch_id)

    # Bind the Treeview click event
    tree.bind("<Button-1>", on_tree_click)

    # Populate the Treeview with data
    refresh_treeview()

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    close_button = ttk.Button(manage_batch_window, text="Close", bootstyle="danger", command=manage_batch_window.destroy)
    close_button.pack(pady=10)
