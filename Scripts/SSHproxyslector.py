from tkinter import *
import tkinter as tk
import subprocess
import threading

# Create a function to run the selected command
def run_command(command):
    global process
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    status_label.config(text="Connection: Connected")

# Create a function to close the connection
def close_connection():
    process.terminate()

def get_current_data():
    # Add code here to return the current data transmitted
    return 50

def is_connection_closed():
    # Add code here to return whether the connection is closed or not
    return False

# Update the GUI inside a separate thread
def update_gui():
    while True:
        current_data = get_current_data()
        progress_bar["value"] = current_data

        if is_connection_closed():
            status_label.config(text="Connection: Not connected")
            break

# Create the GUI
root = tk.Tk()
root.title("Select DSN Cluster")

# Create the progress bar
progress_bar = tk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

# Create a list of commands
commands = [
    "ssh -D 1234 PDX@host",
    "ssh -D 1234 -J IAD@host2:user@host3 user@host1",
    "ssh -D 1234 -J GRUuser@host3:user@host4 user@host1",
    "ssh -D 1234 -J user@host4:user@host5 user@host1"
]

# Create a radio button for each command
selected_command = tk.StringVar()
for command in commands:
    tk.Radiobutton(root, text=command, variable=selected_command, value=command).pack()

# Create a label to show the connection status
status_label = tk.Label(root, text="Connection: Not connected")
status_label.pack()

# Create a button to run the selected command
button = tk.Button(root, text="Run Command", command=lambda: run_command(selected_command.get()))
button.pack()

# Create a button to close the connection
button = tk.Button(root, text="Close Connection", command=close_connection)
button.pack()

# Start the GUI update thread
thread = threading.Thread(target=update_gui)
thread.start()

# Run the main loop
root.mainloop()
thread.join() # Join the GUI update thread when the main loop is finished

