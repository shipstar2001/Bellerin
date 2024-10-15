class Database :
    def __init__(self) :
        self.Database = {}
        
    def registNewCustomer(self, customerID, customerName) :
        temp = {}
        if self.Database.get(customerID) == None :
            self.Database[customerID] = customerName
            temp[customerID] = customerName
            return temp
        else :
            return -1
score = 0
       
try:
    myDB = Database()

    solution = [True, True, True]
    answer = []

    res = myDB.registNewCustomer('0001', 'Apple')
    if res == {'0001': 'Apple'}:
        answer.append(True)

    res = myDB.registNewCustomer('0002', 'Tomato')
    if res == {'0002': 'Tomato'}:
        answer.append(True)

    res = myDB.registNewCustomer('0001', 'Apple')
    if res == -1:
        answer.append(True)

    if answer == solution:
        score += 6
        print("[1] SUCCESS")
    else:
        print("[1] FAIL")
except:
    print("[1] FAIL")