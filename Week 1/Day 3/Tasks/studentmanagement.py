class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"Hi, I'm {self.name} and I'm {self.age} years old.")


class Student(Person):
    def __init__(self, name, age, roll_no, marks):
        super().__init__(name, age)   # reuse Person's constructor
        self.roll_no = roll_no
        self.marks = marks            # list of marks, e.g. [80, 90, 70]

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        else:
            return "F"

    def report(self):
        print(f"--- Report for {self.name} (Roll No: {self.roll_no}) ---")
        self.introduce()
        print(f"Marks: {self.marks}")
        print(f"Average: {self.average():.2f}")
        print(f"Grade: {self.grade()}")
        print()


class Classroom:
    def __init__(self, class_name):
        self.class_name = class_name
        self.students = []          # will hold Student objects

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        total = sum(s.average() for s in self.students)
        return total / len(self.students)

    def show_all_reports(self):
        print(f"===== {self.class_name} — Student Reports =====\n")
        for student in self.students:
            student.report()
        print(f"Class Average: {self.class_average():.2f}")


# ---- Using the application ----
if __name__ == "__main__":
    s1 = Student("Ali", 20, 101, [80, 90, 70])
    s2 = Student("Sara", 19, 102, [95, 85, 100])
    s3 = Student("Danish", 20, 103, [60, 75, 88])

    my_class = Classroom("AI Engineering Batch 1")
    my_class.add_student(s1)
    my_class.add_student(s2)
    my_class.add_student(s3)

    my_class.show_all_reports()