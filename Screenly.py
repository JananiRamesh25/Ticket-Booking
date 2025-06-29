import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk

# Global variables for user data and movie booking
user_data = {}
seating_data = {}

# Constants for ticket pricing
ticket_price = 100.0  # Base price per ticket
tax_rate = 0.18  # Tax rate (18%)
service_charge = 20.0  # Flat service charge per ticket


def show_frame(frame):
    frame.tkraise()


def handle_signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()

    if username and password:
        user_data[username] = password
        messagebox.showinfo("Signup", "Signup successful! Please login.")
        show_frame(login_frame)
    else:
        messagebox.showerror("Signup Error", "Please enter both username and password.")


def handle_login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username in user_data and user_data[username] == password:
        show_frame(main_page_frame)
        display_images()
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")
        # After failed login, show an option to go to the signup page
        show_signup_button()
def show_signup_button():
    signup_prompt_label = tk.Label(login_frame, text="Not a user? Sign Up Now!", fg="red", font=("Arial", 12, "italic"))
    signup_prompt_label.pack(pady=10)

    signup_button = tk.Button(login_frame, text="Go to Signup", bg='#EDF9EB', font=('Helvetica', 12), command=lambda: show_frame(signup_frame))
    signup_button.pack(pady=10)

def display_images():
    for widget in image_frame.winfo_children():
        widget.destroy()

    image_paths = [
        ('C:/Users/Admin/Downloads/amaran.jpeg', 'Amaran'),
        ('C:/Users/Admin/Downloads/dear comrade.jpeg', 'Dear Comrade'),
        ('C:/Users/Admin/Downloads/vtv.jpeg', 'VTV'),
        ('C:/Users/Admin/Downloads/shershaah.jpeg', 'Shershaah')
        
    ]
    
    for path, title in image_paths:
        image = Image.open(path)
        new_size = (200, 150)
        res = image.resize(new_size)
        photo = ImageTk.PhotoImage(res)
        
        movie_frame = tk.Frame(image_frame)
        movie_frame.pack(side="left", padx=20, pady=20)

        label = tk.Label(movie_frame, image=photo)
        label.image = photo  
        label.pack()

        button = tk.Button(movie_frame, text=f"Book Ticket for {title}", bg='#EDF9EB', font=('Helvetica', 12), command=lambda m=title: show_theater_selection(m))
        button.pack(pady=10)


def show_theater_selection(movie_name):
    theaters = ["INOX", "PVR cinemas", "BROADWAY cinemas","KG cinemas","CINEPOLIS"]

    theater_window = tk.Toplevel(root)
    theater_window.title(f"Select Theater for {movie_name}")
    
    movie_label = tk.Label(theater_window, text=f"Select Theater for {movie_name}", font=("Raleway", 16))
    movie_label.pack(pady=10)
    
    def select_theater(theater):
        show_showtimes_and_dates(movie_name, theater)
        theater_window.destroy()

    for theater in theaters:
        tk.Button(theater_window, text=theater, bg='#EDF9EB', command=lambda t=theater: select_theater(t)).pack(pady=5)


def show_showtimes_and_dates(movie_name, theater_name):
    showtimes = ["10:00 AM", "1:00 PM", "4:00 PM", "7:00 PM","10:00 PM"]
    dates = ["Dec 15, 2024", "Dec 16, 2024", "Dec 17, 2024"]

    showtime_window = tk.Toplevel(root)
    showtime_window.title(f"Select Showtime and Date for {movie_name} at {theater_name}")
    
    movie_label = tk.Label(showtime_window, text=f"Select Showtime and Date for {movie_name} at {theater_name}", font=("Raleway", 16))
    movie_label.pack(pady=10)
    
    showtime_var = tk.StringVar(value=showtimes[0])
    for time in showtimes:
        tk.Radiobutton(showtime_window, text=time, variable=showtime_var, value=time).pack(anchor="w")

    date_var = tk.StringVar(value=dates[0])
    for date in dates:
        tk.Radiobutton(showtime_window, text=date, variable=date_var, value=date).pack(anchor="w")
    
    def confirm_booking():
        selected_showtime = showtime_var.get()
        selected_date = date_var.get()
        show_seating_selection(movie_name, theater_name, selected_date, selected_showtime)
        showtime_window.destroy()

    confirm_button = tk.Button(showtime_window, text="Confirm Showtime and Date", bg='#EDF9EB', command=confirm_booking)
    confirm_button.pack(pady=10)


def show_seating_selection(movie_name, theater_name, selected_date, selected_showtime):
    seat_window = tk.Toplevel(root)
    seat_window.title(f"Select Seats for {movie_name} at {theater_name}")
    
    seats = {}
    selected_seats = set()  # Set to track selected seats
    
    # Create seat buttons (10 rows and 10 columns)
    for row in range(1, 11):
        for col in range(1, 11):
            seat_id = f"R{row}C{col}"
            button = tk.Button(seat_window, text=seat_id, width=5, height=2)
            button.grid(row=row, column=col, padx=5, pady=5)
            seats[seat_id] = button

            button.config(command=lambda s=seat_id, b=button: toggle_seat_selection(s, b, selected_seats))

    selected_seats_label = tk.Label(seat_window, text="Selected Seats: ", font=("Raleway", 16))
    selected_seats_label.grid(row=11, column=0, columnspan=5)

    def toggle_seat_selection(seat_id, button, selected_seats):
        if seat_id not in selected_seats:
            selected_seats.add(seat_id)
            button.config(bg="green")
        else:
            selected_seats.remove(seat_id)
            button.config(bg="SystemButtonFace")
        
        selected_seats_label.config(text=f"Selected Seats: {', '.join(selected_seats)}", font=("Raleway", 16))
        button.update_idletasks()

    def confirm_seating():
        # Calculate the total cost based on the number of selected seats
        num_tickets = len(selected_seats)
        if num_tickets > 0:
            base_amount = ticket_price * num_tickets
            tax_amount = base_amount * tax_rate
            service_charge_total = service_charge * num_tickets
            total_amount = base_amount + tax_amount + service_charge_total

            # Show the billing page in a new window
            show_billing_page(movie_name, theater_name, selected_date, selected_showtime, selected_seats, base_amount, tax_amount, service_charge_total, total_amount)
            seat_window.destroy()
        else:
            messagebox.showerror("Error", "Please select at least one seat.")

    confirm_seating_button = tk.Button(seat_window, text="Confirm Seats", bg='#EDF9EB', font=("Times New Roman", 16), command=confirm_seating)
    confirm_seating_button.grid(row=12, column=0, columnspan=5, pady=10)


import tkinter as tk

def show_billing_page(movie_name, theater_name, selected_date, selected_showtime, selected_seats, base_amount, tax_amount, service_charge_total, total_amount): 
    # Create a new top-level window for billing details
    billing_window = tk.Toplevel(root)
    billing_window.title("Booking Confirmation and Billing")
    
    # Title for the billing window
    billing_label = tk.Label(billing_window, text="Booking Confirmation", font=("Raleway", 16,"bold"))
    billing_label.pack(pady=10)
    
    # Format and display the billing details
    details = f"""
    Movie: {movie_name}
    Theater: {theater_name}
    Showtime: {selected_showtime}
    Date: {selected_date}
    Selected Seats: {', '.join(selected_seats)}
    
    Base Price: {base_amount:.2f}
    Tax: {tax_amount:.2f}
    Service Charge: {service_charge_total:.2f}
    Total Amount: {total_amount:.2f}
    """
    
    # Label to show all the details
    details_label = tk.Label(billing_window, text=details, font=("Raleway", 12))
    details_label.pack(pady=20)
    
    # Gratitude message after the billing details
    gratitude_msg1 = """You’ve got the tickets, Popcorn ready? Movie’s set? Now all that’s missing is you!
    Thanks for booking with us!"""
    gratitude_label1 = tk.Label(billing_window, text=gratitude_msg1, font=("Raleway", 12, "italic"), fg="green")
    gratitude_label1.pack(pady=10)
    
    # Special offer message
    gratitude_msg2 = """Get 10% off on your next booking with code 'MOVIE10'.
    Book soon, this offer won’t last forever!"""
    gratitude_label2 = tk.Label(billing_window, text=gratitude_msg2, font=("Times New Roman", 12), fg="blue")
    gratitude_label2.pack(pady=10)
    
    # Close button to exit the billing window
    close_button = tk.Button(billing_window, text="Close", bg='#EDF9EB', command=billing_window.destroy)
    close_button.pack(pady=10)



# Main application window
root = tk.Tk()
root.title("Screenly")
root.geometry("2000x1000")

# Frames for different sections
signup_frame = tk.Frame(root)
login_frame = tk.Frame(root)
main_page_frame = tk.Frame(root)
welcome_frame= tk.Frame(root)

for frame in (welcome_frame,signup_frame, login_frame, main_page_frame):
    frame.place(x=0, y=0, width=1550, height=800)


def set_background(frame, image_path):
    image = Image.open(image_path)
    image = image.resize((1550, 800))
    bg_image = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(frame, width=1550, height=800)
    canvas.place(x=0, y=0)
    canvas.create_image(0, 0, image=bg_image, anchor="nw")

    return canvas, bg_image


# Welcome frame (Opening screen with buttons for Login/Signup)
canvas_welcome, bg_image_welcome = set_background(welcome_frame, "C:/Users/Admin/Downloads/1 (1).jpg")
welcome_label = tk.Label(welcome_frame, text="Welcome to Screenly", bg='#FFFFFF', fg="#000000", font=("Times New Roman", 20, 'bold'))
welcome_label.pack(pady=20)

login_button = tk.Button(welcome_frame, text="Login", bg="#780606", fg="#FFFFFF", font=("Arial", 14), command=lambda: show_frame(login_frame))
login_button.pack(pady=10)

signup_button = tk.Button(welcome_frame, text="Sign Up", bg="#780606", fg="#FFFFFF", font=("Arial", 14), command=lambda: show_frame(signup_frame))
signup_button.pack(pady=10)

# Signup frame
canvas1, bg_image1 = set_background(signup_frame, "C:/Users/Admin/Downloads/1 (1).jpg")
signup_label = tk.Label(signup_frame, text="Signup For Screenly", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 16))
signup_label.pack(pady=10)
signup_username_label = tk.Label(signup_frame, text="Username:", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 15, 'bold'))
signup_username_label.pack()
signup_username_entry = tk.Entry(signup_frame, font=("Times New Roman", 16))
signup_username_entry.pack()
signup_password_label = tk.Label(signup_frame, text="Password:", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 16, 'bold'))
signup_password_label.pack()
signup_password_entry = tk.Entry(signup_frame, show="*")
signup_password_entry.pack()
signup_button = tk.Button(signup_frame, text="Signup", bg="#780606", fg="#FFFFFF", font=("Times New Roman", 16), command=handle_signup)
signup_button.pack(pady=10)

# Login frame
canvas2, bg_image2 = set_background(login_frame, "C:/Users/Admin/Downloads/1 (1).jpg")
login_label = tk.Label(login_frame, text="Login to Screenly", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 16))
login_label.pack(pady=10)
login_username_label = tk.Label(login_frame, text="Username:", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 16, 'bold'))
login_username_label.pack()
login_username_entry = tk.Entry(login_frame, font=("Times New Roman", 16))
login_username_entry.pack()
login_password_label = tk.Label(login_frame, text="Password:", bg='#000000', fg="#FFFFFF", font=("Times New Roman", 16, 'bold'))
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()
login_button = tk.Button(login_frame, text="Login", bg="#780606", fg="#FFFFFF", font=("Times New Roman", 16), command=handle_login)
login_button.pack(pady=10)

# Main page frame
canvas3, bg_image3 = set_background(main_page_frame, "C:/Users/Admin/Downloads/WhatsApp Image 2024-12-07 at 9.03.07 PM.jpeg")
main_label = tk.Label(main_page_frame, text="Welcome to Screenly", font=("Helvetica", 18))
main_label.pack(pady=10)
welcome_label = tk.Label(main_page_frame, text="Lights, Camera, Tickets!", font=("Raleway", 16))
welcome_label.pack()
image_frame = tk.Frame(main_page_frame)
image_frame.pack(pady=20)
logout_button = tk.Button(main_page_frame, text="Logout", command=lambda: show_frame(login_frame))
logout_button.pack(pady=10)

show_frame(welcome_frame)

root.mainloop()
