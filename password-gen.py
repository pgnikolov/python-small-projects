import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Password Generator!")

letters_amount = int(input("How many letters you want in your password?\n"))
symbols_amount = int(input(f"How many symbols you want?\n"))
digit_amount = int(input(f"How many numbers you want?\n"))
password_list = []

for char in range(1, letters_amount + 1):
    password_list.append(random.choice(letters))

for char in range(1, symbols_amount + 1):
    password_list += random.choice(symbols)

for char in range(1, digit_amount + 1):
    password_list += random.choice(numbers)

print(password_list)
random.shuffle(password_list)
print(password_list)

password = ""
for char in password_list:
    password += char

print(f"Your password is: {password}")