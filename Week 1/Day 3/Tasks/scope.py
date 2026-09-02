#Scope
#Where a variable can be accessed.
#Local scope: variables defined inside a function only exist there.
#Global scope: variables defined outside any function, accessible everywhere.
x = 10   # global variable

def show():
    y = 5   # local variable to this function
    print(x, y)   # can read global x here

show()
# print(y)  # ERROR - y doesn't exist outside the function