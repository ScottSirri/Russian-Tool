for i in range(1, int(720/(9*2))):
    if 720 % (9*i + 1) == 0:
        print(f"{9*i + 1}, ", end='')
print()
