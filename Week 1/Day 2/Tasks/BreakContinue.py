#Use a while loop with break to keep asking the user for numbers until they type "stop", then print the sum of all numbers entered.

total = 0
while True:
    value = input("Enter a number (or type 'stop' to finish): ")
    if value.lower() == 'stop':
        break
    total = total + int(value)

print("Sum of all numbers entered:", total)

#Given a list with duplicate numbers, use continue inside a loop to skip numbers already printed once (basic dedup logic without using a set).

numbers = [1, 2, 3, 2, 4, 1, 5, 3, 6]
seen = []

for num in numbers:
    if num in seen:
        continue
    print(num)
    seen.append(num)