import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import os
import json
from notr_loader import *

# Function to open the project folder (directory)
def open_project():
    global project_dir, notr_file_path
    project_dir = filedialog.askdirectory(title="Select Project Directory")
    if project_dir:
        notr_file_path = os.path.join(project_dir, "Main.notr")
        if os.path.exists(notr_file_path):
            notr_data = load_notr_file(notr_file_path)
            load_treeview(notr_data, project_dir, "Main", notr_file_path)
            load_editor_with_default_file(project_dir, "Main")
        else:
            print("No existing .notr file found!")

# Function to create a new project
def create_new_project():
    global project_dir, notr_file_path
    project_dir = filedialog.askdirectory(title="Select Project Directory")
    if project_dir:
        project_name = simpledialog.askstring("Project Name", "Enter project name:")
        if project_name:
            notr_data, notr_file_path = create_project(project_dir, project_name)
            load_treeview(notr_data, project_dir, project_name, notr_file_path)
            load_editor_with_default_file(project_dir, project_name)

# Function to load the notr data into the treeview
def load_treeview(notr_data, project_dir, project_name, notr_file_path):
    treeview.delete(*treeview.get_children())  # Clear the treeview
    root_node = treeview.insert("", "end", text=project_name, open=True)  # Root node (Project name)

    # Insert categories and files into the treeview
    for category_name, category_data in notr_data.get(project_name, {}).items():
        category_node = treeview.insert(root_node, "end", text=category_name, open=True)
        for file_name, file_path in category_data.items():
            treeview.insert(category_node, "end", text=file_name, value=file_path)

# Function to load the editor with the default text file
def load_editor_with_default_file(project_dir, project_name):
    default_category = "Main"  # Default category
    default_file = "untitled.txt"  # Default file name
    category_path = os.path.join(project_dir, default_category)

    if not os.path.exists(category_path):
        os.makedirs(category_path)
        
    default_file_path = os.path.join(category_path, default_file)
    if not os.path.exists(default_file_path):
        with open(default_file_path, 'w') as f:
            f.write("")  # Create an empty text file

    open_text_file(default_file_path)

# Function to open a text file in the editor
def open_text_file(file_path):
    content = get_file_content(file_path)
    if content is not None:
        note.delete("1.0", "end")
        note.insert("1.0", content)
        file_name_label.config(text=os.path.basename(file_path))
        global last_saved_file
        last_saved_file = file_path

# Function to handle file selection in the Treeview
def on_treeview_select(event):
    selected_item = treeview.selection()
    if selected_item:
        item_id = selected_item[0]
        item_data = treeview.item(item_id)
        file_path = item_data.get("value")

        if file_path:
            open_text_file(file_path)

# Function to save the content of the text file
def save_file():
    if last_saved_file:
        content = note.get("1.0", "end-1c")
        save_text_file(last_saved_file, content)

# Function to create a new category
def create_new_category():
    new_category_name = simpledialog.askstring("New Category", "Enter category name:")
    if new_category_name:
        category_path = create_category(project_dir, new_category_name)
        if "Main" not in notr_data[project_name]:
            notr_data[project_name]["Main"] = {}
        notr_data[project_name]["Main"][new_category_name] = {}
        save_notr_file(notr_data, notr_file_path)
        load_treeview(notr_data, project_dir, project_name, notr_file_path)

# Function to create a new text file (in the currently selected category)
def create_new_text_file():
    selected_item = treeview.selection()
    if selected_item:
        category_name = treeview.item(selected_item[0])["text"]
        if category_name == project_name:
            category_name = "Main"  # Default to "Main" if the root is selected
        new_file_name = simpledialog.askstring("New Text File", "Enter text file name:")
        if new_file_name:
            category_path = os.path.join(project_dir, category_name)
            file_path = create_text_file(category_path, new_file_name)
            if category_name not in notr_data[project_name]:
                notr_data[project_name][category_name] = {}
            notr_data[project_name][category_name][new_file_name] = file_path
            save_notr_file(notr_data, notr_file_path)
            load_treeview(notr_data, project_dir, project_name, notr_file_path)
            open_text_file(file_path)

# Initialize global variables
project_dir = None
project_name = None
notr_data = {}
notr_file_path = None
last_saved_file = None

# Create the main window
root = tk.Tk()
root.title("EasyNotes")
root.geometry("1000x600")  # Adjust the window size for better layout
root.resizable(True, True)

# Frame for buttons (top of the window)
buttons_frame = ttk.Frame(root)
buttons_frame.pack(side="top", fill="x", padx=10, pady=10)

# File name label on the editor side
file_name_label = ttk.Label(root, text="No file loaded", font=("Helvetica", 14))
file_name_label.pack(pady=5, side="top")

# Text widget for the editor
note = tk.Text(root, wrap="word", font=("Helvetica", 16), height=30, width=50)
note.insert(tk.INSERT, "Insert text here or open a file to edit.")
note.pack(padx=10, pady=10, fill="both", expand=True, side="right")

# Treeview for file structure (Larger tree area)
treeview = ttk.Treeview(root, height=25)  # Increased height for a larger tree area
treeview.pack(fill="y", expand=True, side="left")

# Create buttons for the UI
open_button = ttk.Button(buttons_frame, text="Open Project", command=open_project)
open_button.pack(side="left", padx=10)

new_project_button = ttk.Button(buttons_frame, text="New Project", command=create_new_project)
new_project_button.pack(side="left", padx=10)

save_button = ttk.Button(buttons_frame, text="Save", command=save_file)
save_button.pack(side="left", padx=10)

new_category_button = ttk.Button(buttons_frame, text="New Category", command=create_new_category)
new_category_button.pack(side="left", padx=10)

new_text_file_button = ttk.Button(buttons_frame, text="New Text File", command=create_new_text_file)
new_text_file_button.pack(side="left", padx=10)

# Bind the treeview selection event to open the selected file
treeview.bind("<<TreeviewSelect>>", on_treeview_select)

# Start the main loop
root.mainloop()