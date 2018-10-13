import random
import csv

MIN_VOLS = 67
MAX_VOLS = 93
CAREERS = 40*[1] + 25*[2] + 15*[3] + 20*[4] + 10*[5]
TASKS = 5
GENDER = 60*[0] + 40*[1] 

TOTAL_VOLS = random.randint(MIN_VOLS, MAX_VOLS)
VOLS = []
for i in range(TOTAL_VOLS):
    volunteer = {
        'gender': random.choice(GENDER),
        'career': random.choice(CAREERS),
        'habilities': []
    }
    for t in range(TASKS):
        volunteer['habilities'].append(random.normalvariate(5, 1))
    VOLS.append(volunteer)

with open('volunteers.csv', 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['volunteer_id', 'gender', 'career'] +
     ['hability_%d' % (i+1) for i in range(TASKS)])
    for i in range(TOTAL_VOLS):
        volunteer = VOLS[i]
        csv_writer.writerow([i, volunteer['gender'], volunteer['career']] + 
            [h for h in volunteer['habilities']])

