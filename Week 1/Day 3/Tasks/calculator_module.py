def add(a, b):
    return a+b

def subtract(a, b):
    return a-b

def multiply(a, b):
    return a*b

def divide(a, b):
    if a != 0 and b != 0:
        return a / b
    else:
        print("Cannot divide when a or b is 0")
        return None