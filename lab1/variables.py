#TYPE
x=54
y="word"

print(type(x))
print(type(y))

x="word"
x='word'
#they are same

a=4
A=4
#not the same variables

#VARIABLE NAMES
name='John'
_age=25
LASTNAME="Kim"
a=5
B=7
log_pass=4984


#MULTIPLE VALUES

#Many Values to Multiple Variables
x,y,z=1,2,3
print(x)
print(y)
print(z)

#One Value to Multiple Variables
x=y=z=7
print(x)
print(y)
print(z)

#Unpack a Collection
numbers=[54,59,62]
x,y,z=numbers
print(x)
print(y)
print(z)

#OUTPUT VARIABLES
#1st example
x="HELLO"
print(x)

#2nd example 
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)

#3rd example 
x = "Python "
y = "is "
z = "awesome"
print(x + y + z)

#4th example 
x = 5
y = 10
print(x + y)

#5th example 
x = 5
y = "John"
print(x, y)

#GLOBAL VARIABLES
#1st example
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()

#2nd example
def myfunc():
  global x
  x = "fantastic"

myfunc()
print("Python is " + x)