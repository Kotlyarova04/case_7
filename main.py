import datetime
import math
import random

with open('filling_machines.txt', encoding='utf-8') as f1:
    filling_machines = {}
    for row in f1:
        machine = row.split()
        filling_machines[machine[0]] = (int(machine[1]), list(machine[2:]))

petrol80, petrol92, petrol95, petrol98 = 43.0, 49.0, 52.5, 67.2
free_places = [i[0] for i in list(filling_machines.values())]
#print(free_places)

with open('input.txt', encoding='utf-8') as f2:
    petrols = []
    liters = []
    f22 = f2.readlines()
    for row in f22:
        raw_request = row.split()
        concatenation = str(datetime.date.today()) + ' ' + raw_request[0]
        # print(concatenation)
        raw_request[0] = str(datetime.datetime.strptime(concatenation, '%Y-%m-%d %H:%M'))       # str вероятно уберем, когда перейдем к расчетам
        petrols.append(raw_request[2])
        liters.append(raw_request[1])


def calculate(x):
    base_time = math.ceil(x/10)
    if base_time>1:
        variation = random.randint(-1,1)
        base_time += variation
    return base_time

base_t = []
for x in liters:
    base_t.append(calculate(int(x)))


cars = {}
for i in range(len(f22)):
    cars[i+1] = base_t[i]
#print(cars)

new_free = [0,0,0]
for j in range(len(cars)):
    if cars[j+1] > 0:
        cars[j+1] -= 1
    for i in petrols:
        if i == 'АИ-80':
            free_places[0] -= 1
            new_free[0] += 1
        if i == 'АИ-92':
            if free_places[2] > 0:
                if new_free[1] >= new_free[2]:
                    new_free[2] += 1
                    free_places[2] -= 1
                else:
                    new_free[1] += 1
                    free_places[1] -= 1
            else:
                new_free[1] += 1
                free_places[1] -= 1
        if i == 'АИ-95' or i == 'АИ-98':
            free_places[2] -= 1
            new_free[2] += 1