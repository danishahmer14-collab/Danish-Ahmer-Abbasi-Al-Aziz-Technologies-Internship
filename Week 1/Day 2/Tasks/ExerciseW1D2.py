#given a list of numbers to print only even numbers using for loop covers if statement for loop and list comprehension 
numbers = [1,2,3,4,5,6,7,8]
for i in numbers:
    if i%2==0:
        print(i)
#using list comprehension to create a new list of their squares        
squares = [i**2 for i in numbers]
print(squares)    
#Given a sentence (string), split it into words and store unique words using a set.
sentence = "the cat sat on the mat and the dog ran"
words = sentence.split()
unique_words = set(words)   # which data structure converts a list to remove duplicates?
print(unique_words)