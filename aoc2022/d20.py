key = 811589153
with open("d20.txt") as fp:
    numbers = [int(line) for line in fp]
# numbers = [1, 2, -3, 3, -2, 0, 4]
numbers = [key * num for num in numbers]
n = len(numbers)
positions = list(range(n))
indexes = list(range(n))
# positions[i]: where in numbers is the i'th input number currently
# indexes[i]: where in the input is numbers[i]

def exch(i, j):
    # exch(i, j): exchange numbers[i] and numbers[j] and update positions,indexes as well
    positions[indexes[i]], positions[indexes[j]] = positions[indexes[j]], positions[indexes[i]]
    indexes[i], indexes[j] = indexes[j], indexes[i]
    numbers[i], numbers[j] = numbers[j], numbers[i]

print(numbers)
print1 = n < 10 and False
for _ in range(10):
    for i in range(n):
        if n >= 10 and i % 100 == 0:
            print(_, i, n)
        position = positions[i]
        v = numbers[position] % (n - 1)
        if v == 0:
            if print1:
                print(numbers[position], "does not move")
                print(numbers)
            continue
        if position + v >= n:
            v = v - (n - 1)
        elif position + v < 0:
            v = v + n
        if v > 0:
            if print1:
                print(numbers[position], "moves", v, "places right")
            for j in range(v):
                next_position = position + 1
                assert next_position < n
                exch(position, next_position)
                position = next_position
        elif v < 0:
            if print1:
                print(numbers[position], "moves", -v, "places left")
            for j in range(-v):
                next_position = position - 1
                assert next_position >= 0
                exch(position, next_position)
                position = next_position
        if print1:
            print(numbers)
    if n < 10:
        print(numbers)
    i = numbers.index(0)
    print(
            numbers[(i + 1000) % n]
            , numbers[(i + 2000) % n]
            , numbers[(i + 3000) % n]
            )
