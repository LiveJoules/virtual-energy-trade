# coding: utf-8
import csv
import os
from tempfile import NamedTemporaryFile
import shutil



def curtailment(data):
    consumption = 0.0
    production = 0.0
    totalCurtailment = 0.0
    purchaseSale = []
    ifile = open(data)
    reader = csv.reader(ifile)
    testData = list(reader)
    for row in testData:
        try:
            if int(row[1]) > 0:
                consumption += int(row[1])
            elif int(row[1]) <0:
                production += abs(int(row[1]))
        except:
            print('Column headers found')

    if consumption > production:
        totalCurtailment = consumption - production
        for row in testData:
            if int(row[1]) > 0:
                userCurtailment = int(row[1]) - ((totalCurtailment/consumption) * int(row[1]))
                purchaseSale.append([row[0], userCurtailment])
            else:
                purchaseSale.append([row[0], int(row[1])])


    if consumption < production:
        totalCurtailment = production - consumption
        for row in testData:
            if int(row[1]) < 0:
                userCurtailment = int(row[1]) - ((totalCurtailment/production) * int(row[1]))
                purchaseSale.append([row[0], userCurtailment])
            else:
                purchaseSale.append([row[0], int(row[1])])

    if consumption == production:
        for row in testData:
            purchaseSale.append([row[0], row[1]])

    return purchaseSale


def pricing(unitPrice, purchaseSale):
    for row in purchaseSale:
        row.extend([row[1] * unitPrice])
    
    return purchaseSale

def getMin(arr): 
      
    minInd = 0
    for i in range(0, len(arr)): 
        if (arr[i][2] < arr[minInd][2]): 
            minInd = i 
    return minInd 

def getMax(arr): 
  
    maxInd = 0
    for i in range(0, len(arr)): 
        if (arr[i][2] > arr[maxInd][2]): 
            maxInd = i 
    return maxInd

def minOf2(x, y): 
  
    return x if x < y else y 
  
# amount[p] indicates the net amount to 
# be credited/debited to/from person 'p' 
# If amount[p] is positive, then i'th  
# person will amount[i] 
# If amount[p] is negative, then i'th 
# person will give -amount[i] 
def minCashFlowRec(amount, initialAccounts):
    

    # Find the indexes of minimum 
    # and maximum values in amount[] 
    # amount[mxCredit] indicates the maximum 
    # amount to be given(or credited) to any person. 
    # And amount[mxDebit] indicates the maximum amount 
    # to be taken (or debited) from any person. 
    # So if there is a positive value in amount[],  
    # then there must be a negative value 
    mxCredit = getMax(amount) 
    mxDebit = getMin(amount)
    # If both amounts are 0,  
    # then all amounts are settled 
    # print(mxCredit, mxDebit, amount[mxCredit][2], amount[mxDebit][2])
    if (amount[mxCredit][2] <= 0.000001 and amount[mxDebit][2] <= 0.000001): 
        return initialAccounts
  
    # Find the minimum of two amounts 
    min = minOf2(-amount[mxDebit][2], amount[mxCredit][2]) 
    # print(min)
    amount[mxCredit][2] -=min
    amount[mxDebit][2] += min
    # If minimum is the maximum amount to be 

    print('Account ', amount[mxDebit][0], ' pays ', min, ' to Account ', amount[mxCredit][0])
    for user in initialAccounts:
        if amount[mxDebit][0] == user[0]:
            user[2] += min
        
        if amount[mxCredit][0] == user[0]:
            user[2] -= min
    
    # Recur for the amount array. Note that 
    # it is guaranteed that the recursion 
    # would terminate as either amount[mxCredit]  
    # or amount[mxDebit] becomes 0
    return minCashFlowRec(amount, initialAccounts) 

def updateConsumption(accounts, pricingData):
    for user in pricingData:
        if user[1] > 0:
            accounts[int(user[0])][1] += user[1]
    return accounts
      


    
        



cAmount = curtailment('test.csv')
print(cAmount)
pricingData = pricing(100, cAmount)
# print(pricingData)
ifile = open('accounts.csv')
reader = csv.reader(ifile)
accounts = list(reader)
for user in accounts:
    user[1] = float(user[1])
    user[2] = float(user[2])
# tempfile = NamedTemporaryFile(delete=False)

    
updatedAccountBalance = minCashFlowRec(pricingData, accounts)
updatedAccounts = updateConsumption(updatedAccountBalance, pricingData)

filename = 'accounts.csv'
tempfile = NamedTemporaryFile(delete=False)

with open(filename, 'rb') as csvFile, tempfile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')
    writer = csv.writer(tempfile, delimiter=',', quotechar='"')

    for row in reader:
        row = accounts[int(row[0])]
        writer.writerow(row)

shutil.move(tempfile.name, filename)

# shutil.move(tempfile.name, 'accounts.csv')
print(pricingData)
print(updatedAccounts)

