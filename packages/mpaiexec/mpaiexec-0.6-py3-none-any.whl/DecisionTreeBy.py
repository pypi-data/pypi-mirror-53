import math

class DataSet:
    def __init__(self, ds):
        self.dataset = ds

    def uniqueAns(self):
        return len(set(self.dataset["Ans"]))

    def getMaxOccur(self):
        unique = set(self.dataset["Ans"])
        maximum = 0
        maxValue = 0
        for i in unique:
            temp = self.dataset["Ans"].count(i)
            if temp > maximum:
                maximum = temp
                maxValue = i
        return maxValue
    
    def getEntropy(self, values):
        uniqueValues = dict()
        for i in set(values):
            uniqueValues[i] = values.count(i)
        entropy = 0
        for i in uniqueValues:
            p = uniqueValues[i]/len(values)
            e = p*math.log2(p)
            entropy += e
        return -entropy

    def split(self, feature):
        uniqueValues = {}
        values = self.dataset[feature]
        answers = self.dataset["Ans"]
        features = self.dataset["Features"].copy()
        features.remove(feature)
        for i in range(len(values)):
            if not uniqueValues.__contains__(values[i]):
                uniqueValues[values[i]] = {"Ans": [answers[i]]}
                for f in features:
                    uniqueValues[values[i]][f] = [self.dataset[f][i]]
                uniqueValues[values[i]]["Features"] = features
            else:
                uniqueValues[values[i]]["Ans"].append(answers[i])
                for f in features:
                    uniqueValues[values[i]][f].append(self.dataset[f][i])
        for i in uniqueValues:
            uniqueValues[i] = DataSet(uniqueValues[i])
        return uniqueValues

    def getInfoGain(self, feature):
        uniqueValues = self.split(feature)
        featureEntropy = 0
        for i in uniqueValues:
            featureEntropy += len(uniqueValues[i].dataset['Ans'])*self.getEntropy(uniqueValues[i].dataset['Ans'])/len(self.dataset['Ans'])
        infoGain = self.getEntropy(self.dataset['Ans']) - featureEntropy
        return infoGain

    def findBestFeature(self):
        features = self.dataset["Features"]
        if len(features) > 0:
            maximum = self.getInfoGain(features[0])
            maximumIndex = 0
            for i in range(len(features)):
                temp = self.getInfoGain(features[i])
                if temp > maximum:
                    maximum = temp
                    maximumIndex = i
            return features[maximumIndex]
        else:
            return None

def calculateAns(dataset, feature, maxoccur, descr):
    branches = dataset.split(feature)
    for key in list(branches.keys()):
        newDS = branches[key]
        if (newDS.uniqueAns() == 1):
            print("Answer for ", descr + "-" + feature , " with value =", key , " is :", newDS.dataset['Ans'][0])
        elif(newDS.uniqueAns() == 0):
            print("in zero")
            print("Answer for ", descr+"-" +feature , " with value =", key , " is :", maxoccur)            
        elif(newDS.uniqueAns() >1 and len(newDS.dataset["Features"]) ==0 ) :
            print("Answer for ", descr+"-" +feature , " with value =", key , " is :", newDS.getMaxOccur())            
        else:            
            newfeat = newDS.findBestFeature()
            newmaxoccur = newDS.getMaxOccur()
            calculateAns(newDS, newfeat, newmaxoccur , descr + ":" + feature +":->" + key + " " )            
    
dataset = {
        "Ans" :["Mammal", "Mammal", "Reptile", "Mammal", "Mammal", "Mammal", "Reptile", "Reptile", "Mammal", "Reptile"],
        "Features":["toothed", "breaths", "legs"],
        "toothed" : ["T", "T", "T", "F", "T", "T", "T", "T", "T", "F"],
        "breaths" : ["T", "T", "T", "T", "T","T", "F", "T", "T", "T"],
        "legs":["T", "T", "F", "T", "T","T", "F", "F", "T", "T"]
        }

dt = DataSet(dataset)
if dt.uniqueAns() > 1:
    feat = dt.findBestFeature()
    calculateAns(dt, feat, dt.getMaxOccur(), "")
