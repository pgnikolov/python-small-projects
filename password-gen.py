import random
import string

chars = string.ascii_letters + string.digits + string.punctuation

print("Password Generator!")

password_length = int(input("Enter password length: "))
password_list = []

for char in range(1, password_length + 1):
    password_list.append(random.choice(chars))

print(f"Your password is: {''.join(password_list)}")
