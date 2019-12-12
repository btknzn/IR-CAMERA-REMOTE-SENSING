import pandas as pd
import numpy as np

def main():
    url="http://193.196.175.153/es_lebt_out.php"
    data = pd.read_csv(url, sep= ';',delimiter = None)
    #reading data from Text File
    f = open("information.txt","r")
    amount = f.readlines()
    #deleting unnecessary datas
    data=data[data.STATE==77]
    data = data.values.tolist()
    value = int(len(data))
    dataset = np.zeros((value,8))
    constructDataset(data,dataset,amount)
    dataset = dataset[dataset[:,7]!=9]
    df =pd.DataFrame(dataset)
    df.to_csv('succes.csv')



def calculateTimeonInfo(line):
    time = int(line[9:11])*44640+ int(line[12:14])*1440+int(line[15:17])*60+int(line[18:20])
    return time



def constructDataset(data,dataset,amount):
    dataset1 = np.zeros((len(data),2))
    times = np.zeros((len(amount),2))
    for i in range (0,len(data)):
        dataset1[i][0] = int(data[i][0][4:6])*44640 +int(data[i][0][6:8])*1440+int(data[i][0][9:11])*60 + int(data[i][0][11:13])
    for i in range (0, len(amount)):
        times[i][0] = calculateTimeonInfo(amount[i])                  
    for i in range (0,len(dataset1)):
        for j in range (1,len(times)):
            if(int(times[j][0])>=int(dataset1[i][0]) and int(dataset1[i][0])>int(times[j-1][0])):
                dataset1[i][1]  = setAmountofHuman(j-1,amount)
        if (int(dataset1[i][0])>int(times[len(times)-1][0])):
           dataset1[i][1] = 9
        if (int(dataset1[i][0])<int(times[0][0])):
            dataset1[i][1] = 9                

    for i in range(0,len(dataset1)):
        dataset[i][7]=dataset1[i][1]
        a = data[i][4]
        for p in range (0,7):
            location = a.find('-')
            value = float(a[0:location])
            dataset[i][p]=value
            a = a[location+1:]
    
    

def setAmountofHuman(p,amount):
     charLocation =int(amount[p].find('-'))
     charLocation1 = int(amount[p+1].find('-'))
     charNumber = amount[p][0:charLocation]
     charNumber1 = amount[p+1][0:charLocation1]
     if (charNumber1=='X'):     
         return 9     
     if (charNumber =='X'):
         return 9
     return int(charNumber)


    
if __name__ == "__main__":
    main()