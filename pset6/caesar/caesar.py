import sys

if (len(sys.argv) != 2):
    print("Give program a single numerical cipher!")
    exit(1)
else:
    cipher = int(sys.argv[1])
    text = input("plaintext:")
    print("ciphertext:", end="")
    for i in text:
        if i.isalpha():
            if i.islower():
                i = chr(((ord(i) - 97 + cipher) % 26) + 97)
            elif i.isupper():
                i = chr(((ord(i) - 65 + cipher) % 26) + 65)
        print(i, end='')
print()
