"""
    Little to no comments, as I worked on this
    very quickly with no intention to make this
    available for public viewing.

    Author: Jacob Bonfanti
"""

from Matrix import Matrix
from Primes import make_primes
import openpyxl as xlsx
import random

def make_commutative(A, m_mode=False):
    if m_mode == False:
        n = float(random.randint(2, 7))
        A[0,0] = n
        A[1,1] = n
        A[1,0] = 0
        A[0,1] = 0
    elif m_mode == 'c':
        primes = make_primes(1000)
        n, m = int(random.randint(100, 999)), int(random.randint(100, 999))
        A[0,0] = primes[n]-1
        A[0,1] = primes[m]-1
        A[1,0] = -(primes[m]-1)
        A[1,1] = primes[n]-1
    elif m_mode == 'cn':
        primes = make_primes(1000)
        n, m = int(random.randint(100, 999)), int(random.randint(100, 999))
        A[0,0] = primes[n]
        A[0,1] = primes[m]
        A[1,0] = -(primes[m])
        A[1,1] = primes[n]
    return A

def randomize(A):
    for i in range(A.m):
        for j in range(A.n):
            A[i,j] = float(random.randint(2, 7))
    return A

def multiply_cells(A, B, c0, c1):
    written_formula = [[None, None], [None, None]]
    written_formula[0][0] = A[0][0]+'*'+B[0][0]+'+'+A[0][1]+'*'+B[1][0]
    written_formula[0][1] = A[0][0]+'*'+B[0][1]+'+'+A[0][1]+'*'+B[1][1]
    written_formula[1][0] = A[1][0]+'*'+B[0][0]+'+'+A[1][1]+'*'+B[1][0]
    written_formula[1][1] = A[1][0]+'*'+B[0][1]+'+'+A[1][1]+'*'+B[1][1]
    if c0 != 1:
        written_formula[0][0] = str(c0)+"*("+written_formula[0][0]+")"
        written_formula[0][1] = str(c0)+"*("+written_formula[0][1]+")"
        written_formula[1][0] = str(c0)+"*("+written_formula[1][0]+")"
        written_formula[1][1] = str(c0)+"*("+written_formula[1][1]+")"
    if c1 != 1:
        written_formula[0][0] = str(c1)+"*("+written_formula[0][0]+")"
        written_formula[0][1] = str(c1)+"*("+written_formula[0][1]+")"
        written_formula[1][0] = str(c1)+"*("+written_formula[1][0]+")"
        written_formula[1][1] = str(c1)+"*("+written_formula[1][1]+")"
    return written_formula

def add_cells(A, B, c0, c1):
    written_formula = [[None, None], [None, None]]
    written_formula[0][0] = A[0][0]+'+'+B[0][0]
    written_formula[0][1] = A[0][1]+'+'+B[0][1]
    written_formula[1][0] = A[1][0]+'+'+B[1][0]
    written_formula[1][1] = A[1][1]+'+'+B[1][1]
    if c0 != 1:
        written_formula[0][0] = str(c0)+"*"+written_formula[0][0]
        written_formula[0][1] = str(c0)+"*"+written_formula[0][1]
        written_formula[1][0] = str(c0)+"*"+written_formula[1][0]
        written_formula[1][1] = str(c0)+"*"+written_formula[1][1]
    if c1 != 1:
        written_formula[0][0] = written_formula[0][0]+"*"+str(c1)
        written_formula[0][1] = written_formula[0][1]+"*"+str(c1)
        written_formula[1][0] = written_formula[1][0]+"*"+str(c1)
        written_formula[1][1] = written_formula[1][1]+"*"+str(c1)
    return written_formula

def operate_matricies(A, B, operator, C, index, cells, sheet, mode, c0=1, c1=1):
    if operator == '*':
        form = multiply_cells(cells[A], cells[B], c0, c1)
    elif operator == '+':
        form = add_cells(cells[A], cells[B], c0, c1)
    col, row = index
    if col-1 > ord('Z'):
        sheet['A'+chr(col-1-26)+str(row)] = C+'='
    else:
        sheet[chr(col-1)+str(row)] = C+'='
        
    Ccell = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            if mode == 'c' or mode=='cn':
                if col+j > ord('Z'):
                    sheet['A'+chr(col+j-26)+str(row+i)] = "="+form[i][j]
                    Ccell[i][j] = 'A'+chr(col+j-26)+str(row+i)
                else:
                    sheet[chr(col+j)+str(row+i)] = "="+form[i][j]
                    Ccell[i][j] = chr(col+j)+str(row+i)
            elif mode == 'n':
                sheet[chr(col+j)+str(row+i)] = "=MOD("+form[i][j]+",B1)"
                Ccell[i][j] = chr(col+j)+str(row+i)
    cells[C] = Ccell
    #print "C=", C

def scalar_multiply(c0, A, C, index, cells, sheet):
    col, row = index
    A = cells[A]
    sheet[chr(col-1)+str(row)] = C+'='
    Ccell = [[None, None], [None, None]]
    for i in range(2):
        for j in range(2):
            sheet[chr(col+j)+str(row+i)] = "="+str(c0)+"*"+A[i][j]
            Ccell[i][j] = chr(col+j)+str(row+i)
    cells[C] = Ccell

def make_sheet(sheet, mode):
    A = Matrix(2,2)
    B = Matrix(2,2)
    C = Matrix(2,2)
    D = Matrix(2,2)
    R = Matrix(2,2)
    n = None
    if mode=='n':
        A = randomize(A)
        B = randomize(B)
        C = randomize(C)
        D = randomize(D)
        R = randomize(R)
        minimum = A[0,0]*B[0,0]*C[0,0]*D[0,0]
        n = float(random.randint(minimum+2, 2*minimum))
        A[0,1] = n
        B[0,1] = n
        C[0,1] = n
        D[0,1] = n
        R[0,0] = n+1
        R[0,1] = n
        
    elif mode=='c' or mode=='cn':
        A = make_commutative(A)
        B = make_commutative(B)
        C = make_commutative(C)
        D = make_commutative(D)
        R = make_commutative(R, m_mode=mode)

    Acells = [['B3', 'C3'], ['B4', 'C4']]
    Bcells = [['B6', 'C6'], ['B7', 'C7']]
    Ccells = [['B9', 'C9'], ['B10', 'C10']]
    Dcells = [['B12', 'C12'], ['B13', 'C13']]
    Rcells = [['B15', 'C15'], ['B16', 'C16']]
    IRcells = [['B18', 'C18'], ['B19', 'C19']]

    cells = {'A': Acells,
             'B': Bcells,
             'C': Ccells,
             'D': Dcells,
             'R': Rcells,
             'IR': IRcells}
    

    sheet['A3'] = "A ="
    sheet['A6'] = "B ="
    sheet['A9'] = "C ="
    sheet['A12'] = "D ="
    sheet['A15'] = "R ="
    sheet['A18'] = "R^-1 ="

    col = 66
    row = 3

    matricies = [A, B, C, D, R]

    for i in range(5):
        matrix = matricies[i]
        for j in range(2):
            for k in range(2):
                sheet[chr(col+k)+str(row+j)] = matrix[j, k]
        row+=3

    sheet['B18'] = "=C16/(B15*C16-B16*C15)"
    sheet['C19'] = "=B15/(B15*C16-B16*C15)"
    sheet['C18'] = "=-C15/(B15*C16-B16*C15)"
    sheet['B19'] = "=-B16/(B15*C16-B16*C15)"
    
    if mode=='n':
        sheet['A1'] = "n ="
        sheet['B1'] = n
        row = 3
        for i in range(4):
            sheet[chr(col+1)+str(row)] = "=B1"
            row+=3
        sheet['B15'] = "=B1+1"
        sheet['C15'] = "=B1"

    operate_matricies("R", "A", '*', "A'", (70, 3), cells, sheet, 'c')
    operate_matricies("R", "B", '*', "B'", (70, 6), cells, sheet, 'c')
    operate_matricies("R", "C", '*', "C'", (70, 9), cells, sheet, 'c')
    operate_matricies("R", "D", '*', "D'", (70, 12), cells, sheet, 'c')

    operate_matricies("IR", "A'", '*', "IRA'", (74, 3), cells, sheet, mode)
    operate_matricies("IR", "B'", '*', "IRB'", (74, 6), cells, sheet, mode)
    operate_matricies("IR", "C'", '*', "IRC'", (74, 9), cells, sheet, mode)
    operate_matricies("IR", "D'", '*', "IRD'", (74, 12), cells, sheet, mode)

    

    matricies = ["A'", "B'", "C'", "D'"]

    i, j, k, l = random.randint(0, 3), random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)
    while i == j:
        j = random.randint(0, 3)
    while i == k or j == k:
        k = random.randint(0, 3)
    while i == l or j == l or k == l:
        l = random.randint(0, 3)

    i = matricies[i]
    j = matricies[j]
    k = matricies[k]
    l = matricies[l]

    operate_matricies(i, j, '+', i+"+"+j, (70, 15), cells, sheet, 'c')
    operate_matricies(k, l, '+', k+"+"+l, (70, 18), cells, sheet, 'c')
    operate_matricies(j, k, '*', j+"*"+k, (70, 21), cells, sheet, 'c')
    operate_matricies(k, j, '*', k+"*"+j, (70, 24), cells, sheet, 'c')
    operate_matricies(i, l, '*', i+"*"+l, (70, 27), cells, sheet, 'c')
    operate_matricies(l, i, '*', l+"*"+i, (70, 30), cells, sheet, 'c')
    operate_matricies(k, k, '+', k+"+"+k, (70, 33), cells, sheet, 'c')

    operate_matricies('IR', i+"+"+j, '*', "IR("+i+"+"+j+")", (74, 15), cells, sheet, mode)
    operate_matricies('IR', k+"+"+l, '*', "IR("+k+"+"+l+")", (74, 18), cells, sheet, mode)
    operate_matricies('IR', j+"*"+k, '*', "IR("+j+"*"+k+")", (74, 21), cells, sheet, mode)
    operate_matricies('IR', k+"*"+j, '*', "IR("+k+"*"+j+")", (74, 24), cells, sheet, mode)
    operate_matricies('IR', i+"*"+l, '*', "IR("+i+"*"+l+")", (74, 27), cells, sheet, mode)
    operate_matricies('IR', l+"*"+i, '*', "IR("+l+"*"+i+")", (74, 30), cells, sheet, mode)
    operate_matricies('IR', k+"+"+k, '*', "IR("+k+"+"+k+")", (74, 33), cells, sheet, mode)

    if mode == 'c' or mode=='cn':
        operate_matricies('IR', "IR("+j+"*"+k+")", '*', "IRIR("+j+"*"+k+")", (74, 36), cells, sheet, mode)
        operate_matricies('IR', "IR("+k+"*"+j+")", '*', "IRIR("+k+"*"+j+")", (74, 39), cells, sheet, mode)
        operate_matricies('IR', "IR("+i+"*"+l+")", '*', "IRIR("+i+"*"+l+")", (74, 42), cells, sheet, mode)
        operate_matricies('IR', "IR("+l+"*"+i+")", '*', "IRIR("+l+"*"+i+")", (74, 45), cells, sheet, mode)

    to_reverse = []

    rn = random.randint(2, 9)
    scalar_multiply(rn, i, str(rn)+i, (78, 3), cells, sheet)
    to_reverse.append(str(rn)+i)
    rn = random.randint(2, 9)
    scalar_multiply(1.0/float(rn), j, j+'/'+str(rn), (78, 6), cells, sheet)
    to_reverse.append(j+'/'+str(rn))
    rn = random.randint(2, 9)
    scalar_multiply(rn, j+"*"+k, str(rn)+"("+j+"*"+k+")", (78, 9), cells, sheet)
    to_reverse.append(str(rn)+"("+j+"*"+k+")")
    rn = random.randint(2, 9)
    scalar_multiply(1.0/float(rn), i+"*"+l, "("+i+"*"+l+")/"+str(rn), (78, 12), cells, sheet)
    to_reverse.append("("+i+"*"+l+")/"+str(rn))
    r = 15

    keys = cells.keys()
    reverse_even_more = []
    for p in range(7):
        rn1 = 0
        rn2 = 0
        while rn2==rn1 or '('+keys[rn1]+')'+'*'+'('+keys[rn2]+')' in keys or "IR" in keys[rn1] or "IR" in keys[rn2] or "'" not in keys[rn1] or "'" not in keys[rn2]:
            rn1 = random.randint(0, len(keys)-1)
            rn2 = random.randint(0, len(keys)-1)
        operate_matricies(keys[rn1], keys[rn2], '*', '('+keys[rn1]+')'+'*'+'('+keys[rn2]+')', (78, r), cells, sheet, 'c')
        string = '('+keys[rn1]+')'+'*'+'('+keys[rn2]+')'
        to_reverse.append(string)
        if (mode=='c' or mode=='cn') and string.count('*') > 0:
            reverse_even_more.append(('IR('+string+')', r))
        r += 3

    reverse_again = []
    r = 3
    for key in to_reverse:
        operate_matricies('IR', key, '*', "IR("+key+")", (82, r), cells, sheet, mode)
        if key.count('*'):
            reverse_again.append((key, r))
        r+=3
    if mode=='c' or mode=='cn':
        for key, r in reverse_again:
            operate_matricies('IR', 'IR('+key+')', '*', 'IRIR('+key+')', (86, r), cells, sheet, mode)
    if mode == 'c' or mode=='cn':
        blah = ''
        numofstars = 0
        c = 82
        while len(reverse_even_more) > 0:
            numofstars += 1
            print numofstars
            c+=4
            r_copy = list(reverse_even_more)
            for key_pair in r_copy:
                key, row = key_pair
                print key
                operate_matricies('IR', key, '*', "IR"+key, (c, row), cells, sheet, mode)
                string = 'IR'+key
                r+=3
                reverse_even_more.remove((key, row))
                if key.count('*') > numofstars:
                    reverse_even_more.append((string, row))
    return cells

wb = xlsx.Workbook()
sheet = wb.get_sheet_by_name('Sheet')
cells=None
for i in range(20):
    print wb.get_sheet_names()
    if i < 10:
        mode = 'cn'
    else:
        mode = 'c'
    #try:
    cells = make_sheet(sheet, mode)
    #except:
        #wb.save('Santa_2.xlsx')
        #sys.exit(1)
    if i != 19:
        wb.create_sheet()
        sheet = wb.get_sheet_by_name('Sheet'+str(i+1))
wb.save('Matrix_Data.xlsx')
