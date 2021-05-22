import csv
import os

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

def saveDataCSV(fileName, trainData: dict, labels: [str], overwrite = True):
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/"
    ramon_path = dany_path 
    try:
        if overwrite is False:    
            file = open(tapia_path+fileName, "r")
            if len(file.readline().split(',')) != len(labels):
                overwrite = True

        modeAppend = 'w' if overwrite else 'a'
        with open(tapia_path+fileName, modeAppend) as f:
            writer = csv.DictWriter(f, fieldnames = labels)
            if os.stat(tapia_path+fileName).st_size == 0:
                writer.writeheader()
            for elem in trainData:
                writer.writerow(elem)
    except IOError:
        print("I/O error")    
