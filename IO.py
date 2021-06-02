import csv
import os
from typing import List
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

def saveDictCSV(fileName: str, dictData: dict):
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/"
    ramon_path = dany_path 

    csvPath = tapia_path+fileName
    df = pandas.DataFrame(dictData)
    df.to_csv(csvPath)


def saveDataCSV(fileName: str, trainData: dict, labels: List[str], overwrite = True):
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

def obtainFilenames(dirPath, dataset = 'Pisinger', qty = 1, shift = 0):
    if dataset == 'Pisinger':
        return [dirPath+"Instances/Pisinger/pisinger_"+str(i)+".kp" for i in range(31)]
    elif dataset == 'OrtizBayliss':
        return [dirPath+"Instances/OrtizBayliss/ortizbayliss_"+str(i)+"_"+str(j)+".kp" for i in range(1, 5) for j in range(25)]
    elif dataset == 'Martello':
        return [dirPath+"Instances/Martello/martello_"+str(i)+"_"+str(j)+".kp" for i in range(1, 15) for j in range(50)]
    elif dataset == 'MiniMartello':
        return [dirPath+"Instances/Martello/martello_"+str(i)+"_"+str(j+10*k+shift)+".kp" for i in list(range(1, 10))+list(range(13, 15)) for j in range(qty) for k in range(3)]
    else:
        return []

def obtainDirectory(dirPath):
    return list(map(lambda filename: dirPath+filename, os.listdir(dirPath)))
