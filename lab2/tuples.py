#tuples 
thistuple = ("apple", "banana", "cherry")
print(thistuple)

#Tuples allow duplicate values
thistuple = ("apple", "banana", "cherry", "apple", "cherry")
print(thistuple)

#Tuple Length
thistuple = ("apple", "banana", "cherry")
print(len(thistuple))

#type()
mytuple = ("apple", "banana", "cherry")
print(type(mytuple))

#Access Tuple Items
thistuple = ("apple", "banana", "cherry")
print(thistuple[1])

#Update Tuples
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)

print(x)

#Add Items
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)

#Add tuple to a tuple
thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y

print(thistuple)

#Remove Items
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)

# delete the tuple completely
thistuple = ("apple", "banana", "cherry")
del thistuple
print(thistuple)

#Loop Tuples
#1
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)

#2
thistuple = ("apple", "banana", "cherry")
for i in range(len(thistuple)):
  print(thistuple[i])

#While Loop
thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1

#Join Tuples
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)

tuple3 = tuple1 + tuple2
print(tuple3)

#Multiply Tuples
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2

print(mytuple)

