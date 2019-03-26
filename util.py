# coding: utf-8
import csv
import os


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
    for i in range(0, len(arr) - 1): 
        if (arr[i][2] < arr[minInd][2]): 
            minInd = i 
    return minInd 

def getMax(arr): 
  
    maxInd = 0
    for i in range(0, len(arr) - 1): 
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
def minCashFlowRec(amount): 
  
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
    if (amount[mxCredit][2] == 0 and amount[mxDebit] == 0): 
        return 0
  
    # Find the minimum of two amounts 
    min = minOf2(-amount[mxDebit][2], amount[mxCredit][2]) 
    amount[mxCredit][2] -=min
    amount[mxDebit][2] += min
  
    # If minimum is the maximum amount to be 
  
    # Recur for the amount array. Note that 
    # it is guaranteed that the recursion 
    # would terminate as either amount[mxCredit]  
    # or amount[mxDebit] becomes 0 
    minCashFlowRec(amount) 

  



cAmount = curtailment('test.csv')
pricingData = pricing(100, cAmount)
print(pricingData)
minCashFlowRec(pricingData)
print(pricingData)

