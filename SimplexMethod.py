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

        return solution[:n], table[-1][-1]
            

c = []
A = []
b = []

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

eps = int(input())
goal = input()

solution, value = simplex(c, A, b, eps, goal)
if (solution != None and value != None):
    print(solution)
    print(value)
