import tkinter as tk
import subprocess

# Create a function to run the selected command
def run_command(command):
    # Run the command using the subprocess module
    global process
    process = subprocess.Popen(command.split())

# Create a function to close the connection
def close_connection():
    # Terminate the process
    process.terminate()

# Create the GUI
root = tk.Tk()
root.title("SSH Proxy Selector")

# Create a list of commands
commands = [
    "ssh -D 1234 user@host1",
    "ssh -D 1234 -J user@host2:user@host3 user@host1",
    "ssh -D 1234 -J user@host2:user@host3:user@host4 user@host1",
    "ssh -D 1234 -J user@host2:user@host3:user@host4:user@host5 user@host1"
]

# Create a radio button for each command
selected_command = tk.StringVar()
for command in commands:
    tk.Radiobutton(root, text=command, variable=selected_command, value=command).pack()

# Create a button to run the selected command
button = tk.Button(root, text="Run Command", command=lambda: run_command(selected_command.get()))
button.pack()

# Create a button to close the connection
button = tk.Button(root, text="Close Connection", command=close_connection)
button.pack()

# Run the main loop
root.mainloop()
