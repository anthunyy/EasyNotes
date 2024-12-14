import tkinter as tk
from tkinter import ttk
from tkinter import *

root = tk.Tk()
root.title("EasyNotes")
root.option_add("*tearOff", False)
root.iconbitmap("icon/icon.ico")

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "theme/forest-dark.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-dark")

# Allow the window to be resizable
root.resizable(True, True)

#String idk
note_content = StringVar()

# Note
note = ttk.Entry(root, textvariable = note_content)
note.insert(0, "Insert text")
note.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.geometry("400x500")

# Start the main loop
root.mainloop()
