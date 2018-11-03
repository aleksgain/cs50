while True:
    try:
        height = int(input("Height:"))
        if type(height) == int and height >= 0 and height < 24:
            break
    except:
        continue
for h in range(1, height+1):
    print(" " * (height-h), "#" * h, "  ", "#" * h, sep="")