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
