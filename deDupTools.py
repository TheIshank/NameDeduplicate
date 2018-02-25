import pandas as pd
from nameparser.parser import HumanName


def preProcess(names):
    #Converting names to HumanName class objects
    fullName = []
    for x,name in names.iterrows():
        fullName.append(HumanName(name.fn + ' ' + name.ln))
    names['fullName'] = fullName
    
    #Converting dob to pandas.datetime object (assuming that entries are not older than 100 years)
    dobs = []
    for entry in names.dob:
        if(int(entry[-2:]) < 18):
            dob = 2000+int(entry[-2:])
        else:
            dob = 1900+int(entry[-2:])
        dobs.append(str(entry[:-2])+str(dob))
    names.dob = dobs
    names.dob = pd.to_datetime(names.dob)

def generateCross(names):
    #Create a new dataframe which compares every entry with every other entry
    entries = []
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            record = {}
            record['fullName1'] = names.fullName[i]
            record['dob1'] = names.dob[i]
            record['gn1'] = names.gn[i]
            record['fullName2'] = names.fullName[j]
            record['dob2'] = names.dob[j]
            record['gn2'] = names.gn[j]
            entries.append(record)
    namesCross = pd.DataFrame(entries)
    count = 0
    for x,name in namesCross.loc[(namesCross.dob1 == namesCross.dob2)].iterrows():
        if(name.fullName1.first == name.fullName1.first):
            count+=1
    # print("Number of entries having same date of birth and first name: ", count)
    # print("Number of entries having same date of birth and gender: ", len(namesCross.loc[(namesCross.dob1 == namesCross.dob2) & (namesCross.gn1 == namesCross.gn2)]))
    # print("Number of entries having same date of birth: ",len(namesCross.loc[(namesCross.dob1 == namesCross.dob2)]))
    return namesCross


def processNames(name1, name2):
    names = list((set(name1.middle.split(' ')) | set(name2.middle.split(' ')) | set(name1.last.split(' ')) | set(name2.last.split(' '))) - {''})
    for name in names:
            if(len(name) == 1):
                for othername in names:
                    if(othername[0] == str(name) and othername!=name):
                        names.remove(name)
                        break
    if(name1.last in names):
        names.remove(name1.last)
        name1.middle = ' '.join(names)
    elif(name2.last in names):
        names.remove(name2.last)
        name1.last = name2.last
        name1.middle = ' '.join(names)


def checkSame(names):
    same = []
    for x,entry in names.iterrows():
        if(entry.dob1 == entry.dob2 and entry.gn1 == entry.gn2 and entry.fullName1.first == entry.fullName2.first):
            same.append(1)
        else:
            same.append(0)
    names['same'] = same

def deDuplicate(names):
    preProcess(names)
    namesCross = generateCross(names)
    namesCross.head()
    checkSame(namesCross)
    n = len(names)
    finals = []
    deleted = set()
    for x,name1 in names.iterrows():
        if x in deleted:
            continue
        record = {}
        if(x == 0):
            record['fullName'] = namesCross.fullName1[x]
            record['dob'] = namesCross.dob1[x]
            record['gn'] = namesCross.gn1[x]
            for y,name2 in names.loc[x+1:].iterrows():
                z = y
                z-=1
    #             print(z," ",namesCross.same[z])
                if(namesCross.same[z] == 1):
                    processNames(record['fullName'],namesCross.fullName2[z])
                    deleted.add(y)

        elif(x!=len(names)-1):
            t = sumAP(n-1,x,-1)
    #         print(t)
            record['fullName'] = namesCross.fullName1[t]
            record['dob'] = namesCross.dob1[t]
            record['gn'] = namesCross.gn1[t]
            for y,name2 in names.loc[x+1:].iterrows():
                k = y-x-1
    #             print(t+k)
                if(namesCross.same[t+k] == 1):
#                     print("yeah", x, y, t+k)
                    processNames(record['fullName'],namesCross.fullName2[t+k])
                    deleted.add(y)
        else:
            record['fullName'] = namesCross.fullName1[len(namesCross) - 1]
            record['dob'] = namesCross.dob1[len(namesCross) - 1]
            record['gn'] = namesCross.gn1[len(namesCross) - 1]
        finals.append(record)
#         print(finals)
    finals = pd.DataFrame(finals)
    return finals

def sumAP(a,n,d):
    s = n * (2 * a + (n-1)*d)/2
    return s