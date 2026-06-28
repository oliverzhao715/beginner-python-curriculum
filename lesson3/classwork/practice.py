# Problem 1
# Ask the user to enter their height in centimeters.
# Print "Tall" if the height is greater than 170, otherwise print "Short".
prompt = int(input("Please enter your height in centimeters: "))

if prompt > 170:
    print("Tall")
else:
    print("Short")


# Problem 2
# Ask the user for their age.
# If they are 18 or older, print "Adult", else print "Minor".
prompt = int(input("what is your age? "))
if prompt >= 18:
    print("Adult")
else:
    print("Minor")


# Problem 3
# Ask the user to enter a number.
# Print "Fizz" if it is divisible by 3, "Buzz" if divisible by 5,
# print "FizzBuzz" if divisible by both 3 and 5,
# otherwise print the number itself.
prompt = int(input("enter a number: "))
if prompt % 3== 0 and prompt % 5 == 0:
    print("FizzBuzz")
elif prompt % 3 == 0:
    print("Fizz")
else:
    print("Buzz")


# Problem 4
# Ask for age and height.
# If age is at least 10 AND height is at least 120 cm, print "You can ride!"
# Otherwise, print "Sorry, you can't ride."
age = int(input("what is your age?: "))
height = int(input("what is your height?: "))
if age >= 10 and height >= 120:
    print("you can ride")
else:
    print("you can't ride")


# Problem 5
# Ask the user for a number.
# If it's divisible by 3 AND (either less than 0 OR greater than 100), print "Weird number!"
# Otherwise, print "Normal number."
promptnumber = int(input("enter a number: "))
if promptnumber % 3 == 0 and (promptnumber < 0 or promptnumber > 100):
    print("Weird number!")
else:
    print("Normal number.")