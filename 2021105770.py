def add(int1, int2) :
    return int1 + int2

def checkIntegerType(inputValue) :
    if type(inputValue) is int :
        return True
    else :
        return False
    
def addIntoList(inputList, int1) :
    inputList.append(int1)
    return inputList

def addNumbersByTuple(int1, int2) :
    num1 = int1
    num2 = int2
    num3 = int1 + int2
    return (num1, num2, num3)

class Storage :
    def __init__(self) :
        self.tempDict = {}
    
    def addProduct(self, name, number) :
        if number == 0 or number < 0 :
            return False, -1
        else :
            if self.tempDict.get(name) == None :
                self.tempDict[name] = number
            else :
                self.tempDict[name] += number
            return name, self.tempDict[name]
    
    def getProduct(self, name) :
        if name in self.tempDict.keys() :
            return True, name, self.tempDict[name]
        else :
            return False, -1, -1
    
    def delProduct(self, name, number) :
        if self.tempDict.get(name) == None :
            return False, -1, -1
        elif self.tempDict[name] < number :
            return False, -1, -1
        else : 
            final_num = self.tempDict[name] - number
            if final_num == 0 :
                self.tempDict.pop(name)
            return True, name, final_num
         
    def getAllProductsNameBySet(self) :
        tempSet = set()
        for key in self.tempDict :
            tempSet.add(key)
        return tempSet
            
    def getAllProductsByList(self, input) :
        tempList = []
        biggerList = []
        if input == False or input == '' :
            for key in self.tempDict :
                tempList.append(key)
                tempList.append(self.tempDict[key])
                biggerList.append(tempList)
            biggerList.sort()
            return biggerList
        elif input == True :
            for key in self.tempDict :
                tempList.append(key)
                tempList.append(self.tempDict[key])
                biggerList.append(tempList)
            biggerList.sort(reverse = True)
            return biggerList
        
class FinancialStorage(Storage) :
    def __init__(self) :
        super().__init__()
    
    def setProductsValue(self, inputDict) :
        tempList = []
        if type(inputDict) is not dict :
            return False, -1
        else :
            for item in inputDict :
                tempList.append(item)
            tempList.sort()
            return True, tempList