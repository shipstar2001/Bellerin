class MySelfClass :
    def __init__(self) :
        self.studentID = '2021105770'
        self.studentBirthday = '20010309'
    
    def getStudentID(self) :
        return self.studentID
    
    def getBirthday(self) :
        return self.studentBirthday
    
    def getTermProject(self) :
        pass
    
class IntegerAccumulator :
    def __init__(self) :
        self.inputList = []
    
    def getNewInteger(self, inputInteger) :
        self.inputList.append(inputInteger)
        return inputInteger
    
    def getAccumulatedIntegers(self) :
        return self.inputList
    
    def getAverage(self) :
        temp = 0
        for item in self.inputList :
            temp += int(item)
        avg = temp / len(self.inputList)
        return avg
    
def calcIntegerFromString(inputString) :
    count = 0
    for element in inputString :
        if element.isdigit() == True :
            count += int(element)
        else :
            count += 0
    return count

def shiftStringLeft(inputString) :
    tempString = ''
    tempString += inputString[1:]
    tempString += inputString[0]
    return tempString

class StringAccumulator :
    def __init__(self) :
        self.tempList = []
        
    def putNewString(self, inputString) :
        self.tempList.append(inputString)
        return len(self.tempList)
    
    def getMaxString(self) :
        max = 0
        for item in self.tempList :
            if    :
                max = item
        return max
    
student1 = IntegerAccumulator()
print(student1.getNewInteger(5))
print(student1.getNewInteger(6))
print(student1.getAccumulatedIntegers())
print(student1.getAverage())
print(calcIntegerFromString('55a555'))
print(shiftStringLeft('ABCDEF'))

student2 = StringAccumulator()
print(student2.putNewString('hello'))
print(student2.putNewString('bals'))
print(student2.getMaxString())