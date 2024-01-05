import tkinter as tk
from tkinter import ttk
import json
import os
import threading

def threaded_function(stop_event):
    while not stop_event.is_set():
        # Your function logic here
        pass

def start_project():
    global stop_event, thread
    stop_event.clear()
    thread = threading.Thread(target=threaded_function, args=(stop_event,))
    thread.start()
    finish_button.config(state="normal")  # Enable the "Finish Project" button

def finish_project():
    global stop_event
    stop_event.set()  # Signal the thread to stop
    if thread.is_alive():
        thread.join()  # Wait for the thread to finish
    finish_button.config(state="disabled")  # Disable the button after finishing

def run_mockup():
    pass

def save_data():
    data = {
        "downloads_dir": downloads_dir_entry.get(),
        "project_dir": project_dir_entry.get(),
        "project_name": project_name_entry.get()
    }
    with open("project_data.json", "w") as file:
        json.dump(data, file)

def load_data():
    if os.path.exists("project_data.json"):
        with open("project_data.json", "r") as file:
            data = json.load(file)
            downloads_dir_entry.insert(0, data.get("downloads_dir", ""))
            project_dir_entry.insert(0, data.get("project_dir", ""))
            project_name_entry.insert(0, data.get("project_name", ""))

# Initialize thread event and thread object
stop_event = threading.Event()
thread = None

# Tkinter setup
root = tk.Tk()
root.title("Project Manager")
root.geometry("400x300")  # Set the size of the window

# Create and place widgets
downloads_dir_label = ttk.Label(root, text="Downloads Directory:")
project_dir_label = ttk.Label(root, text="Project Directory:")
project_name_label = ttk.Label(root, text="Project Name:")
text_entry = ttk.Entry(root)
downloads_dir_entry = ttk.Entry(root)
project_dir_entry = ttk.Entry(root)
project_name_entry = ttk.Entry(root)

start_button = ttk.Button(root, text="Start New Project", command=start_project)
mockup_button = ttk.Button(root, text="Re-Generate Mockup", command=run_mockup)
finish_button = ttk.Button(root, text="Finish Project", command=finish_project, state="disabled")

# Layout using grid

downloads_dir_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')
downloads_dir_entry.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
project_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')
project_dir_entry.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
project_name_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')
project_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky='ew')

start_button.grid(row=4, column=0, padx=10, pady=10)
mockup_button.grid(row=4, column=1, padx=10, pady=10)
finish_button.grid(row=4, column=2, padx=10, pady=10)

root.grid_columnconfigure(1, weight=1)  # Make the entry fields expandable

# Load data from JSON if available
load_data()

# Run the application
root.mainloop()
