import csv
import os
from fnmatch import fnmatch
from typing import List
import pandas as pd


# Directory paths
tapia_path = 'C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/'
dany_path =  '/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/'
ramon_path = dany_path

def loadInstance(path):
    # Function to read the instance
    file = open(path, 'r')
    data = file.readlines()
    weights, profits = [], []
    
    for i, line in enumerate(data):
        item = line.split(',')
        if i == 0: n, W = int(item[0]), int(item[1])
        else:
            weights.append(int(item[0]))
            profits.append(float(item[1]))

    return n, W, weights, profits

def saveDictCSV(fileName: str, dictData: dict):
    csvPath = tapia_path+fileName
    df = pd.DataFrame(dictData)
    df.to_csv(csvPath)


def saveDataCSV(fileName: str, trainData: dict, labels: List[str], overwrite = True):
    # Function to save the train dataset for the LSTM model, allowing to overwrite or not the data
    csvPath = tapia_path+fileName
    try:
        labels += ['ID']
        if overwrite is False:    
            file = open(csvPath, 'r')
            if len(file.readline().split(',')) != len(labels):
                overwrite = True
            file.close()
        instanceNumber = 1
        if overwrite is False:
            df = pd.read_csv(csvPath)
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
        print('I/O Error: The CSV file was not able to read or write.')    

def obtainFilenames(dirPath, dataset = 'Pisinger'):
    # Obtain the instance's path for a given dataset
    filesPath = []
    dataset_path = dirPath+'Instances/'+dataset
    for path, _, files in os.walk(dataset_path):
            for name in files:
                if fnmatch(name, '*.kp'):
                    filesPath.append(os.path.join(path, name))
    return filesPath
