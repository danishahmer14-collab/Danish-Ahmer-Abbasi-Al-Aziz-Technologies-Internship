#Lambda Functions
#Small, anonymous, one-line functions.

square = lambda x: x ** 2
print(square(5))   

# Commonly used as a quick function passed to sorted(), map(), filter()
# Lambda Functions to sort  in descending order
nums = [3, 1, 4, 1, 5]
print(sorted(nums, key=lambda x: -x))  
