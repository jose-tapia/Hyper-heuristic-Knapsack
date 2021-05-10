import os 
import math 
def pisingerFormat(oldVersion, newVersion, printLastLine):
    fileOld = open(oldVersion, "r")
    fileNew = open(newVersion, "w")
    data = fileOld.readlines()

    for i, line in enumerate(data):
        items = line.split(' ')
        if i+1 < len(data) or printLastLine:
            if i == 0:
                fileNew.write(f'{items[0]}, {items[1]}')
            else: 
                v = math.ceil(float(items[0]))
                w = math.ceil(float(items[1]))
                if w == 0:
                    w += 1
                if v == 0:
                    v += 1
                fileNew.write(f'{int(w)}, {int(v)}\n')

def changeFileNames():
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/OrtizBayliss"
    types = ["DEFAULT", "MAXPROFIT", "MAXPROFITWEIGHT", "MINWEIGHT"]
    for typeFile, idType in zip(types, range(len(types))):
        for idCase in range(25):
            oldFileName = tapia_path+"/GA-"+typeFile+"_20_"+str(idCase).zfill(3)+".kp"        
            newFileName = tapia_path+"/ortizbayliss_"+str(idType+1)+"_"+str(idCase)+".kp"
            os.rename(oldFileName, newFileName)

def addFormatAndName():
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/Pisinger"
    sizesForInstances = ["100", "200", "500", "1000", "2000", "5000", "10000"]
    currentFile = 0
    for typeFile in range(1,4):
        for sizeInstance in sizesForInstances:
            oldVersion = tapia_path+"/large_scale/knapPI_"+str(typeFile)+"_"+sizeInstance+"_1000_1"
            newVersion = tapia_path+"/pisinger_"+str(currentFile)+".kp"
            currentFile += 1
            pisingerFormat(oldVersion, newVersion, False)

    low_dimensional_files = ["f1_l-d_kp_10_269", "f2_l-d_kp_20_878", "f3_l-d_kp_4_20", "f4_l-d_kp_4_11", 
                            "f5_l-d_kp_15_375", "f6_l-d_kp_10_60", "f7_l-d_kp_7_50", "f8_l-d_kp_23_10000", 
                            "f9_l-d_kp_5_80", "f10_l-d_kp_20_879"]
    for oldSuffix in low_dimensional_files:
        oldVersion = tapia_path+"/low-dimensional/"+oldSuffix
        newVersion = tapia_path+"/pisinger_"+str(currentFile)+".kp"
        currentFile += 1
        pisingerFormat(oldVersion, newVersion, True)

def validateFormat(path):
    file = open(path, "r")
    data = file.readlines()
    weight_set = []
    value_set = []

    for i, line in enumerate(data):
        items = line.split(',')
        if i == 0: numItems, knapsackCap = int(items[0]), int(items[1])  #Number of items, Knapsack capacity
        else:
            weight_set.append(int(items[0])) # For each bin: weight, profit
            value_set.append(float(items[1]))
    if numItems <= 0:
        print("Size negative")
        return False
    if knapsackCap <= 0:
        print("capacity negative")
        return False

    if len(weight_set) != numItems or len(value_set) != numItems:
        print("Wrong size")
        return False 
    for w, v in zip(weight_set, value_set):
        if w <= 0 or v <= 0:
            print("negative numbers")
            return False 
        if w > knapsackCap:
            print(w, v)
            print("out limit")
            return False 
    return True

addFormatAndName()
tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/"
sources = ["martello", "ortizbayliss", "pisinger"]
typesIns = [14, 4, 1]
insPerType = [50, 25, 31]

for source, types, sizeTypes in zip(sources, typesIns, insPerType):
    for typeFile in range(1, types+1):
        for currentCase in range(sizeTypes):
            instanceFile = tapia_path+source.capitalize()+"/"+source
            if types != 1:
                instanceFile += "_"+str(typeFile)
            instanceFile += "_"+str(currentCase)+".kp"
            if validateFormat(instanceFile) is False:
                print("ERROR\n")
                print(instanceFile)
            
