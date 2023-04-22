from tkinter import *
from tkinter import ttk

# root = Tk()

# frame = ttk.Frame(root, padding=10)
# frame.grid()
# ttk.Label(frame, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frame, text="Bye!", command=root.destroy)

# root.mainloop()



def handle_right_click(event):
    print("You found a secret!")

def change_label():
    hello_label["text"] = "Later!"