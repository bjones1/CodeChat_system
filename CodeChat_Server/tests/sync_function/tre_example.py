#
# This file makes use of the approx match written by Dr. Jones and the Tre libraries to find matches between two documents. 
#
# In its current state, the document can take two input files and randomly check different spots in the input to see if that
# text exists in the ouput. 
#

import approx_match 
import random

# used to generate a list of random integers to test the match function for different sections of the code
def Rand(start, end, num):
    res = []
 
    for j in range(num):
        res.append(random.randint(start, end))
 
    return res

# open the two files being examined
f = open('html_example.txt', 'r' )
data = f.read()
f.close()
f = open('conf.py', 'r')
cursorTxt = f.read()
f.close()

# PRint the lenths of the files and ask for user input 
# user input has been removed for 20 random test cases
# print("Python File Length = " + str(len(cursorTxt)))
# print("HTML File Length = :" + str(len(data)))
# print("Enter for Cursor Position in Python File:")

# generate an array of 20 random "cursor" points. 
# Feeling lazy right now and just chopped off the end instead of writing code to check for the end
# that could be copied from approx_match if desired. 
num = 20
start = 20
end = len(cursorTxt) -1500
array = Rand(start, end, num)
print(array)

# for user input
#cursorPos = int(input())

# iterate over the array of Cursor Positions to test the random points
for cursorPos in array:

    print("****************************************************")
    print("Test for Cursor Position: " + str(cursorPos))
    print("***************************************************")
    
    # create a window around the corser this number could be played with depending on how much it affects accuracy and speed
    # I havent run into much issue with a 60 character window, but I also havent tried that many other values
    cursorPosPlus = cursorPos + 30
    cursorPosNeg = cursorPos - 30
    searchTxt = cursorTxt[cursorPosNeg:cursorPosPlus]

    # output the section of the first file that will be searched for. 
    print("Input Txt")
    print("---------------------------------------------")
    print(searchTxt)
    print()

    # search for that section of code in the other file
    print("Matching Txt")
    print("--------------------------------------------")
    
    # approx_match.py lines 142 - 170
    match, beginInTarget, endInTarget = approx_match.findApproxText(searchTxt, data)

    # if the match fails to find something or returns multiple matches, it will return none
    # Approx_match.py has a function to check for narrow or widen the search based on paramaters. 
    if match is None:
        # output that approx text
        targetSubstring, beginInTarget, endInTarget = approx_match.findApproxTextInTarget(data, cursorPos, searchTxt,50)
        #print(approx_match.findApproxTextInTarget(data, cursorPos, searchTxt,50))

    else:
        # the first match function ran successfully it will be output in match [0]
        targetSubstring = match[0]
        
    #print the match
    print(targetSubstring)
    print()




