import json


M = 0
H = 0
volunteers = []
with open('volunteers.csv', 'r') as f:
    f.readline()
    for line in f.readlines():
        line = line.strip()
        data = line.split(',')
        volunteers.append({
            "gender": data[1]
        })
        if data[1] == '0':
            H += 1
        elif data[1] == '1':
            M += 1

with open('results.json', 'r') as f:
    results = json.load(f)

for key, value in results['X'].items():
    keys = key.strip('()').split(',')
    volunteer = int(keys[0])
    if value == 1:
        print(key)
        volunteers[volunteer]['community'] = keys[1].strip(' \'')

print(json.dumps(volunteers, indent=2))
coms = [x["community"] for x in volunteers]
communities = set(coms)
for c in communities:
    print(c)
    print('Voluntarios', coms.count(c))
    # print('Mujeres', len([x for x in volunteers if x["community"] == c and x['gender'] == '1']))


for key, value in results["J"].items():
    print(key, value)