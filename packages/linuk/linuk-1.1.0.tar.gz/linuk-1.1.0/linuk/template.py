### Different Kind of numbers

def armstrong_number():
	return'''# Python program to determine whether the number is 
# Armstrong number or not 
  
# Function to calculate x raised to the power y 
def power(x, y): 
    if y==0: 
        return 1
    if y%2==0: 
        return power(x, y/2)*power(x, y/2) 
    return x*power(x, y/2)*power(x, y/2) 
  
# Function to calculate order of the number 
def order(x): 
  
    # variable to store of the number 
    n = 0
    while (x!=0): 
        n = n+1
        x = x/10
    return n 
  
# Function to check whether the given number is 
# Armstrong number or not 
def isArmstrong (x): 
    n = order(x) 
    temp = x 
    sum1 = 0
    while (temp!=0): 
        r = temp%10
        sum1 = sum1 + power(r, n) 
        temp = temp/10
  
    # If condition satisfies 
    return (sum1 == x) 
  
  
# Driver Program 
x = 153
print(isArmstrong(x)) 
x = 1253
print(isArmstrong(x)) '''



def prime_number():
	return '''# Python program to print all  
# prime number in an interval 
  
start = 11
end = 25
  
for val in range(start, end + 1): 
      
   # If num is divisible by any number   
   # between 2 and val, it is not prime  
   if val > 1: 
       for n in range(2, val): 
           if (val % n) == 0: 
               break
       else: 
           print(val) '''


def check_prime():
	return '''# Python program to check if  
# given number is prime or not 
  
num = 11
  
# If given number is greater than 1 
if num > 1: 
      
   # Iterate from 2 to n / 2  
   for i in range(2, num//2): 
         
       # If num is divisible by any number between  
       # 2 and n / 2, it is not prime  
       if (num % i) == 0: 
           print(num, "is not a prime number") 
           break
   else: 
       print(num, "is a prime number") 
  
else: 
   print(num, "is not a prime number") '''


def ascii_value():
	return '''# Python program to print  
# ASCII Value of Character 
  
# In c we can assign different 
# characters of which we want ASCII value  
  
c = 'g'
# print the ASCII value of assigned character in c 
print("The ASCII value of '" + c + "' is", ord(c)) '''

###specials

def font_writer():
	return '''# Python3 code to print input in your own font 
  
name = "GEEK"
  
# To take input from User 
# name = input("Enter your name: \n\n") 
  
lngth = len(name) 
l = "" 
  
for x in range(0, lngth): 
    c = name[x] 
    c = c.upper() 
      
    if (c == "A"): 
        print("..######..\n..#....#..\n..######..", end = " ") 
        print("\n..#....#..\n..#....#..\n\n") 
          
    elif (c == "B"): 
        print("..######..\n..#....#..\n..#####...", end = " ") 
        print("\n..#....#..\n..######..\n\n") 
          
    elif (c == "C"): 
        print("..######..\n..#.......\n..#.......", end = " ") 
        print("\n..#.......\n..######..\n\n") 
          
    elif (c == "D"): 
        print("..#####...\n..#....#..\n..#....#..", end = " ") 
        print("\n..#....#..\n..#####...\n\n") 
          
    elif (c == "E"): 
        print("..######..\n..#.......\n..#####...", end = " ") 
        print("\n..#.......\n..######..\n\n") 
          
    elif (c == "F"): 
        print("..######..\n..#.......\n..#####...", end = " ") 
        print("\n..#.......\n..#.......\n\n") 
          
    elif (c == "G"): 
        print("..######..\n..#.......\n..#.####..", end = " ") 
        print("\n..#....#..\n..#####...\n\n") 
          
    elif (c == "H"): 
        print("..#....#..\n..#....#..\n..######..", end = " ") 
        print("\n..#....#..\n..#....#..\n\n") 
          
    elif (c == "I"): 
        print("..######..\n....##....\n....##....", end = " ") 
        print("\n....##....\n..######..\n\n") 
          
    elif (c == "J"): 
        print("..######..\n....##....\n....##....", end = " ") 
        print("\n..#.##....\n..####....\n\n") 
          
    elif (c == "K"): 
        print("..#...#...\n..#..#....\n..##......", end = " ") 
        print("\n..#..#....\n..#...#...\n\n") 
          
    elif (c == "L"): 
        print("..#.......\n..#.......\n..#.......", end = " ") 
        print("\n..#.......\n..######..\n\n") 
          
    elif (c == "M"): 
        print("..#....#..\n..##..##..\n..#.##.#..", end = " ") 
        print("\n..#....#..\n..#....#..\n\n") 
          
    elif (c == "N"): 
        print("..#....#..\n..##...#..\n..#.#..#..", end = " ") 
        print("\n..#..#.#..\n..#...##..\n\n") 
          
    elif (c == "O"): 
        print("..######..\n..#....#..\n..#....#..", end = " ") 
        print("\n..#....#..\n..######..\n\n") 
          
    elif (c == "P"): 
        print("..######..\n..#....#..\n..######..", end = " ") 
        print("\n..#.......\n..#.......\n\n") 
          
    elif (c == "Q"): 
        print("..######..\n..#....#..\n..#.#..#..", end = " ") 
        print("\n..#..#.#..\n..######..\n\n") 
          
    elif (c == "R"): 
        print("..######..\n..#....#..\n..#.##...", end = " ") 
        print("\n..#...#...\n..#....#..\n\n") 
          
    elif (c == "S"): 
        print("..######..\n..#.......\n..######..", end = " ") 
        print("\n.......#..\n..######..\n\n") 
          
    elif (c == "T"): 
        print("..######..\n....##....\n....##....", end = " ") 
        print("\n....##....\n....##....\n\n") 
          
    elif (c == "U"): 
        print("..#....#..\n..#....#..\n..#....#..", end = " ") 
        print("\n..#....#..\n..######..\n\n") 
          
    elif (c == "V"): 
        print("..#....#..\n..#....#..\n..#....#..", end = " ") 
        print("\n...#..#...\n....##....\n\n") 
          
    elif (c == "W"): 
        print("..#....#..\n..#....#..\n..#.##.#..", end = " ") 
        print("\n..##..##..\n..#....#..\n\n") 
          
    elif (c == "X"): 
        print("..#....#..\n...#..#...\n....##....", end = " ") 
        print("\n...#..#...\n..#....#..\n\n") 
          
    elif (c == "Y"): 
        print("..#....#..\n...#..#...\n....##....", end = " ") 
        print("\n....##....\n....##....\n\n") 
          
    elif (c == "Z"): 
        print("..######..\n......#...\n.....#....", end = " ") 
        print("\n....#.....\n..######..\n\n") 
          
    elif (c == " "): 
        print("..........\n..........\n..........", end = " ") 
        print("\n..........\n\n") 
          
    elif (c == "."): 
        print("----..----\n\n") '''

def reverse_pyramid():
	return '''# python 3 code to print inverted star 
# pattern  
  
# n is the number of rows in which 
# star is going to be printed. 
n=11
  
# i is going to be enabled to 
# range between n-i t 0 with a 
# decrement of 1 with each iteration. 
# and in print function, for each iteration, 
# ” ” is multiplied with n-i and ‘*’ is 
# multiplied with i to create correct 
# space before of the stars. 
for i in range (n, 0, -1): 
    print((n-i) * ' ' + i * '*') '''

