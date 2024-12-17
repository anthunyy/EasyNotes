import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
import os
from notr_loader import *
from PIL import Image, ImageTk

# Function to open the project by selecting a .notr file
def open_project():
    global project_dir, notr_data, project_name, notr_file_path
    notr_file_path = filedialog.askopenfilename(
        title="Select a .notr Project File", filetypes=[("Notr Files", "*.notr")]
    )
    if notr_file_path:
        project_dir = os.path.dirname(notr_file_path)
        notr_data = load_notr_file(notr_file_path)
        project_name = list(notr_data.keys())[0]  # Assume first key is project name
        load_treeview(notr_data, project_dir, project_name, notr_file_path)

# Function to create a new project
def create_new_project():
    global project_dir, notr_data, project_name, notr_file_path
    project_dir = filedialog.askdirectory(title="Select Project Directory")
    if project_dir:
        project_name = simpledialog.askstring("Project Name", "Enter project name:")
        if project_name:
            # Ensure .notr extension is added
            project_name = project_name if project_name.endswith(".notr") else f"{project_name}.notr"
            notr_data, notr_file_path = create_project(project_dir, project_name[:-5])  # Strip .notr for internal name
            load_treeview(notr_data, project_dir, project_name[:-5], notr_file_path)

# Function to load data into the treeview
def load_treeview(notr_data, project_dir, project_name, notr_file_path):
    treeview.delete(*treeview.get_children())  # Clear the treeview
    root_node = treeview.insert("", "end", text=project_name, open=True, values=("folder", project_dir))
    insert_treeview_items(root_node, notr_data[project_name])

# Recursive function to add items to the treeview
def insert_treeview_items(parent, data):
    for name, value in data.items():
        if isinstance(value, dict):  # Subcategory
            node = treeview.insert(parent, "end", text=name, open=True, values=("folder", ""))
            insert_treeview_items(node, value)  # Recurse for subcategories
        else:  # Text file
            treeview.insert(parent, "end", text=name, values=("file", value))

# Handle unsaved changes before selecting a new file
def on_treeview_select(event):
    global last_saved_file
    selected_item = treeview.selection()
    if selected_item:
        file_type, file_path = treeview.item(selected_item[0], "values")
        if file_type == "file":
            # Save the current file's unsaved changes
            if last_saved_file:
                unsaved_changes[last_saved_file] = note.get("1.0", "end-1c")

            # Open the selected file (load from cache or disk)
            last_saved_file = file_path
            if file_path in unsaved_changes:
                note.delete("1.0", "end")
                note.insert("1.0", unsaved_changes[file_path])
            else:
                open_text_file(file_path)

            file_name_label.config(text=os.path.basename(file_path))

# Function to open a text file
def open_text_file(file_path):
    content = get_file_content(file_path)
    if content is not None:
        note.delete("1.0", "end")
        note.insert("1.0", content)

# Function to save all unsaved changes to files
def save_file():
    for file_path, content in unsaved_changes.items():
        save_text_file(file_path, content)
    unsaved_changes.clear()
    messagebox.showinfo("Save", "All unsaved changes have been saved.")

# Function to create a new category (subcategory)
def create_new_category():
    selected_item = treeview.selection()
    if selected_item:
        parent_node = selected_item[0]
        new_category_name = simpledialog.askstring("New Category", "Enter category name:")
        if new_category_name:
            item_values = treeview.item(parent_node, "values")
            if "folder" in item_values:  # Only allow categories
                category_path = os.path.join(item_values[1], new_category_name)
                os.makedirs(category_path, exist_ok=True)
                treeview.insert(parent_node, "end", text=new_category_name, values=("folder", category_path))

# Function to create a new text file
def create_new_text_file():
    selected_item = treeview.selection()
    if selected_item:
        parent_node = selected_item[0]
        new_file_name = simpledialog.askstring("New Text File", "Enter text file name:")
        if new_file_name:
            # Ensure .txt extension
            if not new_file_name.endswith(".txt"):
                new_file_name += ".txt"

            item_values = treeview.item(parent_node, "values")
            if "folder" in item_values:  # Allow only in folders
                file_path = os.path.join(item_values[1], new_file_name)
                with open(file_path, "w") as f:
                    f.write("")  # Create an empty file
                treeview.insert(parent_node, "end", text=new_file_name, values=("file", file_path))

# Initialize global variables
project_dir = None
project_name = None
notr_data = {}
notr_file_path = None
last_saved_file = None
unsaved_changes = {}

# GUI Setup
root = tk.Tk()
root.title("Notetree")
root.geometry("1000x600")

# Add icon
icon = Image.open("icon/icon.png")
iconphoto = ImageTk.PhotoImage(icon)
root.iconphoto(True, iconphoto)

# Add theme
root.tk.call("source", "theme/forest-dark.tcl")
ttk.Style().theme_use("forest-dark")

# Top Buttons Frame
buttons_frame = ttk.Frame(root)
buttons_frame.pack(side="top", fill="x", padx=10, pady=10)

ttk.Button(buttons_frame, text="Open Project", command=open_project).pack(side="left", padx=5)
ttk.Button(buttons_frame, text="New Project", command=create_new_project).pack(side="left", padx=5)
ttk.Button(buttons_frame, text="Save All", command=save_file).pack(side="left", padx=5)
ttk.Button(buttons_frame, text="New Category", command=create_new_category).pack(side="left", padx=5)
ttk.Button(buttons_frame, text="New Text File", command=create_new_text_file).pack(side="left", padx=5)

# Treeview for File Structure
treeview = ttk.Treeview(root)
treeview.pack(side="left", fill="y")
treeview.bind("<<TreeviewSelect>>", on_treeview_select)

# File Name Label (moved above editor on right)
file_name_label = ttk.Label(root, text="No file loaded", font=("Helvetica", 12))
file_name_label.pack(side="top", anchor="e", padx=10, pady=5)

# Text Editor
note = tk.Text(root, wrap="word", font=("Helvetica", 14))
note.pack(side="right", fill="both", expand=True)

# Start the application
root.mainloop()