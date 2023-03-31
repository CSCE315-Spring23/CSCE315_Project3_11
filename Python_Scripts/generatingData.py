import datetime
import random
import time as time
import ast
import hashlib

# test

def generateDatesWithinPastYear():
    now = datetime.datetime.now()
    currDate = now.strftime("%m/%d/%Y")
    currMonth = int(currDate[0:2])
    currDay = int(currDate[3:5])
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day = random.randint(1, 31)
    else:
        day = random.randint(1, 30)
    if month < currMonth or (month == currMonth and day <= currDay):
        year = 2023
    else:
        year = 2022
    return f"{month}/{day}/{year}"


def generateEmployeeData():
    employeesDataFile = open("employeesData.csv", "w+")
    lastNames = ["Gonce", "Noyes", "Pusey", "Lee", "Fattig"]
    firstNames = ["Alex", "Anthony", "Drew", "Stanley", "Brendan"]
    numEmployees = len(lastNames)
    # employee data columns
    # PK:   employeeID (int)
    #       lastName (string)
    #       firstName (string)
    #       hireDate (date)
    #       employeePin (int)
    #       positionTitle (string)
    #       hourWorked (float)

    isThereManager = False  # implement late, try to guarantee manager
    employeesDataFile.write("EmployeeID,LastName,FirstName,HireDate,EmployeePIN,PositionTitle,HoursWorked\n")
    for i in range(numEmployees):
        employeeID = f"0000{i + 1}"

        # lastName = input("Last name: ")
        lastName = lastNames[i]

        # firstName = input("First name: ")
        firstName = firstNames[i]

        # Data creation on 2/24
        # hireDate = datetime.datetime.strptime(input("Hire date: "), "%m/%d/%Y").date()
        hireDate = generateDatesWithinPastYear()
        hireDate = datetime.datetime.strptime(hireDate, "%m/%d/%Y").date()

        employeePin = random.randint(1, 9999)
        employeePin = "{:0>4}".format(employeePin, "0")

        positionRan = random.randint(1, 100)
        if positionRan < 10 or (i == (numEmployees - 1) and not isThereManager):
            positionTitle = "Manager"
            isThereManager = True
        else:
            positionTitle = "Server"

        hoursWorked = random.randint(0, 140) / 4

        addEmployee = f"{employeeID},{lastName},{firstName},{hireDate},{employeePin},{positionTitle},{hoursWorked}\n"
        employeesDataFile.write(addEmployee)

    employeesDataFile.close()


def generateInventoryItems():
    inventoryItemsFile = open(f"inventoryItems.csv", "w+")
    inventoryItemsFile.write("Name,Stock,NumberNeeded,OrderChance,Units,Category,Servings,RestockCost\n")
    # PK:   itemName (string)
    #       stock (int)
    #       numNeeded (int)
    #       orderChance (float)
    #       units (string)
    #       category (string)
    #       servings (int)
    servings = 0
    restockCost = 0
    bases = ["shreddedLettuce", "spinach", "brownRice", "whiteRice"]
    protein = ["chicken", "lamb", "falafel", "beef", "pork"]
    toppings = ["couscous", "onions", "bigTomatoes", "smallTomatoes", "pitaChips", "vegetableMedley", "olives",
                "pickledOnions", "cucumbers", "cauliflower", "peppers", "redCabbageSlaw", "garlicFries"]
    sauces = ["hummus", "spicyHummus", "jalapenoFeta", "tzatziki", "greekVinaigrette", "harrisaYogurt", "yogurtDill",
              "tahini"]
    drinks = ["pepsiSyrup", "sierraMistSyrup", "briskSyrup", "pepsiZeroSyrup", "pepsiDietSyrup", "gatoradeSyrup",
              "mtnDewSyrup", "drPepperSyrup"]
    nonPerishable = ["cupDrink", "cupWater", "bowls", "straws", "cupLids", "bowlLids", "utensilPacks"]
    itemNames = bases + protein + toppings + sauces + drinks + nonPerishable

    for item in itemNames:
        units = ""
        category = ""
        orderChance = 1
        if item in bases:
            if "Rice" in item:
                units = "50 lb"
                servings = 200
                restockCost = 30
            else:
                units = "5 lb"
                servings = 50
                restockCost = 25
            category = "base"
            stock = 10
            orderChance = 1/4
            
        if item in protein:
            units = "160 oz"
            category = "protein"
            orderChance = 1/5
            servings = 16
            stock = 10
            if "chicken" in item or "falafel" in item:
                restockCost = 100
            else:
                restockCost = 290
        elif item in toppings:
            units = "80 oz"
            category = "toppings"
            orderChance = 2/15
            servings = 20
            stock = 10
            restockCost = 40
        elif item in sauces:
            units = "16 oz"
            category = "sauces"
            orderChance = 1/9
            servings = 16
            stock = 10
            restockCost = 25
        elif item in drinks:
            units = "5 gallon"
            category = "drinks"
            orderChance = 1/10
            servings = 100
            stock = 10
            restockCost = 50
        elif item in nonPerishable:
            units = "500 count boxes"
            category = "nonPerishable"
            orderChance = 1/2
            servings = 500
            stock = 10
            restockCost = 20
        numNeeded = 10 - stock

        itemLine = f"{item},{stock},{numNeeded},{orderChance},{units},{category},{servings},{restockCost}\n"
        inventoryItemsFile.write(itemLine)

    inventoryItemsFile.close()


def generateMenuTable():
    menu_items = [["ItemName", "Price"], ["Gyro", 8.09], ["Bowl", 8.09], ["Hummus & Pita", 3.49], ["Falafels", 3.49], ["Extra Protein", 2.49],
                  ["Extra Dressing", 0.39], ["Fountain Drink", 2.45]]

    f = open("MenuItems.csv", "w")
    f.write("ItemName,Price\n")

    for item in menu_items:
        f.write(item[0] + "," + str(item[1]) + "\n")

    f.close()


def generateExpirationDates(itemCounts: list):
    inventoryItemsFile = open(f"inventoryItems.csv", "r+")
    inventoryLines = inventoryItemsFile.readlines()
    # idealItemCounts is how many servings are in a unit of an item
    idealItemCounts = []
    for i in range(len(inventoryLines)):
        if i == 0:
            idealItemCounts.append(-1)
            continue
        idealItemCounts.append(int(inventoryLines[i].split(",")[6])) 
    inventoryItemsFile.close()

    expirationDatesFile = open(f"expirationDates.csv", "w+")
    expirationDatesFile.write("UniqueID,ItemName,ExpirationDate,RemainingServings")
    restockOrdersFileCSV = open(f"restockOrders.csv", "r+")
    uniqueID = 0
    itemName = ""
    expirationDate = ""
    remainingServings = 0
    loopNum = 0
    bases = ["shreddedLettuce", "spinach", "brownRice", "whiteRice"]
    protein = ["chicken", "lamb", "falafel", "beef", "pork"]
    toppings = ["couscous", "onions", "bigTomatoes", "smallTomatoes", "pitaChips", "vegetableMedley", "olives",
                "pickledOnions", "cucumbers", "cauliflower", "peppers", "redCabbageSlaw", "garlicFries"]
    sauces = ["hummus", "spicyHummus", "jalapenoFeta", "tzatziki", "greekVinaigrette", "harrisaYogurt", "yogurtDill",
              "tahini"]
    drinks = ["pepsiSyrup", "sierraMistSyrup", "briskSyrup", "pepsiZeroSyrup", "pepsiDietSyrup", "gatoradeSyrup",
              "mtnDewSyrup", "drPepperSyrup"]
    nonPerishable = ["cupDrink", "cupWater", "bowls", "straws", "cupLids", "bowlLids", "utensilPacks"]
    itemNames = bases + protein + toppings + sauces + drinks + nonPerishable
    for line in (restockOrdersFileCSV.readlines() [-5:]): # base expiration dates on last five restock orders
        elements = line.split(",")

        date_str = ""
        expirationDate = datetime.datetime.strptime("01-10-2022", "%d-%m-%Y")
        itemsArray = []

        for i in range(len(elements)):
            if i == 0: # expecting a date
                date_str = elements[0].strip()
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                continue
            if i == len(elements) - 1 or i == len(elements) - 2: # dont need to look at restock received date or price
                break
            # else expecting an order item
            itemsArrayStr = elements[i].strip().lstrip("[ ").rstrip("]")
            itemsArray.append(ast.literal_eval(itemsArrayStr))

        for i in range(len(itemsArray)):
            if loopNum == 0:
                itemName = itemsArray[i]
                expirationDate = date + datetime.timedelta(days=6)
                uniqueStr = itemName + expirationDate.strftime("%m/%d/%Y")
                uniqueID = int.from_bytes(hashlib.sha256(uniqueStr.encode()).digest(), byteorder='big', signed=False) % (10 ** 14)
                uniqueID %= 10000 # digits go past integer limit so have to limit the amount
                if itemName == "cupDrink" or itemName == "cupWater" or itemName == "bowls" or itemName == "straws" or itemName == "cupLids" or itemName == "bowlLids" or itemName == "utensilPacks":
                    expirationDate = date + datetime.timedelta(weeks=260)
                inventoryNum = itemNames.index(itemName)
                remainingServings = itemCounts[inventoryNum]
                line = f"{uniqueID}, {itemName}, {expirationDate}, {remainingServings}\n"
                expirationDatesFile.write(line)
                continue

            itemName = itemsArray[i]
            expirationDate = date + datetime.timedelta(days=6)
            if itemName == "cupDrink" or itemName == "cupWater" or itemName == "bowls" or itemName == "straws" or itemName == "cupLids" or itemName == "bowlLids" or itemName == "utensilPacks":
                expirationDate = date + datetime.timedelta(weeks=260)
            uniqueStr = itemName + expirationDate.strftime("%m/%d/%Y")
            uniqueID = int.from_bytes(hashlib.sha256(uniqueStr.encode()).digest(), byteorder='big', signed=False) % (10 ** 14)
            uniqueID %= 10000
            inventoryNum = itemNames.index(itemName)
            remainingServings = idealItemCounts[inventoryNum]
            line = f"{uniqueID}, {itemName}, {expirationDate}, {remainingServings}\n"
            expirationDatesFile.write(line)
        loopNum += 1


def makeOrder(itemCounts: list):
    MenuItemsFile = open(f"MenuItems.csv", "r+")
    inventoryItemsFile = open(f"inventoryItems.csv", "r+")
    itemsInOrder = []
    menuItems = []
    orderTotal = 0.0

    menuLines = MenuItemsFile.readlines()
    inventoryLines = inventoryItemsFile.readlines()
    chooseBetween = random.randint(1, 2) # 1 = gyro, 2 = bowl
    if chooseBetween == 1:
        menuItems.append("Gyro")
    else:
        menuItems.append("Bowl")

    orderChipsAndHummus = random.random() < 0.2
    orderFalafel = random.random() < 0.2
    orderExtraSauce = random.random() < 0.1
    orderDrink = random.random() < 0.75
    for i in range(4):
        if i == 0:
            continue
        new_line = menuLines[i].split(",")
        if i == chooseBetween:
            orderTotal += float(new_line[1])
            # determine what base to add to order
            baseNum = random.randint(1,4)
            itemsInOrder.append((inventoryLines[baseNum].split(","))[0])
            itemCounts[baseNum] -= 1
            # pick a protien to add
            protienNum = random.randint(5, 9)
            itemsInOrder.append((inventoryLines[protienNum].split(","))[0])
            itemCounts[protienNum] -= 1
            # decide if extra protien is added
            if random.random() < 0.2:
                menuItems.append("Extra Protein") 
                protienNum = random.randint(5, 9)
                itemsInOrder.append((inventoryLines[protienNum].split(","))[0])
                orderTotal += float(menuLines[4].split(",")[1])
                itemCounts[protienNum] -= 1
            if orderFalafel:
                menuItems.append("Falafels")
                itemsInOrder.append("falafel")
                itemsInOrder.append("falafel")
                orderTotal += 3.49
                itemCounts[6] -= 2
            for j in range(10, 22):
                if j == 14: # don't add pita chips right now
                    continue
                toppingLine = inventoryLines[j].split(",")
                toppingCount = 0
                if random.random() < float(toppingLine[3]) and toppingCount < 4: # only up to 4 toppings
                    itemsInOrder.append(toppingLine[0])
                    toppingCount += 1
                    itemCounts[j] -= 1
            for j in range(23, 30):
                sauceLine = inventoryLines[j].split(",")
                if random.random() < float(sauceLine[3]):
                    itemsInOrder.append(sauceLine[0])
                    itemCounts[j] -= 1
            if orderExtraSauce:
                menuItems.append("Extra Dressing")
                sauceNum = random.randint(23, 30)
                itemsInOrder.append((inventoryLines[sauceNum].split(","))[0])
                orderTotal += 0.39
                itemCounts[sauceNum] -= 1
            if orderChipsAndHummus:
                menuItems.append("Hummus & Pita")
                itemsInOrder.append("pitaChips")
                itemsInOrder.append("hummus")
                orderTotal += 3.49
                itemCounts[23] -= 1
                itemCounts[14] -= 1
            if orderDrink:
                drinkType = random.randint(0, 1)
                if drinkType == 0:
                    itemsInOrder.append("cupWater")
                    itemsInOrder.append("straws")
                    itemsInOrder.append("cupLids")
                    itemCounts[40] -= 1
                    itemCounts[42] -= 1
                    itemCounts[43] -= 1
                else:
                    menuItems.append("Fountain Drink")
                    orderTotal += 2.45
                    itemsInOrder.append("cupDrink")
                    itemsInOrder.append("straws")
                    itemsInOrder.append("cupLids")
                    drinkNum = random.randint(31, 38)
                    itemsInOrder.append((inventoryLines[drinkNum].split(","))[0])
                    itemCounts[39] -= 1
                    itemCounts[42] -= 1
                    itemCounts[43] -= 1
                    itemCounts[drinkNum] -= 1
        if i == 2:
            itemsInOrder.append("bowls")
            itemsInOrder.append("bowlLids")
            itemCounts[41] -= 1
            itemCounts[44] -= 1
    itemsInOrder.append("utensilPacks")
    itemCounts[45] -= 1

    employees = ["0000", "0001", "0002", "0003", "0004"]
    employeeTaker = random.choice(employees)
    for i in range(len(itemCounts)):
        if i == 0:
            continue
        if itemCounts[i] <= 0:
            currStock = int(inventoryLines[i].split(",")[1])
            currNeed = int(inventoryLines[i].split(",")[2])
            currStock -= 1
            currNeed += 1
            newInventoryLine = ""
            for j in range(len(inventoryLines[i].split(","))):
                if (j == 1):
                    newInventoryLine += str(currStock)
                    newInventoryLine += ","
                    continue
                if (j == 2):
                    newInventoryLine += str(currNeed)
                    newInventoryLine += ","
                    continue
                newInventoryLine += (inventoryLines[i].split(",")[j])
                if j != len(inventoryLines[i].split(",")) - 1:
                   newInventoryLine += ","

            inventoryLines[i] = newInventoryLine

            inventoryItemsFile.seek(0)
            inventoryItemsFile.truncate()
            inventoryItemsFile.writelines(inventoryLines)
            itemCounts[i] = int(inventoryLines[i].split(",")[6])

    inventoryItemsFile.close()
    MenuItemsFile.close()
                            
    return employeeTaker, itemsInOrder, orderTotal, itemCounts, menuItems

def generateHistory():
    currentItemCounts = []
    generateInventoryItems()
    open(f"restockOrders.csv", "w+").close()
    open(f"populate_restockorders.sql", "w+").close()
    open(f"restockOrders.csv", "w+").close()
    inventoryItemsFile = open(f"inventoryItems.csv", "r+")
    inventoryLines = inventoryItemsFile.readlines()
    for i in range(len(inventoryLines)):
        if i == 0:
            currentItemCounts.append(-1)
            continue
        currentItemCounts.append(int(inventoryLines[i].split(",")[6])) 
    inventoryItemsFile.close()
    gameDay1 = datetime.datetime.strptime("01-10-2022", "%d-%m-%Y")
    gameDay2 = datetime.datetime.strptime("05-11-2022", "%d-%m-%Y")
    start = datetime.datetime.strptime("01-03-2022", "%d-%m-%Y")
    end = datetime.datetime.strptime("01-03-2023", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    ordersFile = open("populate_orders.sql", "w+")
    restockOrdersFile = open(f"populate_restockorders.sql", "w+")
    zReportsFile = open(f"zReports.sql", "w+")
    restockOrdersFileCSV = open(f"restockOrders.csv", "r+")
    restockOrdersFileCSV.write("DateOrdered,DateReceived,Items,Cost\n")
    dailyTotal = 0.0
    for currDate in date_generated:
        if currDate.weekday() != 6:
            if currDate == gameDay1 or currDate == gameDay2:
                # do gameday calcs
                orders = 390
                timeChange = datetime.timedelta(seconds=90)
                timeTaken = datetime.datetime.combine(currDate, datetime.time(10, 0))
                for order in range(orders):
                    if order == 0:
                        timeChange = datetime.timedelta(seconds=90)
                    elif order == 40:
                        timeChange = datetime.timedelta(seconds=72)
                    elif order == 90:
                        timeChange = datetime.timedelta(seconds=60)
                    elif order == 150:
                        timeChange = datetime.timedelta(seconds=45)
                    elif order == 230:
                        timeChange = datetime.timedelta(seconds=45)
                    elif order == 310:
                        timeChange = datetime.timedelta(seconds=45)
                    
                    employeeID, items, total, currentItemCounts, menuItems = makeOrder(currentItemCounts)
                    line = "INSERT INTO \"Orders\" (\"DateTimePlaced\", \"EmployeeID\", \"Items\", \"Subtotal\", \"Total\", \"MenuItemsInOrder\") VALUES ('" + str(timeTaken) + "', " + str(employeeID) + ", ARRAY" + str(items) + ", " + str(total) + ", " + str(total * 1.0825) + ", ARRAY" + str(menuItems) + ");\n"
                    ordersFile.write(line)
                    timeTaken += timeChange
                    dailyTotal += total
                generateZReport(timeTaken, zReportsFile, dailyTotal)
                dailyTotal = 0.0
                checkInventoryCount(currDate, restockOrdersFile, restockOrdersFileCSV)
            else:
                # normal day
                orders = 300
                timeChange = datetime.timedelta(seconds=90)
                timeTaken = datetime.datetime.combine(currDate, datetime.time(10, 0))
                for order in range(orders):
                    if order == 0:
                        timeChange = datetime.timedelta(seconds=90)
                    elif order == 40:
                        timeChange = datetime.timedelta(seconds=72)
                    elif order == 90:
                        timeChange = datetime.timedelta(seconds=60)
                    elif order == 150:
                        timeChange = datetime.timedelta(seconds=60)
                    elif order == 210:
                        timeChange = datetime.timedelta(seconds=72)
                    elif order == 260:
                        timeChange = datetime.timedelta(seconds=90)
                    employeeID, items, total, currentItemCounts, menuItems = makeOrder(currentItemCounts)
                    line = "INSERT INTO \"Orders\" (\"DateTimePlaced\", \"EmployeeID\", \"Items\", \"Subtotal\", \"Total\", \"MenuItemsInOrder\") VALUES ('" + str(timeTaken) + "', " + str(employeeID) + ", ARRAY" + str(items) + ", " + str(total) + ", " + str(total * 1.0825) + ", ARRAY" + str(menuItems) + ");\n"                    
                    ordersFile.write(line)
                    timeTaken += timeChange
                    dailyTotal += total
                generateZReport(timeTaken, zReportsFile, dailyTotal)
                dailyTotal = 0.0
                checkInventoryCount(currDate, restockOrdersFile, restockOrdersFileCSV)

    restockOrdersFileCSV.close()
    inventoryItemsFile.close()
    zReportsFile.close()
    generateExpirationDates(currentItemCounts)

    

def checkInventoryCount(date, restockOrdersFile, restockOrdersFileCSV):
    inventoryItemsFile = open(f"inventoryItems.csv", "r+")
    inventoryLines = inventoryItemsFile.readlines()
    itemsInOrder = []
    cost = 0
    dateOrdered = date
    
    for i in range(len(inventoryLines)):
        if i == 0:
            continue
        if int(inventoryLines[i].split(",")[1]) <= 0:
            itemsInOrder.append(inventoryLines[i].split(",")[0])
            cost += int(inventoryLines[i].split(",")[7]) * int(inventoryLines[i].split(",")[2])
            newInventoryLine = ""
            for j in range(len(inventoryLines[i].split(","))):
                if (j == 1):
                    newInventoryLine += str(10)
                    newInventoryLine += ","
                    continue
                if (j == 2):
                    newInventoryLine += str(0)
                    newInventoryLine += ","
                    continue
                newInventoryLine += (inventoryLines[i].split(",")[j])
                if j != len(inventoryLines[i].split(",")) - 1:
                   newInventoryLine += ","

            inventoryLines[i] = newInventoryLine
            inventoryItemsFile.seek(0)
            inventoryItemsFile.truncate()
            inventoryItemsFile.writelines(inventoryLines)

    dateReceived = date + datetime.timedelta(days=3)
    line = f"{dateOrdered}, {itemsInOrder}, {cost}, {dateReceived}\n"
    restockOrdersFileCSV.write(line)
    line = "INSERT INTO \"RestockOrders\" (\"DateOrdered\", \"DateReceived\", \"Items\", \"Cost\") VALUES ('" + str(dateOrdered) + "', '" + str(dateReceived) + "', ARRAY" + str(itemsInOrder) + ", " + str(cost) + ");\n"
    restockOrdersFile.write(line)
    
    inventoryItemsFile.close()

def generateZReport(date, zReportsFile, dailyTotal):
    line = "INSERT INTO \"ZReports\" (\"DateTimeGenerated\", \"Subtotal\", \"Total\") VALUES ('" + str(date) + "', " + str(dailyTotal) + ", " + str(dailyTotal * 1.0825) + ");\n"
    zReportsFile.write(line)

generateHistory()

# generateMenuTable()
# generateInventoryItems()