while True:
    try:
        change = float(input("Change owed:"))
        if type(change) == float and change > 0.009:
            change = round(change*100)
            break
    except:
        continue
counter = 0
coins = [25, 10, 5, 1]
while change > 0:
    for i in coins:
        while change - i >= 0:
            change -= i
            counter += 1
print(counter)

