import tkinter as tk
from tkinter import filedialog, Canvas, Scrollbar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def on_button_click(period, column):
    messagebox.showinfo("Button Clicked", f"You clicked on {period} in column {column}")

# Define window
window = tk.Tk()
# Import the tcl file
dir_path = os.path.dirname(os.path.realpath(__file__))
window.tk.call('source', os.path.join(dir_path, 'forest-light.tcl'))
 

# Set the theme with the theme_use method
ttk.Style().theme_use('forest-light')
window.title("Image Viewer with Scrollbar")
window.geometry("900x600")  # Set initial size

# Tab creation
tabcontrol = ttk.Notebook(window)
tabcontrol.grid(row=0, column=0, sticky="nsew")

tab1 = ttk.Frame(tabcontrol,  ) #padx=10, pady=10,
tab2 = ttk.Frame(tabcontrol)
tab3 = ttk.Frame(tabcontrol, padding=10)


tabcontrol.add(tab1, text="Tab 1")
tabcontrol.add(tab2, text="✉️")
tabcontrol.add(tab3, text="Requests")

# Configure the main window grid to expand properly
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Configure tab1 grid
tab1.grid_rowconfigure(1, weight=1)
tab1.grid_columnconfigure(1, weight=1)

# Top bar using .grid()
profile_frame = ttk.Frame(tab1,  borderwidth=1)
profile_pic = ttk.Label(profile_frame, text="Picture", font=("Arial", 20))# padx=10, pady=10,
profile_pic.grid(row=0, column=0, sticky="ew")
username_label = ttk.Label(profile_frame, text="@YourUsername", font=("Arial", 16))
username_label.grid(row=0, column=1, sticky="ew")
search_bar = ttk.Entry(profile_frame, width=30)
search_bar.grid(row=0, column=2,  sticky="ew")
message_icon = ttk.Label(profile_frame, text="✉️", font=("Arial", 16), )
message_icon.grid(row=0, column=3,  sticky="ew")
profile_frame.grid(row=0, column=0, sticky="ns")

# Image upload 
bottom_frame = ttk.Frame(tab1,   )#padx=10, pady=10
upload_button = ttk.Button(bottom_frame, text='Upload File', command=lambda: upload_file(), width=10, )
#upload_button.grid(row=0, column=2, sticky="nsew") # changed upload file to be near the text box - Dylan
upload_button.grid(row=0, column=1, sticky="s")
text = ttk.Entry(bottom_frame, width=30,)
text.grid(row=0, column=0, sticky="s")
bottom_frame.grid(row=2, column=0,sticky="s", )

# Scrollable Canvas
canvas = Canvas(tab1)
scrollbar = Scrollbar(tab1, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas,) # padx=10 

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
    if filename:
        post = ttk.Frame(scrollable_frame)
        textoutput = text.get()
        username_label = tk.Label(post, text="@YourUsername  "+ textoutput)
        username_label.grid(row=0, column=0, sticky="w")
        img = Image.open(filename)
        img_resized = img.resize((400, 200))  # new width & height
        img_tk = ImageTk.PhotoImage(img_resized)
        images.append(img_tk)  # Keep a reference to avoid garbage collection
        button = ttk.Button(post, image=img_tk)
        
        label.grid(row=2, column=0)
        button.grid(row=current_row+1, column=0)
        

        post.grid(row=current_row, column=0, sticky="w")
       #)
        current_row += 1
        
        text.delete(0, len(textoutput) + 1) # Clearing text box after uploading image - Dylan

# Configure tab2
tab2.grid_rowconfigure(0, weight=1)
tab2.grid_columnconfigure(0, weight=1)

# Create a Frame for the timetable in tab2
timetable_frame = ttk.Frame(tab2)
timetable_frame.grid(row=0, column=0, sticky="nsew")

# Define the columns and rows
columns = ["Ant", "Barra", "Croc", "Dingo", "Eagle", "Frog"]
rows = ["Period 1", "Period 2", "Recess", "Period 3", "Period 4", "Lunch", "Period 5", "Period 6"]

# Define the starting row index
start_row = 0

# Create the labels for columns
for i, col in enumerate(columns):
    label = ttk.Label(timetable_frame, text=col, font=('Arial', 12, 'bold'), padding=1 )
    label.grid(row=start_row, column=i+1, sticky="nsew", padx=1, pady=1)

# Create the labels for rows
for i, row in enumerate(rows):
    label = ttk.Label(timetable_frame, text=row, font=('Arial', 12, 'bold'),  padding=1)
    label.grid(row=start_row + i + 1, column=0, sticky="nsew", padx=1, pady=1)

# Create the buttons in the grid
for i, row in enumerate(rows):
    for j, col in enumerate(columns):
        button = ttk.Button(timetable_frame, text=row, command=lambda r=row, c=col: on_button_click(r, c),  )
        button.grid(row=start_row + i + 1, column=j+1, sticky="nsew", padx=1, pady=1)

# Configure grid weights for timetable_frame
for i in range(len(columns) + 1):
    timetable_frame.grid_columnconfigure(i, weight=1)

for i in range(len(rows) + 1):
    timetable_frame.grid_rowconfigure(i, weight=1)

# Add a dropdown list for multiple student selection
students_frame = ttk.Frame(tab2)
students_frame.grid(row=1, column=0, sticky="nsew", pady=10)
students_label = ttk.Label(students_frame, text="Select Students:", font=('Arial', 12, 'bold'))
students_label.pack(side="top", anchor="w")

# Create a list of student names
student_names = ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Charlie Black", "Diana Green"]

# Frame to hold the dropdown menu
dropdown_frame = ttk.Frame(students_frame)
dropdown_frame.pack(fill="x", expand=True)

# Button to toggle the dropdown menu
def toggle_menu():
    if dropdown_frame.winfo_ismapped():
        dropdown_frame.pack_forget()
    else:
        dropdown_frame.pack(fill="x", expand=True)

dropdown_button = ttk.Button(students_frame, text="Select Students", command=toggle_menu)
dropdown_button.pack(fill="x")

# Checkboxes for each student name
selected_students = []

def toggle_student(name):
    if name in selected_students:
        selected_students.remove(name)
    else:
        selected_students.append(name)

for name in student_names:
    var = tk.BooleanVar()
    chk = tk.Checkbutton(dropdown_frame, text=name, variable=var, command=lambda n=name: toggle_student(n))
    chk.pack(anchor="w")

# Text widget to display selected students
selected_students_label = ttk.Label(students_frame, text="Selected Students:", font=('Arial', 12, 'bold'))
selected_students_label.pack(anchor="w")
selected_students_text = tk.Text(students_frame, height=5, state="disabled")
selected_students_text.pack(fill="x", expand=True)

# Button to show selected students
def show_selected_students():
    selected_students_text.config(state="normal")
    selected_students_text.delete("1.0", tk.END)
    for student in selected_students:
        selected_students_text.insert(tk.END, f"{student}\n")
    selected_students_text.config(state="disabled")

enter_button = ttk.Button(students_frame, text="Enter", command=show_selected_students)
enter_button.pack(side="bottom", fill="x", expand=True)

# Configure grid weights for students_frame
tab2.grid_rowconfigure(1, weight=0)  # Ensure this row does not expand
tab2.grid_columnconfigure(0, weight=1)

# Configue tab3
tab3.grid_rowconfigure(0, weight=1)
tab3.grid_columnconfigure(0, weight=1)

# Create widgets for tab3 header frame
header_frame = ttk.Frame(tab3, )
tab3_label = ttk.Label(header_frame, text="Requests", font=('Arial', 24, ))
member_count_frame = ttk.Frame(header_frame, borderwidth=0.5, relief=tk.SOLID, padding=5, width=30, height=10)
member_count_text_label = ttk.Label(member_count_frame, text="Gym: ", font=('Arial', 15, ),  )
member_count_label = ttk.Label(member_count_frame, text="10", font=('Arial', 15, ), )

# Display all created widgets
header_frame.pack(fill=tk.X, ) #grid(row=0, column=0, sticky="nsew")
tab3_label.pack(side=tk.LEFT, fill=tk.Y)
member_count_frame.pack(side=tk.RIGHT,  fill=tk.Y)
member_count_text_label.grid(row=0, column=0, sticky="nsew")    
member_count_label.grid(row=0, column=1, sticky="nsew")

# Main tab3 frame
main_tab3_frame = ttk.Frame(tab3, padding=15)

# Scrollable Canvas
tab3_canvas = Canvas(main_tab3_frame)
tab3_scrollbar = Scrollbar(main_tab3_frame, orient="vertical", command=canvas.yview)
tab3_scrollable_frame = ttk.Frame(tab3_canvas, padding=10) # padx=10 

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

#   Displaying tab3 frame widgets

tab3_canvas.create_window((0, 0), window=tab3_scrollable_frame, anchor="w")
tab3_canvas.configure(yscrollcommand=scrollbar.set)
tab3_canvas.grid(row=0, column=0, columnspan=3, sticky="nsew")
tab3_scrollbar.grid(row=0, column=1, sticky="ns")
main_tab3_frame.pack()

# Run the main loop to keep the window open
window.mainloop()