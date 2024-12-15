import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *

# Create the main window
root = tk.Tk()
root.title("EasyNotes")

# Set the icon (Ensure you have the correct file path for your icon)
try:
    icon = PhotoImage(file='icon/icon.png')  # Update the path to your icon
    root.iconphoto(True, icon)
except Exception as e:
    print(f"Error loading icon: {e}")

# Allow the window to be resizable (both directions)
root.resizable(True, True)

# Import the custom theme (Ensure the theme file path is correct)
root.tk.call("source", "theme/forest-dark.tcl")  # Update with your theme path
style = ttk.Style(root)
style.theme_use("forest-dark")

# StringVar for holding note content
note_content = StringVar()

# Variable to store the path of the last saved file
last_saved_file = None

# Create a Frame to hold the buttons in the top-left corner
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=10)

# Function to save the text from the Text widget into note_content
def save_note():
    # Get all the text from the Text widget (excluding the trailing newline)
    content = note.get("1.0", "end-1c")
    
    # If there's a file path from previous save, overwrite it
    if last_saved_file:
        with open(last_saved_file, "w") as file:
            file.write(content)
        print(f"File saved to: {last_saved_file}")
    else:
        # If no file has been saved before, prompt the user to save the file
        save_to_file()

# Create the Save button inside the Frame
save_button = ttk.Button(button_frame, text="Save", command=save_note, style="TButton")

# Function to save the content to a text file (with file dialog)
def save_to_file():
    # Get the content of the Text widget
    content = note.get("1.0", "end-1c")
    
    # Open a file dialog to choose where to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    # If the user selected a file, save the content to the file
    if file_path:
        with open(file_path, "w") as file:
            file.write(content)
        print(f"File saved to: {file_path}")
        # Store the last saved file path for future saves
        global last_saved_file
        last_saved_file = file_path

# Create the Save to File button inside the Frame
save_to_file_button = ttk.Button(button_frame, text="Save to File", command=save_to_file, style="TButton")

# Function to open a file and load its content into the Text widget
def open_file():
    # Open a file dialog to choose a file to open
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    if file_path:
        # If a file was selected, open and read the content into the Text widget
        with open(file_path, "r") as file:
            content = file.read()
            note.delete("1.0", "end")  # Clear any existing content
            note.insert("1.0", content)  # Insert the file content
        print(f"File opened: {file_path}")
        # Store the file path for saving later
        global last_saved_file
        last_saved_file = file_path

# Create the Open button inside the Frame
open_button = ttk.Button(button_frame, text="Open", command=open_file, style="TButton")

# Pack the Open button first, then Save and Save to File buttons
open_button.pack(side="left", padx=10)
save_button.pack(side="left", padx=10)
save_to_file_button.pack(side="left", padx=10)

# Create the Text widget with wrapping enabled and a specific font size (20)
note = tk.Text(root, wrap="word", font=("Helvetica", 20), height=12, width=30)  # Width 30, Font size 20
note.insert(tk.INSERT, "Insert text here or open a file to edit.")
note.pack(padx=10, pady=10, fill="both", expand=True)

# Function to adjust the font size of the text widget and buttons
def set_font_size(size):
    # Set the font size of the Text widget
    note.config(font=("Helvetica", size))
    
    # Set the font size of the buttons
    style.configure("TButton", font=("Helvetica", size))

# Set the initial font size to 20
set_font_size(20)

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

# Set the initial fixed window size and allow resizing
root.geometry("250x400")  # Narrower window size (less wide)
root.resizable(True, True)  # Allow resizing

# Start the main loop
root.mainloop()