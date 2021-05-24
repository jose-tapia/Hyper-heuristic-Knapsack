import csv
import os
import pandas

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

    csvPath = tapia_path+fileName
    try:
        labels += ['ID']
        if overwrite is False:    
            file = open(csvPath, "r")
            if len(file.readline().split(',')) != len(labels):
                overwrite = True
            file.close()
        instanceNumber = 1
        if overwrite is False:
            df = pandas.read_csv(csvPath)
            if 'ID' in df.columns:
                instanceNumber = max(df['ID'])+1
 
        modeAppend = 'w' if overwrite else 'a'
        with open(csvPath, modeAppend) as f:
            writer = csv.DictWriter(f, fieldnames = labels)
            if os.stat(csvPath).st_size == 0:
                writer.writeheader()
            for elem in trainData:
                elem['ID'] = instanceNumber
                writer.writerow(elem)
    except IOError:
        print("I/O error")    
