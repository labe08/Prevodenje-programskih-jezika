import sys

tree = "<program>\n <lista_naredbi>"
current = 0

def next_or_end(lines):
    global current
    if current == len(lines)-1:
        return
    else: current += 1

def tweek_tree(depth):
    global tree
    tree += "\n"
    for i in range (depth):
        tree += " "

def setup(depth):
    global tree
    tweek_tree(depth)
    tree += lines[current]

def obradi_P(lines, depth):
    global tree
    global current
    if lines[current].startswith("OP_PLUS"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<P>"
        obradi_P(lines, depth+1)
    elif lines[current].startswith("OP_MINUS"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<P>"
        obradi_P(lines, depth+1)
    elif lines[current].startswith("L_ZAGRADA"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<E>"
        obradi_E(lines, depth+1)
        if lines[current].startswith("D_ZAGRADA"):
            setup(depth)
            next_or_end(lines)
        elif lines[current] == "kraj":
            print("err kraj")
            raise SystemExit()   
        else:
            print("err " + lines[current]) 
            raise SystemExit() 
    elif lines[current].startswith("IDN"):
        setup(depth)
        next_or_end(lines)
    elif lines[current].startswith("BROJ"):
        setup(depth)
        next_or_end(lines)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    return

def t_lista(lines, depth):
    global tree
    global current
    if lines[current].startswith("OP_PUTA"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<T>"
        obradi_T(lines, depth+1)
    elif lines[current].startswith("OP_DIJELI"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<T>"
        obradi_T(lines, depth+1)
    else:
        tweek_tree(depth)
        tree += "$"
    return

def e_lista(lines, depth):
    global tree
    global current
    if lines[current].startswith("OP_PLUS"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<E>"
        obradi_E(lines, depth+1)
    elif lines[current].startswith("OP_MINUS"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<E>"
        obradi_E(lines, depth+1)
    else:
        tweek_tree(depth)
        tree += "$"
    return

def obradi_T(lines, depth):
    global tree
    global current
    tweek_tree(depth)
    tree += "<P>"
    obradi_P(lines, depth+1)
    tweek_tree(depth)
    tree += "<T_lista>"
    t_lista(lines, depth+1)
    return

def obradi_E(lines, depth):
    global tree
    global current
    tweek_tree(depth)
    tree += "<T>"
    obradi_T(lines, depth+1)
    tweek_tree(depth)
    tree += "<E_lista>"
    e_lista(lines, depth+1)
    return

def naredba_pridruzivanja(lines, depth):
    global tree
    global current
    setup(depth)
    next_or_end(lines)
    if lines[current].startswith("OP_PRIDRUZI"):
        setup(depth)
        next_or_end(lines)
        tweek_tree(depth)
        tree += "<E>"
        obradi_E(lines, depth+1)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    return

def za_petlja(lines, depth):
    global tree
    global current
    setup(depth)
    next_or_end(lines)
    if lines[current].startswith("IDN"):
        setup(depth)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    next_or_end(lines)
    if lines[current].startswith("KR_OD"):
        setup(depth)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    next_or_end(lines)
    tweek_tree(depth)
    tree += "<E>"
    obradi_E(lines, depth+1)
    if lines[current].startswith("KR_DO"):
        setup(depth)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    next_or_end(lines) 
    tweek_tree(depth)
    tree += "<E>"
    obradi_E(lines, depth+1)
    tweek_tree(depth)
    tree += "<lista_naredbi>"
    lista_naredbi(lines, depth+1)
    if lines[current].startswith("KR_AZ"):
        setup(depth)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit()  
    next_or_end(lines)
    return

def naredba(lines, depth):
    global tree
    global current
    if lines[current].startswith("IDN"):
        tweek_tree(depth)
        tree += "<naredba_pridruzivanja>"
        naredba_pridruzivanja(lines, depth+1)
    elif lines[current].startswith("KR_ZA"):
        tweek_tree(depth)
        tree += "<za_petlja>"
        za_petlja(lines, depth+1)
    elif lines[current] == "kraj":
        print("err kraj")
        raise SystemExit()   
    else:
        print("err " + lines[current]) 
        raise SystemExit() 
    return

def lista_naredbi(lines, depth):
    global tree
    global current
    tweek_tree(depth)
    if lines[current].startswith("IDN") or lines[current].startswith("KR_ZA"):
        tree += "<naredba>"
        naredba(lines, depth+1)
        tweek_tree(depth)
        tree += "<lista_naredbi>"
        lista_naredbi(lines, depth+1)
    elif lines[current].startswith("OP_"):
        print("err " + lines[current]) 
        raise SystemExit() 
    else:
        tree += "$"
    return

lines = []
for line in sys.stdin:
    lines.append(line.strip())
lines.append("kraj")
depth = 2
lista_naredbi(lines, depth)
print(tree)