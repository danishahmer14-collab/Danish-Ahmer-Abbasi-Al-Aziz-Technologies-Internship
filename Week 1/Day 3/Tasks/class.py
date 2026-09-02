#A class is a blueprint. An object is a specific instance built from it.
class Student:
    pass

s1 = Student()   # s1 is an object (instance) of the Student class
#Constructors
#Runs automatically when you create a new object, used to set up initial data.
#self refers to the specific object being created/used.
#the basic concept of constructor is to prevent any default garbage values to object of the class 
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

s1 = Student("Ali", 20)
print(s1.name, s1.age)   # Ali 20


#Methods
#Functions defined inside a class, used to give objects behavior.
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

s1 = Student("Ali", [80, 90, 70])
print(s1.average())   # 80.0
#Inheritance Basics
#A class can inherit attributes/methods from another class (avoids repeating code).
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hi, I'm {self.name}")

class Student(Person):          # Student inherits from Person
    def __init__(self, name, roll_no):
        super().__init__(name)  # call the parent's __init__
        self.roll_no = roll_no

s1 = Student("Ali", 101)
s1.greet()                      # inherited method works: Hi, I'm Ali
print(s1.roll_no)               # 101