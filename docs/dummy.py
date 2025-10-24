print("aseem")

#jj asldkj asldj asldkj asldkj asdlkjas ldkja dsl ---> Comment
#Variables Integer
x = 100
y = 200
z = x + y
print(z)

#String variable = characters
underlying = "NIFTY"
strike = 23500
direction = "CE"
expiry = "FEB25"
optionname = underlying  + expiry + str(strike) + direction
print(optionname)

#print, integer variable, string variable

#LIST (arrays)
list1 = ["aa","bb","cc","dd","ee"]
#INDEX    0    1     2   3     4
#INDEX   -5    -4   -3   -2   -1
print(list1[0])
print(list1[1])
print(list1[2])
print(list1[3])
print(list1[4])
print(list1[-1])

#Conditions
a = 1000
b = 1000
if a>b:
    print("a is bigger")
elif b>a:
    print("b is bigger")
else:
    print("both are same")


entry = 100
sl = 80
target = 120
ltp = 105

if ltp > target:
    print("target is hit")
elif ltp < sl:
    print("sl is hit")
else:
    print("keep checking")

#LOOPS WHILE
var1 = 0
while (var1<1):
    print("abc")
    #break
    var1 = 100

#example
var1 = 0
entry = 100
sl = 80
target = 120

while (var1 < 1):
    ltp = 121     #This will keep changing
    if ltp > target:
        print("target is hit")
        break
    elif ltp < sl:
        print("sl is hit")
        break
    else:
        print("keep checking")


#print, integer variable, string variable, list, if/elif/else , while loop, break

#user defined functions
#sumofthreenumbers ---> name of the function
#x, y, z ----> parameters / inputs
def sumofthreenumbers(x,y,z):
    w = x + y + z
    print (w)

#CALL THE FUNCTION
sumofthreenumbers(1,2,3)
sumofthreenumbers(10,20,30)
sumofthreenumbers(13,21,1233)


#Reuse
#i can just call that part of code
#error finding

#print, variables, list, if/elif/else, while, break, user defined functions