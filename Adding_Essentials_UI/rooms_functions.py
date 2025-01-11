import ttkbootstrap as ttk
from tkinter import messagebox


def open_add_rooms_form(conn):
    add_rooms_window = ttk.Toplevel()  # Create a new top-level window
    add_rooms_window.title("Add rooms")
    add_rooms_window.geometry("400x300")

    width = 400
    height = 450

    # Get the screen width and height to center the window
    screen_width = add_rooms_window.winfo_screenwidth()
    screen_height = add_rooms_window.winfo_screenheight()

    # Calculate the position to center the window
    x_position = (screen_width // 2) - (width // 2)
    y_position = (screen_height // 2) - (height // 2)

    # Set the window position and size
    add_rooms_window.geometry(f"{width}x{height}+{x_position}+{y_position}")


    rooms_types=["lecture_room","seminar_room","practical_lab"]

    # Add rooms Form Labels and Entries
    rooms_number_label = ttk.Label(add_rooms_window, text="Rooms Number:", font=("Helvetica", 12))
    rooms_number_label.pack(pady=10)
    rooms_number_entry = ttk.Entry(add_rooms_window, width=30)
    rooms_number_entry.pack(pady=5)

    room_capacity_lable=ttk.Label(add_rooms_window,text="Room capacity",font=("Helvetica",12))
    room_capacity_lable.pack(pady=10)
    room_capacity_entry = ttk.Entry(add_rooms_window, width=30)
    room_capacity_entry.pack(pady=5)

    room_type_label = ttk.Label(add_rooms_window, text="Room Type:", font=("Helvetica", 12))
    room_type_label.pack(pady=10)
    room_type_combobox = ttk.Combobox(add_rooms_window, values=rooms_types, width=30)
    room_type_combobox.set(rooms_types[0])  # Default selection
    room_type_combobox.pack(pady=5)



    # Add rooms Button
    def submit_rooms():
        rooms_name = rooms_number_entry.get()
        capacity=room_capacity_entry.get()
        room_type=room_type_combobox.get()


        if rooms_name and capacity and room_type:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO rooms (room_no,capacity,room_type)  VALUES (%s,%s,%s)",(rooms_name,capacity,room_type))
            conn.commit()
            messagebox.showinfo("Success", "rooms Added Successfully!")
            add_rooms_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    submit_button = ttk.Button(add_rooms_window, text="Add rooms", bootstyle="primary", command=submit_rooms)
    submit_button.pack(pady=20)


    add_rooms_window.mainloop()
