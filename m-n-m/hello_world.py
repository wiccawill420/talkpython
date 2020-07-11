print("Hello world")
print("Odd/Even number checker")
check_request = 1
while check_request != 0:
    check_request = int(input("Number to check? "))
    if check_request % 2 == 0:
        print("Even")
    else:
        print("Odd")
print("bye")
