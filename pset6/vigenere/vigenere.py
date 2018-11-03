import sys

if (len(sys.argv) != 2) or sys.argv[1].isalpha() == False:
    print("Give program a single keyword for cipher!")
    exit(1)
else:
    keyword = sys.argv[1]
    text = input("plaintext:")
    print("ciphertext:", end="")
    k = 0
    for i in text:
        if (k == len(keyword)):
            k = 0
        if i.isalpha():
            # get shift to convert from acsii to alphabetical order
            if i.islower():
                shift = 97
            elif i.isupper():
                shift = 65
        # character((ascii value - shift + cypher in lowercase) modulo 26 to get alpabetical order value) + shift to get back to ascii)
            i = chr(((ord(i) - shift + (ord(keyword[k].lower()) - 97) % 26) % 26) + shift)
            k += 1
        print(i, end='')
print()
