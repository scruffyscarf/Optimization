s = list(map(int, input().split()))
c = [list(map(int, input().split())) for i in range(3)]
d = list(map(int, input().split()))



def print_matrix(supply, costs, demand):
    print("       | ", "1  2  3",  " | Supply")
    print("—" * 25)
    for i in range(len(supply)): 
        print(i + 1, "     | ", *costs[i], " | ", supply[i])
    print("—" * 25)
    print("Demand | ", *demand,  " | ")



def north_west(supply, costs, demand):

    supply = supply[:]
    demand = demand[:]
    costs = [row[:] for row in costs]
    north_west_allocation_matrix = [[0] * len(demand) for _ in range(len(supply))]
    north_west_total_cost = 0

    i, j = 0, 0

    while i < len(supply) and j < len(demand):
        quantity = min(supply[i], demand[j])
        north_west_allocation_matrix[i][j] = quantity
        north_west_total_cost += costs[i][j] * quantity

        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0:
            i += 1
        elif demand[j] == 0:
            j += 1

    return north_west_allocation_matrix, north_west_total_cost



def vogel(supply, costs, demand):
    
    supply = supply[:]
    demand = demand[:]
    costs = [row[:] for row in costs]
    vogel_allocation_matrix = [[0] * len(demand) for i in range(len(supply))]
    vogel_total_cost = 0

    while any(supply) and any(demand):

        minimal_values = []

        for i in range(len(supply)):
            if supply[i] > 0:
                line = costs[i][:]
                first_min = min(line)
                line.remove(first_min)
                second_min = min(line) if line else float('inf')
                minimal_values.append((abs(first_min - second_min), i, 'row'))

        for j in range(len(demand)):
            if demand[j] > 0:
                col = [costs[i][j] for i in range(len(supply))]
                first_min = min(col)
                col.remove(first_min)
                second_min = min(col) if col else float('inf')
                minimal_values.append((abs(first_min - second_min), j, 'col'))

        maximal_value, index, direction = max(minimal_values)

        if direction == 'row':
            row_index = index
            col_index = costs[row_index].index(min(costs[row_index]))
        else:
            col_index = index
            row_index = [costs[i][col_index] for i in range(len(supply))].index(min([costs[i][col_index] for i in range(len(supply))]))

        quantity = min(supply[row_index], demand[col_index])
        vogel_allocation_matrix[row_index][col_index] = quantity
        vogel_total_cost += quantity * costs[row_index][col_index]

        supply[row_index] -= quantity
        demand[col_index] -= quantity

        if supply[row_index] == 0:
            for j in range(len(demand)):
                costs[row_index][j] = float('inf')

        if demand[col_index] == 0:
            for i in range(len(supply)):
                costs[i][col_index] = float('inf')

    return vogel_allocation_matrix, vogel_total_cost



def russell(supply, costs, demand):

    supply = supply[:]
    demand = demand[:]
    costs = [row[:] for row in costs]
    russell_allocation_matrix = [[0] * len(demand) for i in range(len(supply))]
    russell_total_cost = 0

    while sum(supply) > 0 and sum(demand) > 0:
        max_supply = [max(costs[i]) if supply[i] > 0 else float('-inf') for i in range(len(supply))]
        max_demand = [max((costs[j][i] for j in range(len(supply)) if demand[i] > 0), default=float('-inf')) for i in range(len(demand))]

        adjusted_costs = [[costs[i][j] - max_supply[i] - max_demand[j] for j in range(len(demand))] for i in range(len(supply))]

        min_value = float('inf')
        row_index, col_index = -1, -1

        for i in range(len(supply)):
            for j in range(len(demand)):
                if supply[i] > 0 and demand[j] > 0 and adjusted_costs[i][j] < min_value:
                    min_value = adjusted_costs[i][j]
                    row_index, col_index = i, j

        quantity = min(supply[row_index], demand[col_index])
        russell_allocation_matrix[row_index][col_index] = quantity
        russell_total_cost += quantity * costs[row_index][col_index]

        supply[row_index] -= quantity
        demand[col_index] -= quantity

        if supply[row_index] == 0:
            for j in range(len(demand)):
                costs[row_index][j] = float('inf')

        if demand[col_index] == 0:
            for i in range(len(supply)):
                costs[i][col_index] = float('inf')

    return russell_allocation_matrix, russell_total_cost



if sum(s) != sum(d):
    print("The problem is not balanced!")
else:
    north_west_allocation_matrix, north_west_total_cost = north_west(s, c, d)
    vogel_allocation_matrix, vogel_total_cost = vogel(s, c, d)
    russell_allocation_matrix, russell_total_cost = russell(s, c, d)

    print()
    print_matrix(s, c, d)


    print("\nFeasible solutions for North-West method:")
    for row in north_west_allocation_matrix:
        print(row)
    print("Total cost for North-West method:", north_west_total_cost)

    print("\nFeasible solutions for Vogel's approximation:")
    for row in vogel_allocation_matrix:
        print(row)
    print("Total cost for Vogel's approximation:", vogel_total_cost)

    print("\nFeasible solutions for Russell's approximation:")
    for row in russell_allocation_matrix:
        print(row)
    print("Total cost for Russell's approximation:", russell_total_cost)
