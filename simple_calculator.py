# **Simple Calculator**
#
# **Description:**
# You are tasked with creating a simple calculator program in Python that can perform basic arithmetic operations:
# addition, subtraction, multiplication, and division. The program should prompt the user to input two numbers
# and the operation they want to perform, then display the result.
#
# **Parts of the Task:**
#
# 1. **Input Numbers:**
#    - Description: Prompt the user to input two numerical values.
#    - Additional Information: Ensure that the inputs are numeric, as they will be used for arithmetic calculations.
#
# 2. **Input Operation:**
#    - Description: Ask the user to specify the arithmetic operation they want to perform
#    (addition, subtraction, multiplication, or division).
#    - Additional Information: Validate the input to ensure it matches one of the specified operations.
#
# 3. **Perform Calculation:**
#    - Description: Based on the selected operation, perform the corresponding arithmetic
#    calculation using the two input numbers.
#    - Additional Information: Use conditional statements (if-elif-else) to determine which operation to perform.
#
# 4. **Print Result:**
#    - Description: Display the result of the arithmetic operation to the user.
#    - Additional Information: Format the output message to make it clear and readable,
#    and handle division by zero cases.
#
# **Sample Input/Output:**
#
# ```
# Enter the first number: 10
# Enter the second number: 5
# Enter the operation (+, -, *, /): *
# Result: 10 * 5 = 50
#
# Enter the first number: 8
# Enter the second number: 4
# Enter the operation (+, -, *, /): /
# Result: 8 / 4 = 2.0
#
# Enter the first number: 15
# Enter the second number: 7
# Enter the operation (+, -, *, /): $
# Invalid operation! Please enter a valid operation.
# ```

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
    result = num1 / num2
    return f"Result: {num1} / {num2} = {result}"


def calculator():
    num1 = int(input("Enter first number:"))

    while True:
        num2 = int(input("Enter second number:"))
        operation = input("Enter the operation (+, -, *, /):")

        if operation == "+":
            print(addition(num1, num2))
        elif operation == "-":
            print(subtraction(num1, num2))
        elif operation == "*":
            print(multiplication(num1, num2))
        elif operation == "/":
            if num2 == 0:
                print("Division by 0 is impossible")
                break
            else:
                print(division(num1, num2))
        else:
            print("Invalid operation! Please enter a valid operation.")


calculator()
