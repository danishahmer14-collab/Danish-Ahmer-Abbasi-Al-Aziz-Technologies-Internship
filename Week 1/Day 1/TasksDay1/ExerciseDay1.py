#comments are started with # symbol in python
#Variables dont need to be deckared hust assign them like  
name = "Danish"
age = 20
is_intern = True

# Data Types in python 
x = 10          # int
y = 3.14        # float
z = 2 + 3j      # complex

# strings Bolean Arthemetic operation input and output and Error hanlind are used in my coding practice files 
#program to swap two number without a third number
a = 5
b=7 
a,b=b,a
print("The swapped numbers are",a,b)

#program which takes input from user and check if number is Even or odd this program also converts datatype to integer
num = int(input("Enter a number: "))
if(num%2==0):
    print("Number is Even")
else: 
    print("Number is ODD")

#program converting a string into integer also covering error handling
number = input("Enter a number: ")
try:
    integer_num = int(number)
    print(integer_num + 5)
except ValueError:
    print("That's not a valid whole number!")

#program to calculate Area of Rectangle by taking Length and Width as Input from user
Length = int(input("Enter the Lenght of Rectangle: "))
Width =  int(input("Enter the Width of Rectangle: "))
Area = Length * Width 
print("Area = " , Area)


#program to Divide number and use error exection
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

try:
    result = num1 / num2
    print("Result =", result)
except ZeroDivisionError:
    print("Error number cannot be divided by zero")
