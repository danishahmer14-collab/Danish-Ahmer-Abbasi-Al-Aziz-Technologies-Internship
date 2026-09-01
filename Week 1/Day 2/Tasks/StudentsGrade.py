
#Covers dictionaries, nesting, and now nested loops
students = {
    "Ali": {"Math": 85, "Science": 90, "English": 78},
    "Sara": {"Math": 92, "Science": 88, "English": 95}
}

for name, subjects in students.items():
    print(f"Report for {name}:")
    for subject, grade in subjects.items():
        print(f"  {subject}: {grade}")