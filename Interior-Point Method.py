def Transpose(B):
    return [[B[j][i] for j in range(len(B))] for i in range(len(B[0]))]

def Inverse(B):
    n = len(B)
    I = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
    A = [B[i] + I[i] for i in range(n)]

    for i in range(n):
        pivot = A[i][i]
        if pivot == 0:
            print("The method is not applicable!")
            return None
        for j in range(n * 2):
            A[i][j] /= pivot
        
        for k in range(i + 1, n):
            factor = A[k][i]
            for j in range(n * 2):
                A[k][j] -= factor * A[i][j]
    
    for i in range(n - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            factor = A[j][i]
            for k in range(n * 2):
                A[j][k] -= factor * A[i][k]
    
    return [i[n:] for i in A]



def interiorPoint(c, A, initial_points, eps, alpha):
    m = len(A)
    c = c + [0] * m
    n = len(c)
    solution = [0] * n
    value = 0

    for i in range(m):
        A[i] = A[i] + [0] * m
        A[i][i + n - m] = 1

    A_x = [[0] * n for i in range(m)]

    for l in range(1, 6):
        ip = initial_points
        D = [[ip[i] if j == i else 0 for j in range(n)] for i in range(n)]

        for i in range(m):
            for j in range(n):
                sum = 0
                for k in range(n):
                    sum += A[i][k] * D[k][j]
                A_x[i][j] = sum
        c_x = [0] * n

        for i in range(n):
            sum = 0
            for j in range(n):
                sum += D[i][j] * c[j]
            c_x[i] = sum

        A_x_T = Transpose(A_x)
        A_x_A_x_T = [[0] * m for i in range(m)]

        for i in range(m):
            for j in range(m):
                sum = 0
                for k in range(n):
                    sum += A_x[i][k] * A_x_T[k][j]
                A_x_A_x_T[i][j] = sum

        A_x_A_x_T_inv = Inverse(A_x_A_x_T)

        if (A_x_A_x_T_inv == None):
            return None, None

        sub = [[0] * n for i in range(n)]
        sub1 = [[0] * m for i in range(n)]

        for i in range(n):
            for j in range(m):
                sum = 0
                for k in range(m):
                    sum += A_x_T[i][k] * A_x_A_x_T_inv[k][j]
                sub1[i][j] = sum

        for i in range(n):
            for j in range(n):
                sum = 0
                for k in range(m):
                    sum += sub1[i][k] * A_x[k][j]
                sub[i][j] = sum

        I = [[1 if j == i else 0 for j in range(n)] for i in range(n)]
        p = [[0] * n for i in range(n)]

        for i in range(n):
            for j in range(n):
                p[i][j] = I[i][j] - sub[i][j]

        c_p = [0] * n

        for i in range(n):
            sum = 0
            for j in range(n):
                sum += p[i][j] * c_x[j]
            c_p[i] = sum
        
        v = -1

        for i in range(n):
            if c_p[i] < 0 and abs(c_p[i]) > v:
                v = abs(c_p[i])

        I = [1] * n
        x_x = [0] * n
        
        for i in range(n):
            x_x[i] = I[i] + alpha / v * c_p[i]

        x = [0] * n

        for i in range(n):
            sum = 0
            for j in range(n):
                sum += D[i][j] * x_x[j]
            x[i] = sum

        initial_points = x

    for i in range(n):
        value += c[i] * initial_points[i]
        solution[i] = round(initial_points[i], eps)
    return solution, round(value, eps)


def simplex(c, A, b, eps, goal):
    n = len(c)
    m = len(A)
    table = []
    solution = [0] * (n + m)
    if (goal == "max"):
        for i in range(m):
            table.append(A[i] + [0] * m + [b[i]])
            table[i][n + i] = 1
        table.append([-i for i in c] + [0] * m + [0])
        pivots = []
        while True:
            if all(i >= 0 for i in table[-1][:n + m]):
                break
            minIndexCol = 0
            minCol = 10**8
            for i in range(n + m):
                if (table[-1][i] < 0 and table[-1][i] < minCol):
                    minCol = table[-1][i]
                    minIndexCol = i
            if (minCol == 10**8):
                print("The method is not applicable!")
                return None, None
            ratios = []
            for i in range(m):
                if table[i][minIndexCol] > 0:
                    ratios.append(table[i][-1] / table[i][minIndexCol])
                else:
                    ratios.append(10**8)
            if all(i == 10**8 for i in ratios):
                print("The method is not applicable!")
                return None, None
            minIndexRow = ratios.index(min(ratios))
            pivots.append([minIndexRow, minIndexCol])
            pivot = table[minIndexRow][minIndexCol]
            table[minIndexRow] = [i / pivot for i in table[minIndexRow]]
            for i in range(len(table)):
                if i != minIndexRow:
                    factor = table[i][minIndexCol]
                    table[i] = [table[i][j] - factor * table[minIndexRow][j] for j in range(len(table[0]))]
            for i in range(len(pivots)):
                if (table[pivots[i][0]][pivots[i][1]] == 1):
                    solution[pivots[i][1]] = round(table[pivots[i][0]][-1], eps)
                else:
                    solution[pivots[i][1]] = 0
        return solution[:n], table[-1][-1]
    if (goal == "min"):
        for i in range(m):
            table.append(A[i] + [0] * m + [b[i]])
            table[i][n + i] = 1
        table.append([-i for i in c] + [0] * m + [0])
        pivots = []
        while True:
            if all(i <= 0 for i in table[-1][:n + m]):
                break
            minIndexCol = 0
            minCol = -10**8
            for i in range(n + m):
                if (table[-1][i] > 0 and table[-1][i] > minCol):
                    minCol = table[-1][i]
                    minIndexCol = i
            if (minCol == -10**8):
                print("The method is not applicable!")
                return None, None
            ratios = []
            for i in range(m):
                if table[i][minIndexCol] > 0:
                    ratios.append(table[i][-1] / table[i][minIndexCol])
                else:
                    ratios.append(10**8)
            if all(i == 10**8 for i in ratios):
                print("The method is not applicable!")
                return None, None
            minIndexRow = ratios.index(min(ratios))
            pivots.append([minIndexRow, minIndexCol])
            pivot = table[minIndexRow][minIndexCol]
            table[minIndexRow] = [i / pivot for i in table[minIndexRow]]
            for i in range(len(table)):
                if i != minIndexRow:
                    factor = table[i][minIndexCol]
                    table[i] = [table[i][j] - factor * table[minIndexRow][j] for j in range(len(table[0]))]
            for i in range(len(pivots)):
                if (table[pivots[i][0]][pivots[i][1]] == 1):
                    solution[pivots[i][1]] = round(table[pivots[i][0]][-1], eps)
                else:
                    solution[pivots[i][1]] = 0
        return solution[:n], table[-1][-1]
            

c = []
A = []
b = []
initial_points = []

number = int(input())

for i in range(number):
    c.append(float(input()))

contraints = int(input())

for i in range(contraints):
    A.append([])
    for j in range(number):
        A[i].append(float(input()))
   
for i in range(contraints):
    b.append(float(input()))

for i in range(number + contraints):
    initial_points.append(float(input()))

eps = int(input())
goal = input()

alpha1 = 0.5
alpha2 = 0.9

solution, value = simplex(c, A, b, eps, goal)
if (solution != None and value != None):
    print("Solution by Simplex Method: ", solution)
    print("Value by Simplex Method: ", value)

print("Solutions by Interior Point Method:")
solition_interior1, value1 = interiorPoint(c, A, initial_points, eps, alpha1)
if (solition_interior1 != None):
    print("Solution with alpha = ", alpha1, ":", solition_interior1)
    print("Value with alpha = ", alpha1, ":", value1)

solition_interior2, value2 = interiorPoint(c, A, initial_points, eps, alpha2)
if (solition_interior2 != None):
    print("Solution with alpha =", alpha2, ":", solition_interior2)
    print("Value with alpha =", alpha2, ":", value2)