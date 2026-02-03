#Boolean Values

print (77<99)
print(7<=7)
print(10>11)

a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#Evaluate Values and Variables
print(bool("Hello, World"))
print(bool(0))

x=" "
y=12
print(bool(x))
print(bool(y))

#False Values
bool(False)
bool(0)
bool(None)
bool("")
bool(())
bool([])
bool({})

#Functions can Return a Boolean
#1st example 
def myFunction() :
  return True

print(myFunction())

#2nd example
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

#isinstance() 
#1
x = 200
print(isinstance(x, int))

#2
x = 200
print(isinstance(x, float))