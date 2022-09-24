#In the example: x=9,multiplier=50
# 9%50 => 50*0+9 => 9   Result will always be smaller than 50 (the 2nd num)
#In the example: x=50,multiplier=9
# 50%9 =>  9*5+5 => 5   Result will always be smaller than  9 (the 2nd num)

# Prints are really slow operations in every language (not certain about disparity of assembly),
#   hence why they are all commented out for benchmarking purposes. The prints exist to make sure
#   the code is operating correctly. # Comments are necessary instead of "if debug:" because
#   "if debug:" requires processing, which affects the results unevenly due to differents #s of
#   prints being called per function definition

import time

#Short code (one line!), extremely short runtime
def modulo1(x,multiplier):
    startTime = time.perf_counter_ns()
    remainder = x-x//multiplier*multiplier
#    print('One liner:',x,'%',multiplier,'=',remainder)
    # x - ((x//multiplier)*multiplier)    where // is int division (division that yields an integer)
    #E.g. x=25, mult=19      25 - 25//19 * 19   =>   25 - 1*19   =>   25-19   => 6
    endTime = time.perf_counter_ns()
    timeElapsed = (endTime-startTime)/1e9
#    print(str(timeElapsed),'seconds')
#    print()
    return timeElapsed

#Short code, longer runtime than MultAdd
def moduloAddOnly(x,multiplier):
    startTime = time.perf_counter_ns()
    temp = multiplier
#    print('All Adds:',x,'%',temp)
    if x>=multiplier:
        while (multiplier+temp) <= x:
            multiplier += temp
            #print('multiplier:',multiplier)
        remainder = x-multiplier
        if remainder < 0:    #If negativeNum, flip sign
            remainder *= -1
            #print(multiplier,'-(x)',x,'=',remainder)
        #else:
        #    print(x,'-(mult)',multiplier,'=',remainder)
#    else:
#        print(x,'%',multiplier,'=',x)
#    print(x,'%',temp,'=',remainder)
    endTime = time.perf_counter_ns()
    timeElapsed = (endTime-startTime)/1e9
#    print(str(timeElapsed),'seconds')
#    print()
    return timeElapsed

#Longer code, shorter runtime
def moduloMultiplyAndAdd(x,multiplier):
    startTime = time.perf_counter_ns()
    temp = multiplier
#    print('Multiplies, then Adds:',x,'%',temp)
    if x>=multiplier:
        while (multiplier<<1) <= x:        #Multiply by 2 until the next multiply would make multiplier>x
            multiplier = multiplier<<1
            #print('multiplied multiplier:',multiplier)
        while (multiplier+temp) <= x:      #Add original num until the next add would make multiplier2 barely go over x
            multiplier += temp
            #print('added multiplier:',multiplier)
        #print('FINAL multiplier:',multiplier)
        remainder = x-multiplier
        if remainder < 0:    #If negativeNum, flip sign
            remainder *= -1
            #print(multiplier,'-(x)',x,'=',remainder)
        #else:                    #If positiveNum, calculate normally
        #    print(x,'-(mult)',multiplier,'=',remainder)
#    else:  #if x<multiplier
#        print(x,'%',multiplier,'=',x)
#        print(x,'%',temp,'=',remainder)
    endTime = time.perf_counter_ns()
    timeElapsed = (endTime-startTime)/1e9
#    print(str(timeElapsed),'seconds')
#    print()
    return timeElapsed



#'x' is for creating a file, throwing an error if the file already exists.
#'w' is for writing to file, overwriting if it already exists, creating a file if it DNE.
#'a' is for appending to file, creating a file if it DNE.
#file = open("x_multiplier_Time.csv","w")   This does NOT safely exit the file in case of a thrown error, next line does
with open("x_multiplier_Time.csv","w") as file:

    upperLimit = 30900900
    multiplier = 400
    x = 0
    numJump = (multiplier-1)*1000
    while x<upperLimit:
        iteration = timeElapsedAddOnly = timeElapsedMultAdd = timeElapsedFundamentalMod = 0
        numTestsForOneValueOfXandMultiplier = 500        #Change me!   Higher num = more tests = greater accuracy
        while iteration<numTestsForOneValueOfXandMultiplier:
            timeElapsedFundamentalMod += modulo1(x,multiplier)
            timeElapsedMultAdd += moduloMultiplyAndAdd(x,multiplier)
            timeElapsedAddOnly += moduloAddOnly(x,multiplier)
            iteration += 1
        x += numJump    #Test a new pair of numbers

        #Average each test's time value
        avgTimeFundamental = timeElapsedFundamentalMod/numTestsForOneValueOfXandMultiplier
        avgTimeMultAdd = timeElapsedMultAdd/numTestsForOneValueOfXandMultiplier
        avgTimeAddOnly = timeElapsedAddOnly/numTestsForOneValueOfXandMultiplier

        print(f'x {x}, multiplier {multiplier}, avgTimeFundamental {avgTimeFundamental}, ', end='')
        print(f'avgTimeMultAdd {avgTimeMultAdd:0.10f}, avgTimeAddOnly {avgTimeAddOnly:0.10f}')

        #Does write() automatically use newline? NOPE.
        #Since this is Windows, use CRLF (Carriage Return=CR='\r, Line Feed=LF=newline='\n'). NOPE NVM. USE EITHER \r OR \n BUT NOT BOTH
        file.write(f'{x}, {multiplier}, {avgTimeFundamental}, {avgTimeMultAdd:0.9f}, {avgTimeAddOnly:0.9f}\r')

    file.close()

#See the info I'm writing to the file
#file = open("x_multiplier_Time.csv","r")    #'r' is for read from file
#print( file.read() )
#file.close()