from subprocess import call
import sys 
x = 5
y = "hallo"
# print(call("python3.7 test.py {} {}".format(x,y), shell=True))
z = call("python3.7 test.py {} {}".format(x,y), shell=True)
f = open("result.txt", "r")
content = f.read()
print(content)