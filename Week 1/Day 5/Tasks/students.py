class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks   # list of numbers, e.g. [80, 90, 70]

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