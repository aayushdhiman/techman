## MackLang
The first thing that was given for this project was a series of instructions "Mack code" and a readme explaining what each occurrence of "MACK" can mean in a given instance. To pass this challenge, the MACK code needs to be analyzed, assembled, and ran to see the output.

### Steps

1. A python script mack2assembly.py was used to translate the Mack code into a more readable assembly based off of the definitions given in the readme
2. Have the mack2assembly.py file in the same directory as the MACK file. Run python mack2assembly.py to output a new file nomackcode.txt
3. When analyzing nomackcode.txt you’ll notice that certain commands listed in the README aren’t listed while others are extremely common. 
4. The CHR, STR, LOAD, ADD, SUB, MULT, and PUSH commands were all extremely common. When looking further I noticed that a series of letters are being created with the CHR command.
5. I created and ran a python script mackruntime.py that followed the instructions in nomackcode.txt and captured the string of characters being created by the CHR command
6. To do this, have mackruntime.py in the same directory and run python mackruntime.py 
7. The output will be the string S0VZezQgMiAyIDQgMSA2IDMgN30= 
8. When decoded from base64 using cyberchef, the flag is revealed as KEY{4 2 2 4 1 6 3 7}

### mack2assembly: 
```python
source = open("mackcode.txt", "r")
assembly = open("noreadablemackcode.txt", "a+")

at6 = False
while True:
    line = source.readline()
    count = line.count("MACK")
    if count == 0:
        if at6:
            assembly.write("STACK\n")
            at6 = False
        else:
            assembly.write("EXIT\n")
    elif count == 1:
        if at6:
            assembly.write("INPUT\n")
            at6 = False
        else:
            assembly.write("MACK\n")
    elif count == 2:
        assembly.write("-\n")
    elif count == 3:
        assembly.write("+\n")
    elif count == 4:
        assembly.write("x\n")
    elif count == 5:
        assembly.write("compare\n")
    elif count == 6:
        assembly.write("LOAD\n")
        at6 = True
    elif count == 7:
        assembly.write("STR\n")
    elif count == 8:
        assembly.write("JMP\n")
    elif count == 9:
        assembly.write("CHAR\n")
    else:
        value=count-10
        output = str(value) + "\n"
        assembly.write(output)
    if not line:
        break

source.close()
assembly.close()
```

### mackruntime.py
```python
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
```

