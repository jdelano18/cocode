import sys

try:
    print(sys.argv[1])
except IndexError:
    print("enter the file you want to split as argv[1] from command line")
