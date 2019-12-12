import datetime 
print(datetime.datetime.now())
file = open("information.txt","a")
while True:
    amount = input("enter amount of people")
    time = datetime.datetime.now()
    wholeInformation = str(amount) +"---"+str(time)
    file.write(wholeInformation)
    if amount == "99":
        break
file.close