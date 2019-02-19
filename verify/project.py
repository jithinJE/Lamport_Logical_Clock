delimiter = ' '
inputFileName = "input_1.txt"

# Print 2-dimensional array with Tab separation
def printArray(myArray):
    for rows in myArray:
        for cols in rows:
            print cols,'\t',
        print '\n'


# Read input from file
with open(inputFileName) as f:
    input = [x.split(delimiter) for x in [line.rstrip('\n') for line in f]]

# Convert string to int list
input = [list(map(int, c)) for c in input]


# Initialize values of N & M
N = len(input)
M = len(input[0])

# Initialize result array
result = [['-1' for x in range(M)] for y in range(N)]

# Initialize all dictionaries
send,recv,int_events = {},{},{}
labels = list(map(chr, range(97, 123)))     # alphabets a..z

''' ------------- Initializations Complete ------------- '''

''' ------------- Verifying Lamport Logical Clocks ------------- '''

# Populate dictionaries
for i in range(N):
    prev = 0
    for j in range(M):
        
        if input[i][j] - prev > 1:      # Gap > 1 found between consecutive logical clock            
            recv[input[i][j]] = (i,j)

            found = False
            for l in [x for x in range(N) if x != i]: # Check all process row except the current ith row
                
                for m in range(M): # Check each column for LC(s) -> LC(r) - 1                    
                    if input[l][m] == input[i][j] - 1:
                        found = True
                        send[input[l][m]] = (l,m)

                if found:
                    break

            if not found:       # Invalid case
                print "INVALID" # because Send message not found for {0}".format(input[i][j])
                exit(0)
        
        if input[i][j] == 0:            
            result[i][j] = 'NULL'

        prev = input[i][j]
#Both for loops end


# Populate result array with send and recv events
msg_count = 1
for key, value in sorted(send.iteritems()):
    
    # for send
    i,j = value
    result[i][j] = 's{0}'.format(msg_count)

    # for recv
    i,j = recv[key + 1]     # key is the LC of send
    result[i][j] = 'r{0}'.format(msg_count)

    msg_count += 1

    
# Populate pending elements in result array with internal events
from itertools import cycle
iter = cycle(labels) # init iterator for labels

for i in range(N):
    for j in range(M):
        if result[i][j] == '-1':
            result[i][j] = next(iter)       #use the next available label



        
# Display the output
printArray(result)