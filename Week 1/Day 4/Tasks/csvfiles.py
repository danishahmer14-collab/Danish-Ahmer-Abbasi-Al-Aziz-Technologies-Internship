import csv

# Writing
with open("student.csv", "w" , newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["name","age","marks"])
    writer.writerow(["Danish","23","80"])
    writer.writerow(["Danny","22","60"])

#Reading 
with open("student.csv","r") as f:
    reader=csv.reader(f)
    for row in reader:
        print(row)

#Reading with Dictionary 
with open("student.csv","r") as f:
    reader=csv.DictReader(f)
    for row in reader:
        print(row["name"] ,row["marks"])

            

