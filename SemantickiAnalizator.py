import sys

current = 0

def is_same_line(first, second):
    return first == second


def read_kr_do(lines, za_idns, idns):
    global current
    while current <= len(lines)-2:
        if (lines[current].startswith('IDN') and lines[current+1].startswith('OP_PRIDRUZI')) or lines[current].startswith('KR_ZA') or lines[current].startswith('KR_AZ'):
            break
        name, line, sign = lines[current].split(" ")
        if name == 'IDN':
            if sign in za_idns:
                print("err " + str(line) + " " + str(sign))
                raise SystemExit()
            elif sign in idns:
                print(line, idns[sign], sign)
            else: 
                print("err " + str(line) + " " + str(sign))
                raise SystemExit() 
        current += 1
    return

def read_kr_od(lines, za_idns, idns):
    global current
    while current <= len(lines)-2 and not lines[current].startswith('KR_DO'):
        name, line, sign = lines[current].split(" ")
        if name == 'IDN':
            if sign in za_idns:
                print("err " + str(line) + " " + str(sign))
                raise SystemExit()
            elif sign in idns:
                print(line, idns[sign], sign)
            else: 
                print("err " + str(line) + " " + str(sign))
                raise SystemExit() 
        current += 1
    return

def za_loop(idns, lines, other, other_line, other_sign):
    global current
    za_idns = {}
    if other == 'IDN':
        za_idns[other_sign] = other_line
    current += 1
    while current <= len(lines)-2:
        name, line, sign = lines[current].split(" ")
        name2, line2, sign2 = lines[current+1].split(" ")
        if name == 'KR_AZ':
            break            
        elif name == 'IDN' and name2 == 'OP_PRIDRUZI':
            if not sign in za_idns.keys() and not sign in idns.keys():
                za_idns[sign] = line
        elif name == 'KR_OD':
            current += 1
            read_kr_od(lines, za_idns, idns)
            current -= 1
        elif name == 'KR_DO':
            current += 1
            read_kr_do(lines, za_idns, idns)
            current -= 1 
        elif (name.startswith('OP_') and name2 == 'IDN') or (name.startswith('L_') and name2 == 'IDN'):
            if sign2 in za_idns:
                if not is_same_line(line2, za_idns[sign2]):
                    print(line2, za_idns[sign2], sign2)
                else: 
                    print("err " + str(line2) + " " + str(sign2))
                    raise SystemExit()
            elif sign2 in idns:
                if not is_same_line(line2, idns[sign2]):
                    print(line2, idns[sign2], sign2)
                else: 
                    print("err " + str(line2) + " " + str(sign2))
                    raise SystemExit()
            else: 
                print("err " + str(line2) + " " + str(sign2))
                raise SystemExit()
        elif name == 'KR_ZA':
            new_idns = {**idns, **za_idns}
            za_loop(new_idns, lines, name2, line2, sign2)
        current += 1
    return

lines = []
for line in sys.stdin:
    line = line.strip()
    if not line.startswith("<") and line != '$':
        lines.append(line)
idns = {}

while current <= len(lines)-2:
    name, line, sign = lines[current].split(" ")
    name2, line2, sign2 = lines[current+1].split(" ")
    if name == 'IDN' and name2 == 'OP_PRIDRUZI':
        if not sign in idns.keys():
            idns[sign] = line  
    elif (name.startswith('OP_') and name2 == 'IDN') or (name.startswith('L_') and name2 == 'IDN'):
        if sign2 in idns:
            if not is_same_line(line2, idns[sign2]):
                print(line2, idns[sign2], sign2)
            else:
                print("err " + str(line2) + " " + str(sign2))
                raise SystemExit()
        else: 
            print("err " + str(line2) + " " + str(sign2))
            raise SystemExit()
    elif name == 'KR_ZA':
        za_loop(idns, lines, name2, line2, sign2)
    current += 1
