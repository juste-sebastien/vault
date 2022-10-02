from os import RWF_APPEND
from tkinter import *
from tkinter import ttk


root = Tk()
root.title("Vault App by Cabron")
root.minsize(height=600, width=400)
root.configure(background="red")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style = ttk.Style()
style.configure("Main.TFrame", background="blue", relief="raised")

mainframe = ttk.Frame(
    root,
    padding="3 3 12 12",
    height=400,
    width=200,
    style="Main.TFrame",
)
mainframe.grid(column=0, row=0, columnspan=3, rowspan=10, sticky=(N, W, E, S))

ttk.Label(mainframe, text="Vault App").grid(column=1, row=0, sticky=(W, E))
logo = ttk.Label(mainframe, text="Logo").grid(column=1, row=2)
ttk.Label(mainframe, text="Login").grid(column=1, row=3, sticky=(W, E))
ttk.Label(mainframe, text="Password").grid(column=1, row=6, sticky=(W, E))
ttk.Label(mainframe, text="All rigths reserved").grid(column=1, row=10, sticky=(W, E))


login = StringVar()
login_entry = ttk.Entry(mainframe, width=15, textvariable=login)
login_entry.grid(column=1, row=4, sticky=(W, E))

pwd = StringVar()
pwd_entry = ttk.Entry(mainframe, width=15, textvariable=pwd, show="*")
pwd_entry.grid(column=1, row=7, sticky=(W, E))

ttk.Button(mainframe, text="Connect").grid(column=1, row=9, sticky=(W, E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

login_entry.focus()

root.mainloop()
