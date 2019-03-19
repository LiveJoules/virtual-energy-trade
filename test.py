# coding: utf-8
import csv
import os

consumption = 0
production = 0
curtailment = 0
purchaseSale = []
ifile = open('test.csv')
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
    curtailment = consumption - production
    for r

print(consumption, production)