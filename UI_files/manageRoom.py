from ttkbootstrap import ttk
from tkinter import Toplevel, messagebox
from tkinter.simpledialog import askstring

def open_manage_room_UI(conn):
    def edit_room(room_id):
        # Prompt user to enter new data for the room
        room_no = askstring("Edit Room", "Enter the new room number:")
        capacity = askstring("Edit Room", "Enter the new room capacity:")
        room_type = askstring("Edit Room", "Enter the new room type:")

        # If the user provided valid values, proceed with updating the room record
        if room_no and capacity and room_type:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE rooms
                    SET room_no = %s, capacity = %s, room_type = %s
                    WHERE room_id = %s
                """, (room_no, capacity, room_type, room_id))
                conn.commit()
                messagebox.showinfo("Success", "Room updated successfully!")
                refresh_treeview()  # Refresh the Treeview to show updated data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update room: {e}")
        else:
            messagebox.showerror("Error", "Invalid input. Please fill all fields.")

    def delete_room(room_id):
        # Ask for confirmation before deleting
        confirm = messagebox.askyesno("Delete Room", "Are you sure you want to delete this room?")
        if confirm:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
                conn.commit()
                messagebox.showinfo("Success", "Room deleted successfully!")
                refresh_treeview()  # Refresh the Treeview to remove the deleted row
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete room: {e}")

    def refresh_treeview():
        # Clear the Treeview
        for row in tree.get_children():
            tree.delete(row)

        # Fetch updated data and repopulate the Treeview
        cursor = conn.cursor()
        query = """
            SELECT 
                room_id, 
                room_no, 
                capacity, 
                room_type
            FROM 
                rooms
        """
        cursor.execute(query)
        room_data = cursor.fetchall()

        if not room_data:
            messagebox.showinfo("No Data", "No records found in the rooms table.")
            return

        for row in room_data:
            # Add the Edit and Delete buttons in front of each row
            tree.insert("", "end", values=(row[1], row[2], row[3], "Edit", "Delete"), tags=(row[0],))

    # Create a new window for managing rooms
    manage_room_window = Toplevel()
    manage_room_window.title("Manage Rooms")
    manage_room_window.geometry("600x500")

    # Add a frame to hold the Treeview
    frame = ttk.Frame(manage_room_window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a Treeview widget to display room data
    columns = ("Room Number", "Capacity", "Room Type", "Edit", "Delete")
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

        # Get the room ID and clicked column
        room_id = tree.item(selected_item)["tags"][0]
        column = tree.identify_column(event.x)

        if column == "#4":  # Edit button clicked
            edit_room(room_id)
        elif column == "#5":  # Delete button clicked
            delete_room(room_id)

    # Bind the Treeview click event
    tree.bind("<Button-1>", on_tree_click)

    # Populate the Treeview with data
    refresh_treeview()

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Add a close button
    close_button = ttk.Button(manage_room_window, text="Close", bootstyle="danger", command=manage_room_window.destroy)
    close_button.pack(pady=10)
