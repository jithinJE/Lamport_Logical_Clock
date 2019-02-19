delimiter = ' '
inputFileName = "input.txt"

# Handles each event by assigning a Lamport clock number to it
def HandleEvent(event, i , j):   

    if event == 'NULL':         # NULL event
        result[i][j] = 0

    elif event[0] == 's':       # send event
        result[i][j] = counters[i] + 1
        send[event[1]] = result[i][j]
        counters[i] = result[i][j]

    elif event[0] == 'r':       # receive event
        if event[1] in send:
            result[i][j] = max( counters[i], send[event[1]] ) + 1
            counters[i] = result[i][j]
        else:
            return False

    else:                       # internal event
        result[i][j] = counters[i] + 1        
        counters[i] = result[i][j]

    return True

# Print 2-dimensional array with Tab separation
def printArray(myArray):
    for rows in myArray:
        for cols in rows:
            print cols,'\t',
        print '\n'


# Check if Algorithm is complete by searching for any remaining -1 (default value) in result array
def CheckComplete():

    return not any(-1 in sublist for sublist in result)


# Read input from file
with open(inputFileName) as f:
    input = [x.split(delimiter) for x in [line.rstrip('\n') for line in f]]

# Initialize values of N & M
N = len(input)
M = len(input[0])

# Initialize send dictionry
send = {}

# Initialize result array
result = [[-1 for x in range(M)] for y in range(N)]

# Initialize counter for each process
counters = [0 for x in range(N)]

''' ------------- Initializations Complete ------------- '''

''' ------------- Calculating Lamport Logical Clocks ------------- '''

while not CheckComplete():
    for i in range(N):
        for j in range(M):
            
            if result[i][j] == -1:
                if not HandleEvent(input[i][j], i , j):
                    break


printArray(result)