import pandas as pd
import editdistance
from nameparser.parser import HumanName
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
import graphviz
import numpy as np

#Function to compare two father names and 
def checkFname(fname1, fname2):
    #If both the names are exactly same
    if (fname1 == fname2):
        return True
    fname1 = fname1.split(' ')
    fname2 = fname2.split(' ')
    #If both names are single words and are not equal
    if(len(fname1) == len(fname2) == 1):
        return False
    #If both names are having more than one word
    if(len(fname1) == len(fname2)):
        #If first names are not equal
        if(fname1[0] != fname2[0]):
            return False
        #If the first character of last name are not same
        if(fname1[1][0] != fname2[1][0]):
            return False
        #If the first character of last name are same and either of the last names are single character
        if(len(fname1[1]) == 1 or len(fname2[1]) == 1):
            return True
        #If both names have same number of words and are not same
        else:
            return False
        #If both names are not having same no. of words but the first names are same
    elif(len(fname1) != len(fname2) and fname1[0] == fname2[0]):
        return True
    
#Function to calculate sum of AP
def sumAP(a,n,d):
    s = n * (2 * a + (n-1)*d)/2
    return s

def processNames(name1, name2):
    if(name1.middle != name2.middle):
        n1 = name1.middle.split(' ')
        n2 = name2.middle.split(' ')
        n = list(set(n1) | set(n2))
        for name in n:
            if(len(name) == 1):
                for othername in n:
                    if(othername[0] == str(name) and othername!=name):
                        n.remove(name)
                        break
        name1.middle = ' '.join(n)
    #Compare last names and choose the not abbreviated one
    if(name1.last != name2.last):
        if(len(name1.last) < len(name2.last)):
            name1.last = name2.last
    if(name1.suffix != name2.suffix):
        if(len(name1.suffix) < len(name2.suffix)):
            name1.suffix = name2.suffix
    return name1

#Function to perform preprocessing on the data    
def preProcess(names):
    suffixes = ["JR","SR","I","II","III","IV"]
    
    #Converting the dates in proper format
    dobs = []
    for entry in names.dob:
        dob = 1900+int(entry[-2:])
        if(dob>2018):
            dob-=100
        dobs.append(str(entry[:-2])+str(dob))
    names.dob = dobs
    names.dob = pd.to_datetime(names.dob)
    
    #Create a new dataframe which compares every entry with every other entry
    entries = []
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            record = {}
            record['ln1'] = names.ln[i]
            record['dob1'] = names.dob[i]
            record['gn1'] = names.gn[i]
            record['fn1'] = names.fn[i]
            record['ln2'] = names.ln[j]
            record['dob2'] = names.dob[j]
            record['gn2'] = names.gn[j]
            record['fn2'] = names.fn[j]
            entries.append(record)
    namesCross = pd.DataFrame(entries)
    
    #Comparing DOBs, Father's Names, First Names, Last Names etc
    ln1 = []
    ln2 = []
    gender = []
    father = []
    dob = []
    first = []
    editdist = []
    last = []
    lastFirst = []
    ln1_length = []
    ln2_length = []
    for i in range(len(namesCross)):
        name1 = HumanName(namesCross['ln1'][i].upper())
        name2 = HumanName(namesCross['ln2'][i].upper())
        
        
        #Check if gender of both entries is same
        if(namesCross['gn1'][i] == namesCross['gn2'][i]):
            gender.append(1)
        else:
            gender.append(0)
        
        #Check if father's name for both entries is same
        if(checkFname(namesCross['fn1'][i],namesCross['fn2'][i])):
            father.append(1)
        else:
            father.append(0)
        
        #Check if DOB for both the entries is same
        if(namesCross['dob1'][i] == namesCross['dob2'][i]):
            dob.append(1)
        else:
            dob.append(0)
        
        #Check if the first name of both the entries is same
        if(name1.first == name2.first):
            first.append(1)
        else:
            first.append(0)
        
        #Calculate edit distance between first names of both entries
        editdist.append(editdistance.eval(name1.first,name2.first))
        
        #If the last name is a suffix categorize it correctly
        if(name1.last.upper() in suffixes):
            name1.suffix = name1.last
            name1.last = ''
        if(name2.last.upper() in suffixes):
            name2.suffix = name2.last
            name2.last = ''
        
        #Check if last names of both the entries are same
        if(name1.last == name2.last or name1.last == '' or name2.last == ''):
            last.append(1)
        else:
            last.append(0)
        
        #Check if the first character of last name of both entries is same while one of the entries is having abbreviated last name 
        if((name1.last != '' and name2.last != '') and (name1.last == name2.last[0] or name1.last[0] == name2.last)):
            lastFirst.append(1)
        else:
            lastFirst.append(0)
        
        #Calculating the length of names for both the entries
        ln1_length.append(len(name1))
        ln2_length.append(len(name2))
        ln1.append(name1)
        ln2.append(name2)

    namesCross['ln1'] = ln1
    namesCross['ln2'] = ln2
    namesCross['sameDob'] = dob
    namesCross['sameGender'] = gender
    namesCross['sameFather'] = father
    namesCross['sameFname'] = first
    namesCross['distFname'] = editdist
    namesCross['sameLname'] = last
    namesCross['sameLnameInitial'] = lastFirst
    namesCross['ln1_len'] = ln1_length
    namesCross['ln2_len'] = ln2_length
    return namesCross

#Function to generate training data on which the model can be learned
def generateTrain(names):
    names = preProcess(names)
    result = []
    for i in range(len(names)):
        result.append(0)
        if(names.sameDob[i] and names.sameGender[i] and names.sameFather[i]):
            if(names.sameFname[i]):
                if(names.sameLname[i] or names.sameLnameInitial[i]):
                    result[i] = 1
    names['same'] = result
    return names

#Function to train the model using the given training data and also 
def deDuplicateTrain(names, clf):
    n = len(names)
    namesCross = generateTrain(names)
    X = namesCross[['sameDob', 'sameGender', 'sameFather', 'sameFname', 'distFname', 'sameLname', 'sameLnameInitial', 'ln1_len', 'ln2_len']]
    y = namesCross['same']
    clf.fit(X,y)

#Function to de-duplicate the data
def deDuplicate(names,clf):
    n = len(names)
    finals = []
    deleted = set()
    namesCross = preProcess(names)
    X = namesCross[['sameDob', 'sameGender', 'sameFather', 'sameFname', 'distFname', 'sameLname', 'sameLnameInitial', 'ln1_len', 'ln2_len']]
    namesCross['same'] = clf.predict(X)
    for x,name1 in names.iterrows():
        if x in deleted:
            continue
        record = {}
        if(x == 0):
            record['ln'] = namesCross.ln1[x]
            record['dob'] = namesCross.dob1[x]
            record['gn'] = namesCross.gn1[x]
            record['dob'] = namesCross.dob1[x]
            record['fn'] = namesCross.fn1[x]
            for y,name2 in names.loc[x+1:].iterrows():
                z = y
                z-=1
    #             print(z," ",namesCross.same[z])
                if(namesCross.same[z] == 1):
                    record['ln'] = processNames(record['ln'],namesCross.ln2[y])
                    deleted.add(y)

        elif(x!=len(names)-1):
            t = sumAP(n-1,x,-1)
    #         print(t)
            record['ln'] = namesCross.ln1[t]
            record['dob'] = namesCross.dob1[t]
            record['gn'] = namesCross.gn1[t]
            record['dob'] = namesCross.dob1[t]
            record['fn'] = namesCross.fn1[t]
            for y,name2 in names.loc[x+1:].iterrows():
                k = y-x-1
    #             print(t+k)
                if(namesCross.same[t+k] == 1):
    #                 print("yeah", x, y, t+k)
                    record['ln'] = processNames(record['ln'],namesCross.ln2[t+k])
                    deleted.add(y)
        else:
            record['ln'] = namesCross.ln1[len(namesCross) - 1]
            record['dob'] = namesCross.dob1[len(namesCross) - 1]
            record['gn'] = namesCross.gn1[len(namesCross) - 1]
            record['dob'] = namesCross.dob1[len(namesCross) - 1]
            record['fn'] = namesCross.fn1[len(namesCross) - 1]
        finals.append(record)
    return pd.DataFrame(finals)

#Function to plot features
def plot_feature_importances(model):
    n_features = X.shape[1]
    plt.barh(range(n_features),model.feature_importances_,align='center')
    plt.yticks(np.arange(n_features),X.columns)
    plt.xlabel("Feature importance")
    plt.ylabel("feature")
    plt.savefig("feature_importance.png")
    plt.close()
#Function to view insights of the classifier
def exportInsights(clf):
    if(type(clf) == sklearn.tree.tree.DecisionTreeClassifier):
        export_graphviz(clf,out_file="nameTree.dot",class_names=["Different","Same"],feature_names=X.columns,impurity=False,filled=True)
