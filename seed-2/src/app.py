def average(xs):
    return sum(xs) / len(xs)


def last_index(xs):
    return len(xs)


def main():
    print(average([1, 2, 3]), last_index([1, 2, 3]))


if __name__ == "__main__":
    main()
