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
root.geometry("600x600")  # max size of the picture

bgimage = tk.PhotoImage(file='/home/plamen/Desktop/Python Mario/mario_mentor/calculator_gui/calc2.png')
label = tk.Label(root, image=bgimage)
label.place(x=0, y=0)

frame1 = tk.Frame(root)
frame1.pack(pady=10)

label1 = tk.Label(frame1, text="Enter first number:")
label1.grid(row=0, column=0)

entry1 = tk.Entry(frame1)
entry1.grid(row=0, column=1)

label2 = tk.Label(frame1, text="Enter second number:")
label2.grid(row=1, column=0)

entry2 = tk.Entry(frame1)
entry2.grid(row=1, column=1)

frame2 = tk.Frame(root)
frame2.pack(pady=5)

operation_var = tk.StringVar(frame2)
operation_var.set("+")  # default value

operation_label = tk.Label(frame2, text="Choose operation:")
operation_label.grid(row=0, column=0)

operation_menu = tk.OptionMenu(frame2, operation_var, "+", "-", "*", "/", "^", "mod", "√")
operation_menu.grid(row=0, column=1)
operation_menu.config(bg="green", fg="white")
operation_menu["menu"].config(bg="red")

calculate_button = tk.Button(frame2, text="Calculate", command=calculate)
calculate_button.grid(row=0, column=2)
calculate_button.configure(bg="orange", fg="black")  # color for calculate button

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
