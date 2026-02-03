#sets
thisset = {"apple", "banana", "cherry"}
print(thisset)    #Duplicate values will be ignored

#True and 1 is considered the same value
#False and 0 is considered the same value
thisset = {"apple", 1,"banana", "cherry", False, True, 0}
print(thisset)

#Length of a Set
thisset = {"apple", "banana", "cherry"}
print(len(thisset))

#type
myset = {"apple", "banana", "cherry"}
print(type(myset))

#Access Set Items
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)


thisset = {"apple", "banana", "cherry"}
print("banana" in thisset)

#Add Set Items
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)

thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)


#Remove Set Items
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset)

thisset = {"apple", "banana", "cherry"}
thisset.discard("banana")
print(thisset)

#The clear() method
thisset = {"apple", "banana", "cherry"}
thisset.clear()
print(thisset)

#Loop Sets
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)

 
#Join Sets
#The union() method 
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)
#the | operator instead of the union() method, and you will get the same result.

#Join a Set and a Tuple
x = {"a", "b", "c"}
y = (1, 2, 3)

z = x.union(y)
print(z)

#The update() method
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}

set1.update(set2)
print(set1)

#The intersection() method
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.intersection(set2)
print(set3) 
#use the & operator instead of the intersection() method

#Set difference() Method
x = {"apple", "banana", "cherry"}
y = {"google", "microsoft", "apple"}
z = x.difference(y)
print(z)
# use the - operator instead of the difference() method

#The symmetric_difference() method
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.symmetric_difference(set2)
print(set3)
#use the ^ operator instead of the symmetric_difference() method

#frozenset
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))