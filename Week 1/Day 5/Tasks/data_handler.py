import csv
from students import Student

def load_students(filename):
    students = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            marks = [int(m) for m in row["marks"].split(";")]  # marks stored as "80;90;70" in the CSV
            student = Student(name, marks)
            students.append(student)
    return students