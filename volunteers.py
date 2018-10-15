import random
import csv
import math

MIN_VOLS = 270
MAX_VOLS = 315
TOTAL_VOLS = 200

LOCATIONS = 9

WOMEN_RATE = 0.55
CAREERS = 40*[1] + 25*[2] + 15*[3] + 20*[4] + 10*[5]
TASKS = 5
GENDER = math.floor(WOMEN_RATE*TOTAL_VOLS)*[1] + math.ceil((1-WOMEN_RATE)*TOTAL_VOLS)*[0]

VOLS = []
for i in range(TOTAL_VOLS):
    volunteer = {
        'gender': GENDER.pop(random.randint(0, len(GENDER) - 1)),
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

max_min_vol = TOTAL_VOLS//(LOCATIONS*TASKS)

with open('tasks_per_location.csv', 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['location'] + ['min_vols_task_%d' % (i+1) for i in range(TASKS)])
    for i in range(LOCATIONS):
        min_tasks = []
        for j in range(TASKS):
            min_tasks.append(random.randint(max(0, max_min_vol - 3),max(1, max_min_vol)))
        csv_writer.writerow([i+1] + min_tasks)
    

