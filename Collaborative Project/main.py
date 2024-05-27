import tkinter as tk
from tkinter import filedialog, Canvas, Scrollbar, ttk
from PIL import Image, ImageTk


# Define window
window = tk.Tk()
window.title("Image Viewer with Scrollbar")

#Tab creation
tabcontrol = ttk.Notebook(window)
tab1 = tk.Frame(tabcontrol)
tab2 = tk.Frame(tabcontrol)

tabcontrol.add(tab1, text="Tab 1")
tabcontrol.add(tab2, text="✉️")
tabcontrol.grid(row=1, column=1 )

# Top bar using .grid()
# top_frame = tk.Frame(window, bg="lightblue", height=50)
# top_frame.grid(row=0, column=0, sticky="ew")
window.grid_columnconfigure(0, weight=1)
profile_pic = tk.Label(tab1, text="", font=("Arial", 20))
profile_pic.grid(row=0, column=0)
username_label = tk.Label(tab1, text="@YourUsername", font=("Arial", 16))
username_label.grid(row=0, column=1)
search_bar = tk.Entry(tab1, width=30)
search_bar.grid(row=0, column=2)
message_icon = tk.Label(tab1, text="✉️", font=("Arial", 16))
message_icon.grid(row=0, column=3)

# Image upload section
upload_button = tk.Button(tab1, text='Upload File', command=lambda: upload_file())
upload_button.grid(row=1, column=0, sticky="ew")
text = tk.Entry(tab1)
text.grid(row=2, column=0, sticky="ew")

# Scrollable Canvas
canvas = Canvas(tab1)
scrollbar = Scrollbar(tab1, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=4, sticky="ns")

# Configure grid for stretching
tab1.grid_rowconfigure(3, weight=1)

# List to keep references to the images so they are not garbage collected
images = []
current_row = 0
def upload_file():
    global current_row
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if filename:
        img = Image.open(filename)
        img_resized = img.resize((400, 200))  # new width & height
        img_tk = ImageTk.PhotoImage(img_resized)
        images.append(img_tk)  # Keep a reference to avoid garbage collection
        button = tk.Button(scrollable_frame, image=img_tk)
        textoutput = text.get()
        label = tk.Label(scrollable_frame, text=textoutput)
        label.grid(row=current_row, column=0)
        button.grid(row=current_row+1, column=0)
        current_row += 2
        
#tab 2 stuffffssss
window.grid_columnconfigure(0, weight=1)
profile_pic = tk.Label(tab2, text="", font=("Arial", 20))
profile_pic.grid(row=0, column=0)
username_label = tk.Label(tab2, text="@YourUsername", font=("Arial", 16))
username_label.grid(row=0, column=1)
search_bar = tk.Entry(tab2, width=30)
search_bar.grid(row=0, column=2)
message_icon = tk.Label(tab2, text="✉️", font=("Arial", 16))
message_icon.grid(row=0, column=3)

notebook = ttk.Notebook(tab2)
notebook.grid(row=0, column=0, sticky="nsew")

# Create a Frame for the tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Timetable')

# Define the columns and rows
columns = ["Ant", "Barra", "Croc", "Dingo", "Eagle", "Frog"]
rows = ["Period 1", "Period 2", "Reecess", "Period 3", "Period 4", "Lunch", "Period 5", "Period 6"]

# Define the starting row index
start_row = 4

# Create the labels for columns
for i, col in enumerate(columns):
    label = tk.Label(tab2, text=col, font=('Arial', 12, 'bold'))
    label.grid(row=start_row, column=i+1, sticky="nsew")

# Create the labels for rows
for i, row in enumerate(rows):
    label = tk.Label(tab2, text=row, font=('Arial', 12, 'bold'))
    label.grid(row=start_row + i + 1, column=0, sticky="nsew")

# Create the buttons in the grid
for i, row in enumerate(rows):
    for j, col in enumerate(columns):
        button = tk.Button(tab2, text=row, command=lambda r=row, c=col: on_button_click(r, c))
        button.grid(row=start_row + i + 1, column=j+1, sticky="nsew")

# Configure grid weights
for i in range(len(columns) + 1):
    tab2.grid_columnconfigure(i, weight=1)

for i in range(len(rows) + 1):
    tab2.grid_rowconfigure(i, weight=1)

# Run the main loop to keep the window open
window.mainloop()

