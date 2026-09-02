#Functions in programing laguages refer to reusable block of code which are defined once and can be used whenever needed
#Parameters are the variable names in the function definition. here a,b are the parameters 
#Arguments = the actual values you pass in when calling it. here 3,5 are the arguments the values given to function
#return sends a value back out of the function

def add(a, b):
    return a + b

result = add(3, 5)   

# Default Parameters are used to give a default value in a function eg by default name is guest if user wants to change it he is allowed to

def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()          # gives Hello, Guest!
greet("Danish")  # gives Hello, Danish!

#*args and **kwargs
#Let a function accept an unknown number of arguments.
#*args collects extra positional arguments into a tuple.
#**kwargs collects extra keyword arguments into a dictionary.
def total(*args):
    return sum(args)

print(total(1, 2, 3))   # 6

def show_info(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

show_info(name="Danish", age=20)