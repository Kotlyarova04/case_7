import datetime

with open('filling_machines.txt', encoding='utf-8') as f1:
    filling_machines = {}
    for row in f1:
        machine = row.split()
        filling_machines[machine[0]] = (int(machine[1]), list(machine[2:]))

petrol80, petrol92, petrol95, petrol98 = 43.0, 49.0, 52.5, 67.2
free_places = [i[0] for i in list(filling_machines.values())]
# print(free_places)

with open('input.txt', encoding='utf-8') as f2:
    for row in f2:
        raw_request = row.split()
        concatenation = str(datetime.date.today()) + ' ' + raw_request[0]
        # print(concatenation)
        raw_request[0] = str(datetime.datetime.strptime(concatenation, '%Y-%m-%d %H:%M'))       # str вероятно уберем, когда перейдем к расчетам
        # print(raw_request)
