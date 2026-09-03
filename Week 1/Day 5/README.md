# Week 1 — Day 5

## Task(s) Assigned
Complete Week 1 revision covering Python syntax, data types, data structures, conditions, loops, functions, modules, OOP, virtual environments, JSON/CSV, APIs, and NumPy basics. Build a working project combining these concepts.

## What I Did
All concepts from Week 1 reviewed, then created a Student Performance Tracker as a Week 1 Master Project. The project reads the student data from a CSV file, then it calculates the average and grade for each student using an Object-Oriented `Student` class and stats for the class using NumPy (average, highest, lowest, standard deviation), and finally exports the full report as a json file. I broke up the code into individual modules (students.py, data_handler.py and main.py), generated a requirements.txt file with the command "pip freeze", and used a specific virtual environment for this project.API's and requests were not covered in my project as they dont felt like meaning according to the project

## Key Learnings
I found this project very helpful since it gave me a sense of how each of the topics I learned over the week actually interrelate in a real application, as opposed to separate stand-alone exercises. I learned why projects are broken up by responsibilities (data handling in one file rather than in the Student class nor in the main program flow) and why it helps to make projects easier to read and maintain. I also found out that not all topics have to go into a project because they have to "check a box", I had to learn how to use pip freeze and requirements.txt to make my project reproducible for any others who reuse/copy it.

## Files in this folder
- `Tasks/` consists of Week 1 deliverable project (Student Performance Tracker) contains `students.py`, `data_handler.py`, `main.py`, `students.csv`, `requirements.txt`, and `report_card.json`.
