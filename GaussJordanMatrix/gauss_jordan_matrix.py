"""Auto-calculates the steps you order."""

n = 3
mt = []

pt = lambda mt, mt2=None : [print(i) for i in mt] if mt2 is None else [print(mt[i],mt2[i],sep = ' | ') for i in range(len(mt))]

def setint(mt: list) -> None:
    for i in range(len(mt)):
        for j in range(len(mt[i])):
            if (mt[i][j]*10)%10 == 0:
                mt[i][j] = int(mt[i][j])
        

id = [[1 if i == j else 0 for i in range(n)] for j in range(n)]

for i in range(n):
    lst = []
    for j in range(n):
        lst.append(int(input(f"Digite el valor A{i+1}{j+1}\n>")))
    mt.append(lst)

pt(mt,id)

pre_mt = []
pre_id = []
cont = 0
f_id = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
while 1:
    ot = input("Operación (1), (2) o (3)?\n>")
    #if ot == 'r' and pre_mt != [] and pre_id != []:
    #    mt = pre_mt[:]
    #    id = pre_id[:]   
    
    if ot == '1':
        pre_mt = mt[:]
        pre_id = id[:]
        a = int(input("Digite la primera fila a intercambiar:\n>"))
        b = int(input("Digite la segunda fila a intercambiar:\n>"))
        if a > 0 and b > 0:
            mt[a-1], mt[b-1] = mt[b-1], mt[a-1]
            id[a-1], id[b-1] = id[b-1], id[a-1]
        else:
            print("\nWrong input.\n")
    elif ot == '2':
        pre_mt = mt[:]
        pre_id = id[:]
        a = int(input("Digite la fila a multiplicar:\n>"))
        b = eval(input("Digite λ:\n>"))
        if a > 0:
            for i in range(len(mt[a-1])):
                mt[a-1][i] *= b
            for i in range(len(id[a-1])):
                id[a-1][i] *= b
        else:
            print("\nWrong input.\n")
    elif ot == '3':
        pre_mt = mt[:]
        pre_id = id[:]
        a = int(input("Digite la primera fila:\n>"))
        b = int(input("Digite la segunda fila:\n>"))
        c = eval(input("Digite λ (f1 + λf2):\n>"))
        if a > 0 and b > 0:
            for i in range(len(mt[a-1])):
                mt[a-1][i] += c*mt[b-1][i]
            for i in range(len(id[a-1])):
                id[a-1][i] += c*id[b-1][i]
    else:
        raise Exception(f"Not expected '{ot}'")
    
    cont += 1
    print()
    setint(mt)
    setint(id)
    pt(mt,id)
    
    if mt == f_id:
        print(f"DONE! in {cont} steps.")
        break

