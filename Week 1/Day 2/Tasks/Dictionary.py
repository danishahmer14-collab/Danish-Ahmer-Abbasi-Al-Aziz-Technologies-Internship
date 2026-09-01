#dictionary mapping 3 students to their marks (nested list), then print each student's average using a for loop.

students = {
     "Danish" : [70 ,60 ,80],
         "Ali": [70,50,40 ],
         "DK": [90,80,76]
         }
for name, marks in students.items():
    avg=sum(marks)/len(marks)
    print(name , "Average:" ,avg)
