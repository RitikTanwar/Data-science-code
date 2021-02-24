# from calculator import add  -># import a particular func
# print(add(5,7))

# from calculator import *  # import all fucntions
# print(sub(20,12))
# print(div(4,5))

# # globals show all the varibles in file
# print(globals())

# alias 
# import calculator as lib
# print(lib.add(46,23))

from calculator import (
    add as sum,
    sub as diff
)

print(sum(5,7))
print(diff(79,67))