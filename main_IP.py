
from knapsack import Item, Knapsack, generateItemsList
from IO import load_data
from ip_solve import IPSolve
import pandas as pd
#if __name__ == '__main__':
dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/"
#solve with IP Brach and Bound
data = []
for i in range(31):
    capacity, lenItems, values_set, weight_set = load_data(dany_path+"Pisinger/pisinger_"+str(i)+".kp")
    #capacity, lenItems, values_set, weight_set = load_data(dany_path+"test.txt")
    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    profit = IPSolve(items, kp.getCapacity(), show = False)
    data.append([capacity, lenItems, values_set, weight_set,profit])
df  = pd.DataFrame(data,columns = ['Cap','Items','Values','Weights','Profit_Obtained'])
df.to_csv('solveIP.csv',index = False)

 