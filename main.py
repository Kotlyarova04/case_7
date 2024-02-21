with open('filling_machines.txt', encoding='utf-8') as f1:
    filling_machines = {}
    for row in f1:
        machine = row.split()
        filling_machines[machine[0]] = (machine[1], list(machine[2:]))

petrol80, petrol92, petrol95, petrol98 = 43.0, 49.0, 52.5, 67.2
print(filling_machines)
