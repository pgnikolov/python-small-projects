import tkinter as tk

# root window - main
root = tk.Tk()
root.geometry("240x100")
root.title('Login')
root.resizable(0, 0)

# configure the grid - 2 columns with diff sizes
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# username
username_label = tk.Label(root, text="Username:")
username_label.grid(column=0, row=0, padx=5, pady=5)

username_entry = tk.Entry(root)
username_entry.grid(column=1, row=0, padx=5, pady=5)

# password
password_label = tk.Label(root, text="Password:")
password_label.grid(column=0, row=1, padx=5, pady=5)

# with hidding the input instead of letters it shows *
password_entry = tk.Entry(root,  show="*")
password_entry.grid(column=1, row=1, padx=5, pady=5)

# login button
login_button = tk.Button(root, text="Login")
login_button.grid(column=1, row=3, padx=5, pady=5)


root.mainloop()
