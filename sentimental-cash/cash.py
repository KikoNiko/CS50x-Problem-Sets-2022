# TODO
from cs50 import get_float


def main():

    cents = get_cents()
    coins = 0
    coin_list = [0.25, 0.10, 0.05, 0.01]

    for i in coin_list:
        while cents >= i:
            cents -= i
            coins += 1

    print(coins)


def get_cents():
    while True:
        try:
            cents = get_float("Change owed: ")
            if cents > 0:
                break
        except ValueError:
            print("Not a number")
    return cents


main()