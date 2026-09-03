import numpy as np
import json
from data_handler import load_students

def main():
    students = load_students("students.csv")

    print("===== Student Performance Report =====\n")

    all_averages = []

    for student in students:
        avg = student.average()
        grade = student.grade()
        all_averages.append(avg)
        print(f"{student.name:10} | Marks: {student.marks} | Average: {avg:.2f} | Grade: {grade}")

    averages_array = np.array(all_averages)

    print("\n----- Class Statistics -----")
    print(f"Class Average: {averages_array.mean():.2f}")
    print(f"Highest Average: {averages_array.max():.2f}")
    print(f"Lowest Average: {averages_array.min():.2f}")
    print(f"Standard Deviation: {averages_array.std():.2f}")

    # ----- Export report as JSON -----
    report_data = {
        "students": [
            {"name": s.name, "marks": s.marks, "average": s.average(), "grade": s.grade()}
            for s in students
        ],
        "class_average": float(averages_array.mean()),
        "highest_average": float(averages_array.max()),
        "lowest_average": float(averages_array.min())
    }

    with open("report_card.json", "w") as f:
        json.dump(report_data, f, indent=2)

    print("\nReport saved to report_card.json")


if __name__ == "__main__":
    main()