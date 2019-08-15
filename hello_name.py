#!/usr/bin/env python3
#
# name = input("What's your name? ")
# print("Hello " + name)

decimals = 3
amount = float(input("How much? "))  # Convert input (str) to float
print(f"This much? ${amount:,.{decimals}f}")
