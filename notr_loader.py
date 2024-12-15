import os
import json

# Create a new project folder structure
def create_project(project_dir, project_name):
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    
    # Initialize the .notr file
    notr_data = {
        project_name: {}
    }
    
    notr_file_path = os.path.join(project_dir, f"{project_name}.notr")
    with open(notr_file_path, 'w') as f:
        json.dump(notr_data, f, indent=4)
    
    return notr_data, notr_file_path

# Load the .notr file
def load_notr_file(notr_file_path):
    if os.path.exists(notr_file_path):
        with open(notr_file_path, 'r') as f:
            return json.load(f)
    return {}

# Save the .notr file (update the structure)
def save_notr_file(notr_data, notr_file_path):
    with open(notr_file_path, 'w') as f:
        json.dump(notr_data, f, indent=4)

# Create a new category (folder) within the project
def create_category(project_dir, category_name):
    category_path = os.path.join(project_dir, category_name)
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    return category_path

# Create a new text file in the category
def create_text_file(category_path, file_name):
    file_path = os.path.join(category_path, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("")  # Create an empty text file
    return file_path

# Get the content of a text file
def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

# Save the content of a text file
def save_text_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
