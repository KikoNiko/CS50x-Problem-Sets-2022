# TODO

while True:
    try:
        h = int(input("Height: "))
        if h > 0 and h < 9:
            break
        else:
            print("Please enter a number between 1 and 8")
    except ValueError:
        print("Not an integer")

for i in range(0, h, 1):
    print((" " * (h-i-1) + "#" * (i+1)))
    