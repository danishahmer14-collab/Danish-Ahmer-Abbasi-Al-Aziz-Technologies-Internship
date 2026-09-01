#tupe indexing and slicing 
#printing first then ast then middle value
Games = ("COD","PUBG","Fortnight","DynastyEdge","Roblox")
print("First" , Games[0])
print("Last" , Games[-1])
print("Middle" , Games[1:4])

# if-elif else
marks = int(input("Enter your marks: "))

if marks >= 90:
    print("Grade: A")
elif marks > 80:
    print("Grade: B")
elif marks >= 70:
    print("Grade: C")
else:
    print("Grade: F")