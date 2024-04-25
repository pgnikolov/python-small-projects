import tkinter as tk
import math


def addition(num1, num2):
    result = num1 + num2
    return f"Result: {num1} + {num2} = {result}"


def subtraction(num1, num2):
    result = num1 - num2
    return f"Result: {num1} - {num2} = {result}"


def multiplication(num1, num2):
    result = num1 * num2
    return f"Result: {num1} * {num2} = {result}"


def division(num1, num2):
    if num2 == 0:
        return "Division by 0 is impossible"
    else:
        result = num1 / num2
        return f"Result: {num1} / {num2} = {result}"


def square(num1, num2):
    num2 = 2
    result = num1 ** num2
    return f"Result: {num1} ** {num2} = {result}"


def modulus(num1, num2):
    result = num1 % num2
    return f"Result: {num1} mod {num2} = {result}"


def square_root(num1):
    result = math.sqrt(num1)
    return f"Result: √{num1} = {result}"


def calculate():
    num1 = int(entry1.get())
    num2 = int(entry2.get())
    operation = operation_var.get()

    if operation == "+":
        result_label.config(text=addition(num1, num2))
    elif operation == "-":
        result_label.config(text=subtraction(num1, num2))
    elif operation == "*":
        result_label.config(text=multiplication(num1, num2))
    elif operation == "/":
        result_label.config(text=division(num1, num2))
    elif operation == "^":
        # entry2.configure(state="disabled")             Tried to make num2 entry disabled for square
        result_label.config(text=square(num1, num2))
    elif operation == "mod":
        result_label.config(text=modulus(num1, num2))
    elif operation == "√":
        result_label.config(text=square_root(num1))
    else:
        result_label.config(text="Invalid operation! Please enter a valid operation.")


root = tk.Tk()
root.title("Calculator")
root.config(bg="#12CBC4")  # add background collor to the main window

frame1 = tk.Frame(root)
frame1.pack(pady=10)
frame1.configure(bg="#12CBC4")   # add collor to first frame( around the "Enter first number")

label1 = tk.Label(frame1, text="Enter first number:", bg="#12CBC4")     # fill with collor background "first number"
label1.grid(row=0, column=0)

entry1 = tk.Entry(frame1)
entry1.grid(row=0, column=1)

label2 = tk.Label(frame1, text="Enter second number:", bg="#12CBC4")    # # fill with collor background "second number"
label2.grid(row=1, column=0)

entry2 = tk.Entry(frame1)
entry2.grid(row=1, column=1)

frame2 = tk.Frame(root)
frame2.pack(pady=5)
frame2.configure(bg="#12CBC4")      # # add collor to first frame( around the "Enter second number")

operation_var = tk.StringVar(frame2)
operation_var.set("+")  # default value

operation_label = tk.Label(frame2, text="Choose operation:", bg="#12CBC4")  # fill background "choose operation"
operation_label.grid(row=0, column=0)

operation_menu = tk.OptionMenu(frame2, operation_var, "+", "-", "*", "/", "^", "mod", "√")
operation_menu.grid(row=0, column=1)
operation_menu.config(bg="green", fg="white", highlightbackground="#12CBC4")    # background for the option menu
operation_menu["menu"].config(bg="red")              # background for the options list

calculate_button = tk.Button(frame2, text="Calculate", command=calculate)
calculate_button.grid(row=0, column=2)
calculate_button.configure(bg="orange", fg="black")  # color for calculate button
calculate_button.config(highlightbackground="#12CBC4")  # change the borders collor the calculate button

result_label = tk.Label(root, text="")
result_label.pack(pady=10)
result_label.configure(bg="#12CBC4")  # result space with the same color of the background

root.mainloop()
