import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import os
import json
from notr_loader import load_notr_file, save_notr_file, get_file_content  # Import functions from notr_loader.py

# Create the main window
root = tk.Tk()
root.title("EasyNotes")

# Set up custom theme (ensure the theme file path is correct)
root.tk.call("source", "theme/forest-dark.tcl")  # Update with your theme path
style = ttk.Style(root)
style.theme_use("forest-dark")

# Set the window size and make it resizable
root.geometry("800x600")
root.resizable(True, True)

# Create a Frame for the left-hand side (Buttons, Treeview)
left_frame = ttk.Frame(root)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

# Create a Frame for the right-hand side (Text Editing Area)
right_frame = ttk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

# Create a label for displaying the file name in the right frame
file_name_label = ttk.Label(right_frame, text="No file loaded", font=("Helvetica", 14))
file_name_label.pack(pady=5)

# Text widget for editing the file content
note = tk.Text(right_frame, wrap="word", font=("Helvetica", 16), height=30, width=50)
note.insert(tk.INSERT, "Insert text here or open a file to edit.")
note.pack(padx=10, pady=10, fill="both", expand=True)

# Variable to store the path of the last saved file
last_saved_file = None

# Load the default .notr structure (Main.notr) or use the default if none exists
notr_data = load_notr_file("Main.notr")

# Create a Frame for the buttons at the top of the left panel (buttons_frame)
buttons_frame = ttk.Frame(left_frame)
buttons_frame.pack(side="top", fill="x", padx=10, pady=10)

# Function to handle selection from the Treeview
def on_treeview_select(event):
    selected_item = treeview.selection()  # Get the selected item (returns a tuple)
    if selected_item:  # Check if there is a selection
        item_id = selected_item[0]  # Extract the ID of the selected item
        item_data = treeview.item(item_id)  # Get the entire item data
        file_path = item_data.get("value")  # Get the file path (stored in 'value')
        
        if file_path:  # If the selected item has a valid file path
            open_text_file(file_path)  # Open the text file in the editor
        else:
            print("Selected item is not a file.")
    else:
        print("No item selected.")

# Helper function to open a text file and load it into the editor
def open_text_file(file_path):
    content = get_file_content(file_path)
    if content is not None:
        note.delete("1.0", "end")  # Clear the current content in the editor
        note.insert("1.0", content)  # Insert the content of the selected file
        file_name_label.config(text=os.path.basename(file_path))  # Update the file name label
        global last_saved_file
        last_saved_file = file_path  # Set the file path as the last saved file

# Function to save the content of the text file
def save_file():
    if last_saved_file:
        content = note.get("1.0", "end-1c")
        save_text_file(last_saved_file, content)

# Helper function to save content into the corresponding text file
def save_text_file(file_path, content):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Saved content to {file_path}")

# Function to save the entire .notr file to disk (metadata only, not content)
def save_to_file():
    folder_path = filedialog.askdirectory()  # Ask user for folder to save all data
    
    if folder_path:
        # Ensure the directory exists
        os.makedirs(folder_path, exist_ok=True)
        
        # Save all text files from notr_data into the folder
        save_notr_file(notr_data, folder_path)
        print(f"Saved .notr file and text files to {folder_path}")

# Create the Open button inside the Frame
def open_file():
    # Open a file dialog to choose a .notr file to open
    file_path = filedialog.askopenfilename(defaultextension=".notr", filetypes=[("Notetree files", "*.notr"), ("All files", "*.*")])
    
    if file_path:
        global notr_data
        notr_data = load_notr_file(file_path)  # Load the selected .notr file
        print(f"Opened .notr file: {file_path}")
        load_treeview()

# Create the Save button inside the Frame
save_button = ttk.Button(buttons_frame, text="Save", command=save_file, style="TButton")
save_button.pack(side="left", padx=5)

# Create the Save to File button inside the Frame
save_to_file_button = ttk.Button(buttons_frame, text="Save to File", command=save_to_file, style="TButton")
save_to_file_button.pack(side="left", padx=5)

# Create the Open button inside the Frame
open_button = ttk.Button(buttons_frame, text="Open", command=open_file, style="TButton")
open_button.pack(side="left", padx=5)

# Create the Treeview widget for file structure
treeview = ttk.Treeview(left_frame)
treeview.pack(fill="both", expand=True)

# Function to load the treeview structure
def load_treeview():
    treeview.delete(*treeview.get_children())  # Clear the current treeview
    root_node = treeview.insert("", "end", text="Main", open=True)  # Root node (Main)
    
    for category, content in notr_data.items():
        category_node = treeview.insert(root_node, "end", text=category, open=True)
        for file_name, file_path in content.items():
            if isinstance(file_path, dict):
                load_treeview_subcategories(category_node, file_name, file_path)
            else:
                treeview.insert(category_node, "end", text=file_name, value=file_path)  # Add text file as a leaf node

# Function to handle subcategories (folders)
def load_treeview_subcategories(parent_node, subcategory, file_data):
    subcategory_node = treeview.insert(parent_node, "end", text=subcategory, open=True)
    for file_name, file_path in file_data.items():
        if isinstance(file_path, dict):
            load_treeview_subcategories(subcategory_node, file_name, file_path)
        else:
            treeview.insert(subcategory_node, "end", text=file_name, value=file_path)

# Bind the treeview selection event to open the selected file
treeview.bind("<<TreeviewSelect>>", on_treeview_select)

# Start the main loop
root.mainloop()