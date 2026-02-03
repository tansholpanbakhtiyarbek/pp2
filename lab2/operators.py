#PYTHON OPERATORS 
print(6+7)
sum1=100=50

#ARITHMETIC OPERATORS 
x=10
y=3
print(x + y) #Addition
print(x - y) #Subtraction
print(x * y) #Multiplication
print(x / y) #Division
print(x % y) #Modulus
print(x ** y) #Exponentiation
print(x // y) #Floor division


#ASSIGMENT OPERATORS
#The Walrus Operator
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#Comparison Operators
x = 7
y = 5

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)


#Logical operators
#1st example  
x=5
print (x>0 and x<10)

#2nd example
x = 5
print(x < 5 or x > 10)

#Identity operators
#1st example
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)

#2nd example
x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)

#Membership Operators
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)

#Bitwise Operators
print(6 & 3)  #&-AND
print(6 | 3)  # |-OR
print(6 ^ 3)  # ^-XOR
