src = open("noreadablemackcode.txt", "r")
output = open("mackcodeoutput1.txt", "a+")
store = []
stack = []
chars = []
while True:
    line = src.readline().strip('\n')

    if line == "+":
        first = 0
        second = 0
        if str(type(stack[0])).count('str') > 0:
            first = ord(stack[0])
        else:
            first = stack[0]

        if str(type(stack[1])).count('str') > 0:
            second = ord(stack[1])
        else:
            second = stack[1]
        
        stack.insert(0, second + first)
    elif line == "-":
        first = 0
        second = 0
        if str(type(stack[0])).count('str') > 0:
            first = ord(stack[0])
        else:
            first = stack[0]

        if str(type(stack[1])).count('str') > 0:
            second = ord(stack[1])
        else:
            second = stack[1]
        stack.insert(0, second - first) 
    elif line == "x":
        first = 0
        second = 0
        if str(type(stack[0])).count('str') > 0:
            first = ord(stack[0])
        else:
            first = stack[0]

        if str(type(stack[1])).count('str') > 0:
            second = ord(stack[1])
        else:
            second = stack[1]
        stack.insert(0, second * first)
    elif line == "compare":
        continue
    elif line == "LOAD":
        continue
    elif line == "STACK":
        stack.insert(0, store[stack[0]-1])
        
    elif line == "STR":
        store.insert(0, stack[1])
        del stack[1]
    elif line == "JMP":
        continue
    elif line == "CHAR":
        char = chr(stack[0])
        stack.insert(0, char)
        chars.insert(0, char)
    elif line == "INPUT":
        continue
    elif line == "EXIT":
        break;
    else:
        pushed = int(line)
        stack.insert(0, pushed)

for i in range(0, len(chars)):
    print(chars[i], end='')
    
