import json
from collections import defaultdict

with open('results.json', 'r') as file:
    variables = json.load(file)

W = variables['W']

locations = defaultdict(lambda: defaultdict(lambda: 0))

for i in W:
    newstr = i.replace('(', '').replace(')', '').replace("'", '').split(',')
    if W[i] == 1:
        locations[newstr[2]][newstr[1]] += 1

for i in locations:
    print("{}: {}".format(i, locations[i]))
