def load_data(path):
    file = open(path, "r")
    data = file.readlines()
    values_set = []
    weight_set = []

    for i, line in enumerate(data):
        items = line.split(',')
        if i == 0: numItems, knapsackCap = int(items[0]), int(items[1])  #Number of items, Knapsack capacity
        else:
            weight_set.append(int(items[0])) # For each bin: weight, profit
            values_set.append(float(items[1]))

    return knapsackCap, numItems, values_set, weight_set