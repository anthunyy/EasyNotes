import tkinter as tk
from tkinter import ttk

def main():
    # Create the main window
    root = tk.Tk()
    root.tk.call('source', 'theme/forest-dark.tcl')
    ttk.Style().theme_use('forest-dark')
    root.title("EazyNotes")

    #Set icon
    root.iconbitmap("icon/icon.ico")

    # Allow the window to be resizable
    root.resizable(True, True)

    # Set the size of the window
    root.geometry("400x500")

    # Add a Text widget for typing
    card = ttk.Frame(root, style='Card', padding=(5, 6, 7, 8))
    text_box = tk.Text(root, wrap="word", height=10, width=50)
    text_box.pack(side="left", fill="both", expand=True)
    text_box.config(highlightthickness=0)

    # Add a scrollbar to the Text widget
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=text_box.yview)
    scrollbar.pack(side="right", fill="y")

    # Link the scrollbar to the Text widget
    text_box.config(yscrollcommand=scrollbar.set)

    # Style  scrollbar
    style = ttk.Style()
    style.configure("TScrollbar", thickness=8)

    # Run the application
    root.mainloop()

if __name__ == "__main__":
    main()

