import tkinter as tk
from tkinter import filedialog, Canvas, Scrollbar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Global variables
requests = []
chosen_days = []
username = "@Hayden"
gym_member_count = 0
active = False

# Define window
window = tk.Tk()
# Import the tcl file
dir_path = os.path.dirname(os.path.realpath(__file__))
window.tk.call('source', os.path.join(dir_path, 'forest-light.tcl'))
 

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-light')
window.title("Student View")
window.geometry("900x600")  # Set initial size

student_window = window
tab3 = tk.Toplevel(window, padx=10, pady=10,)
tab3.title("Teacher View")
tab3.geometry("900x600")
# Tab creation
tabcontrol = ttk.Notebook(student_window)
tabcontrol.grid(row=0, column=0, sticky="nsew")

tab1 = ttk.Frame(tabcontrol,  ) #padx=10, pady=10,
tab2 = ttk.Frame(tabcontrol)


tabcontrol.add(tab1, text="Home")
tabcontrol.add(tab2, text="✉️")

# Configure the main window grid to expand properly
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Configure tab1 grid
tab1.grid_rowconfigure(1, weight=1)
tab1.grid_columnconfigure(1, weight=1)


def update_member_count(): 
    global gym_member_count, active

    if active:
        gym_member_count = gym_member_count - 1
        member_count_label.config(text=str(gym_member_count))
        student_member_count_label.config(text=str(gym_member_count))
        join_button["text"] = "Join gym"
        messagebox.showinfo("Left", "You have left the gym!")

        active = False
    else:
        gym_member_count = gym_member_count + 1
        member_count_label.config(text=str(gym_member_count))
        student_member_count_label.config(text=str(gym_member_count))
        
        join_button["text"] = "Leave gym"

        messagebox.showinfo("Join", "You have joined the gym!")
        active = True

# Top bar using .grid()
profile_frame = ttk.Frame(tab1,  borderwidth=1, padding=10)
img = Image.open(os.path.join(dir_path, 'profile_picture.png'))
img_resized = img.resize((25, 25))  # new width & height
img_tk = ImageTk.PhotoImage(img_resized)
button = ttk.Button(profile_frame, image=img_tk)

button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

username_label = ttk.Label(profile_frame, text=username, font=("Arial", 15))
username_label.pack(fill=tk.BOTH, side=tk.LEFT, )

student_member_count_frame = ttk.Frame(profile_frame,  padding=5, width=30, height=10)
student_member_count_text_label = ttk.Label(student_member_count_frame, text="Member count: " , font=('Arial', 15, ),  )
student_member_count_label = ttk.Label(student_member_count_frame, text=str(gym_member_count), font=('Arial', 15, ), )

student_member_count_frame.pack(side=tk.RIGHT, fill=tk.BOTH, pady=10, padx=30)
student_member_count_text_label.grid(row=0, column=0, sticky="nsew")    
student_member_count_label.grid(row=0, column=1, sticky="nsew")



join_button = ttk.Button(profile_frame, text="Join gym", command=update_member_count)
join_button.pack(fill=tk.BOTH, padx=20, pady=10)

profile_frame.grid(row=0, column=0, sticky="ns",)

# Image upload 
bottom_frame = ttk.Frame(tab1, padding=10, relief=tk.SUNKEN,) #padx=10, pady=10
upload_button = ttk.Button(bottom_frame, text='Upload File', command=lambda: upload_file(),  )
upload_button.pack(fill=tk.BOTH, side=tk.LEFT, ) 
text = ttk.Entry(bottom_frame,  width=70,)
text.pack(fill=tk.BOTH,side=tk.LEFT,  expand=True,)
send_button = ttk.Button(bottom_frame, text='Send', command=lambda: upload_file(),  )
send_button.pack(fill=tk.BOTH, side=tk.LEFT,) 
bottom_frame.grid(row=2, column=0, sticky="nsew", columnspan=3, )  # Modify this line to expand the frame to the end of the screen

# Scrollable Canvas
canvas = Canvas(tab1)
scrollbar = Scrollbar(tab1, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas, padding=10) # padx=10 

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=1, column=0, columnspan=3, sticky="nsew")
scrollbar.grid(row=1, column=4, sticky="ns")

# Configure scrollable_frame to expand properly
tab1.grid_rowconfigure(1, weight=1)
tab1.grid_columnconfigure(1, weight=1)

# List to keep references to the images so they are not garbage collected
images = []
current_row = 0

def upload_file():
    global current_row
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    print(filename)
    if filename:
        post = ttk.Frame(scrollable_frame)
        textoutput = text.get()
        username_label = tk.Label(post, text=username + textoutput)
        username_label.grid(row=0, column=0, sticky="w")
        img = Image.open(filename)
        img_resized = img.resize((400, 200))  # new width & height
        img_tk = ImageTk.PhotoImage(img_resized)
        images.append(img_tk)  # Keep a reference to avoid garbage collection
        button = ttk.Button(post, image=img_tk)
        
        #label.grid(row=2, column=0)
        button.grid(row=current_row+1, column=0)
        
        post.grid(row=current_row, column=0, sticky="w")
        current_row += 1
        
        text.delete(0, len(textoutput) + 1) # Clearing text box after uploading image - Dylan

# Configure tab2
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(0, weight=1)

# Create a Frame for the timetable in tab2
timetable_frame = ttk.Frame(tab2)
timetable_frame.grid(row=0, column=0, sticky="nsew")

# Dictionary to store selections
selections = {}

# Function to handle button clicks and store selections
def on_button_click(period, column):
    selections[column] = period
    #print(selections)  # For debugging, you can see the saved selections in the console

def setup_timetable():
        # Define the columns and rows
    columns = ["Ant", "Barra", "Croc", "Dingo", "Eagle", "Frog"]
    rows = ["Period 1", "Period 2", "Recess", "Period 3", "Period 4", "Lunch", "Period 5", "Period 6"]

    # Define the starting row index
    start_row = 0

    # Create the labels for columns
    for i, col in enumerate(columns):
        label = tk.Label(timetable_frame, text=col, font=('Arial', 12, 'bold'), borderwidth=1, relief="solid")
        label.grid(row=start_row, column=i+1, sticky="nsew", padx=1, pady=1)

    # Create the labels for rows
    for i, row in enumerate(rows):
        label = tk.Label(timetable_frame, text=row, font=('Arial', 12, 'bold'), borderwidth=1, relief="solid")
        label.grid(row=start_row + i + 1, column=0, sticky="nsew", padx=1, pady=1)

    
    # Create the buttons in the grid
    for i, row in enumerate(rows):
        for j, col in enumerate(columns):
            if len(chosen_days) != 0:
                for selected in chosen_days:
                    if col in selected["times"] and selected["times"][col] == row:
                        button = tk.Button(timetable_frame, text=row, command=lambda: messagebox.showinfo("Taken", "This spot is already taken please chose another one."), borderwidth=1, relief="solid", bg="red")
                        button.grid(row=start_row + i + 1, column=j+1, sticky="nsew", padx=1, pady=1)
                    else:
                        button = tk.Button(timetable_frame, text=row, command=lambda r=row, c=col: on_button_click(r, c, button), borderwidth=1, relief="solid",  )
                        button.grid(row=start_row + i + 1, column=j+1, sticky="nsew", padx=1, pady=1)
            else:
                button = tk.Button(timetable_frame, text=row, command=lambda r=row, c=col: on_button_click(r, c), borderwidth=1, relief="solid",  )
                button.grid(row=start_row + i + 1, column=j+1, sticky="nsew", padx=1, pady=1)

        # Configure grid weights for timetable_frame
    for i in range(len(columns) + 1):
        timetable_frame.grid_columnconfigure(i, weight=1)

    for i in range(len(rows) + 1):
        timetable_frame.grid_rowconfigure(i, weight=1)


setup_timetable()

# Add a dropdown list for multiple student selection
students_frame = ttk.Frame(tab2)
students_frame.grid(row=1, column=0, sticky="nsew", pady=10)
students_label = tk.Label(students_frame, text="Select Students:", font=('Arial', 12, 'bold'))
students_label.pack(side="top", anchor="w")

# Create a list of student names
student_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Black", "Diana Green"]

# # Frame to hold the dropdown menu
# dropdown_frame = tk.Frame(students_frame)
# dropdown_frame.pack(fill="x", expand=True)

# Button to toggle the dropdown menu
# def toggle_menu():
#     if dropdown_frame.winfo_ismapped():
#         dropdown_frame.pack_forget()
#     else:
#         dropdown_frame.pack(fill="x", expand=True)

# dropdown_button = tk.Button(students_frame, text="Select Students", command=toggle_menu)
# dropdown_button.pack(fill="x")

# Checkboxes for each student name
selected_students = []

def toggle_student(name):
    if name in selected_students:
        selected_students.remove(name)
    else:
        selected_students.append(name)

for name in student_names:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(students_frame, text=name, variable=var, command=lambda n=name: toggle_student(n))
    chk.pack(anchor="w")



# Button to show selected students
def send_request():
    
    requests.append({"students": selected_students, "times": selections})

    update_requests()

    # Reset Values

    for widget in timetable_frame.winfo_children():
        widget.destroy()
    
    setup_timetable()
    # selections = {}
    # selected_students = []
    

enter_button = tk.Button(students_frame, text="Send Request", command=send_request)
enter_button.pack(side="bottom", fill="x", expand=True)

# Configure grid weights for students_frame
tab2.grid_rowconfigure(1, weight=0)  # Ensure this row does not expand
tab2.grid_columnconfigure(0, weight=1)

# Dictionary to store selected students
selected_students_dict = {}

# Function to update the selected students dictionary with the names from the list
def update_selected_students():
    global selected_students_dict
    selected_students_dict.clear()  # Clear the dictionary before updating
    for student in selected_students:
        selected_students_dict[student] = True

# Function to toggle student selection
def toggle_student(name):
    global selected_students
    if name in selected_students:
        selected_students.remove(name)
    else:
        selected_students.append(name)

# Function to update the dictionary when Enter key is pressed in the text widget
def enter_pressed(event):
    if event.keysym == "Return":
        update_selected_students()
        #print("Selected Students Dictionary:")
        #print(selected_students_dict)

# Configure the text widget to call enter_pressed function when Enter key is pressed
# selected_students_text.bind("<KeyPress>", enter_pressed)

# Tab 3 widgets
requests_frame_array = []


# Update request functions

def accept_request(index):
    chosen_request = requests[index]
    name_text = ""
    times_text = ""

    for name in chosen_request["students"]:
        name_text = name_text + name + ", "

    for time in chosen_request["times"].items():
            times_text = times_text + f"{time[0]}: {time[1]}, "

    requests_frame_array[index].destroy()
    requests_frame_array.pop(index)
    chosen_days.append(requests[index])
   
    requests.pop(index)

    update_requests()
    tk.messagebox.showinfo("Request Accepted", f"{name_text}have been approved for the gym at {times_text}",)


def decline_request(index):
    requests_frame_array[index].destroy()
    requests_frame_array.pop(index)

    tk.messagebox.showinfo("Request Declined", "Request has been declined",)
    requests.pop(index)

    update_requests()


def update_requests(): 
    for widget in requests_frame.winfo_children():
        widget.destroy()
    

    for i in range(len(requests)):       
        # Request frame
        
        request_frame = ttk.Frame(requests_frame,  padding=10)
        requests_frame_array.append(request_frame)

        request_frame.pack(fill=tk.BOTH, )
        
        name_frame = ttk.Frame(request_frame)

        name_title_label = ttk.Label(name_frame, text="Names:")
        name_title_label.pack(fill=tk.X)

        for name in requests[i]["students"]:
            name_label = ttk.Label(name_frame, text=name)
            name_label.pack(fill=tk.X, )

        
        name_frame.pack(fill=tk.BOTH, side=tk.LEFT, padx=10)

        # Display Information widgets
        info_frame = ttk.Frame(request_frame)

        times_label = ttk.Label(info_frame, text=f"Times: ")
        msg_label = ttk.Label(info_frame, text="Message: Please leave the door open ", width=70)

        for time in requests[i]["times"].items():
            times_label["text"] = times_label["text"] + f"{time[0]}: {time[1]}, "

        times_label.pack(fill=tk.BOTH)
        msg_label.pack(fill=tk.BOTH)

        info_frame.pack(fill=tk.BOTH, side=tk.LEFT, )

        # Display Requests widgets
        request_button_frame = ttk.Frame(request_frame, padding=10)

        accept_button = ttk.Button(request_button_frame, text="✔", padding=10, command=lambda: accept_request(i))
        decline_button = ttk.Button(request_button_frame, text="✘", padding=10, command=lambda: decline_request(i))
        decline_button.pack(side=tk.RIGHT, fill=tk.Y)
        accept_button.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        request_button_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)


# Create widgets for tab3 header frame
header_frame = ttk.Frame(tab3, padding=5)
tab3_label = ttk.Label(header_frame, text="Requests", font=('Arial', 24, ))

member_count_frame = ttk.Frame(header_frame,  padding=5, width=30, height=10)
member_count_text_label = ttk.Label(member_count_frame, text="Member count: " , font=('Arial', 15, ),  )
member_count_label = ttk.Label(member_count_frame, text=str(gym_member_count), font=('Arial', 15, ), )

# Display all created widgets
header_frame.pack(fill=tk.X, ) #grid(row=0, column=0, sticky="nsew")
tab3_label.pack(side=tk.LEFT, fill=tk.Y)

member_count_frame.pack(side=tk.RIGHT,  fill=tk.Y)
member_count_text_label.grid(row=0, column=0, sticky="nsew")    
member_count_label.grid(row=0, column=1, sticky="nsew")

# Main tab3 frame
# main_tab3_frame = ttk.Frame(tab3, padding=15)

# # Scrollable Canvas
# tab3_canvas = Canvas(main_tab3_frame)
# tab3_scrollbar = Scrollbar(main_tab3_frame, orient="vertical", command=canvas.yview)
# tab3_scrollable_frame = ttk.Frame(tab3_canvas, padding=10) # padx=10 

# scrollable_frame.bind(
#     "<Configure>",
#     lambda e: canvas.configure(
#         scrollregion=canvas.bbox("all")
#     )
# )

#   Displaying tab3 frame widgets
# tab3_canvas.create_window((0, 0), window=tab3_scrollable_frame, anchor="w")
# tab3_canvas.configure(yscrollcommand=scrollbar.set)
# tab3_canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")
# tab3_scrollbar.grid(row=0, column=1, sticky="ns")
# main_tab3_frame.pack()
requests_frame = ttk.Frame(tab3, )
requests_frame.pack(fill=tk.BOTH, side=tk.TOP)

# Run the main loop to keep the window open
window.mainloop()