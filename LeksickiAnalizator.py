import sys

def spliting_parts_nums(w, idx):
    for n in w:
        if (not n.isnumeric()):
            check_word(w[0:w.index(n)], idx)
            check_word(w[w.index(n):], idx)
            break

def spliting_parts_letters(w, idx):
    for n in w:
        if (not n.isalnum()):
            check_word(w[0:w.index(n)], idx)
            check_word(w[w.index(n):], idx)
            break

def number(w, idx):
    if (w.isnumeric()):
        print('BROJ ' + str(idx) + ' ' + w)
    else:
        spliting_parts_nums(w, idx)

def operator(w, idx):
    for o in w:
        if (o == '='):
            print('OP_PRIDRUZI ' + str(idx) + ' ' + o)
        elif (o == '+'):
            print('OP_PLUS ' + str(idx) + ' ' + o)
        elif (o == '-'):
            print('OP_MINUS ' + str(idx) + ' ' + o)  
        elif (o == '*'):
            print('OP_PUTA ' + str(idx) + ' ' + o)  
        elif (o == '/'):
            print('OP_DIJELI ' + str(idx) + ' ' + o)
        elif (o == '('):
            print('L_ZAGRADA ' + str(idx) + ' ' + o)  
        elif (o == ')'):
            print('D_ZAGRADA ' + str(idx) + ' ' + o)
        else:
            check_word(w[w.index(o):], idx)
            break    

def letter(w, idx):
    if (w == 'za'):
        print('KR_ZA ' + str(idx) + ' ' + w)
    elif (w == 'az'):
        print('KR_AZ ' + str(idx) + ' ' + w)
    elif (w == 'od'):
        print('KR_OD ' + str(idx) + ' ' + w)
    elif (w == 'do'):
        print('KR_DO ' + str(idx) + ' ' + w)
    elif (w.isalnum()):
        print('IDN ' + str(idx) + ' ' + w)
    else:
        spliting_parts_letters(w, idx)
        

def check_word(w, idx):
    if (w != ' '):
        if (w[0].isnumeric()):
            number(w, idx)
        elif ((w[0] >= 'A' and w[0] <= 'Z') or (w[0] >= 'a' and w[0] <= 'z')):
            letter(w, idx)
        else:
            operator(w, idx)


def spliting_words(line, idx):
    words = line.split(' ')
    for w in words:
        if (w.startswith('//') or w == '//'):
            words = words[:words.index(w)]
            break
        check_word(w, idx)


lines = []
for line in sys.stdin:
    lines.append(line.strip())
idx = 1
for line in lines:
    line = " ".join(line.split())
    if (line != ""):
        spliting_words(line, idx)
    idx += 1



