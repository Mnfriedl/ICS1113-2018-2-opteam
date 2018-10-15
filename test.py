M = 0
H = 0
with open('volunteers.csv', 'r') as f:
    for line in f.readlines():
        line = line.strip()
        data = line.split(',')
        if data[1] == '0':
            H += 1
        elif data[1] == '1':
            M += 1
print(H)
print(M)
