n = int(input())     # n (1 ≤ n ≤ 100)

for i in range(1, n + 1):
    print(" " * (n - i), '*' * (i - 1), "|", "*" * (i - 1))
