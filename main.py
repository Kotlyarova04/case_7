import datetime
import math
import random


def calculate(n_liters):
    n_liters = int(n_liters)
    base_time = math.ceil(n_liters / 10)
    if base_time > 1:
        variation = random.randint(-1, 1)
        base_time += variation
    return base_time


with open('filling_machines.txt', encoding='utf-8') as f1:
    filling_machines = {}
    for row in f1:
        machine = row.split()
        filling_machines['Machine' + ' ' + machine[0]] = (int(machine[1]), list(machine[2:]))
print(filling_machines)

petrol80, petrol92, petrol95, petrol98 = 43.0, 49.0, 52.5, 67.2
free_places = {}
queue = {}
for m_object in filling_machines.items():
    free_places[m_object[0]] = m_object[1][0]
    queue[m_object[0]] = 0
print(free_places)
print(queue)

with open('input.txt', encoding='utf-8') as f2:
    for row in f2:
        raw_request = row.split()
        concatenation = str(datetime.date.today()) + ' ' + raw_request[0]
        raw_request[0] = str(datetime.datetime.strptime(concatenation, '%Y-%m-%d %H:%M'))       # str вероятно уберем, когда перейдем к расчетам
        raw_request.insert(2, str(calculate(raw_request[1])))

        machines = []       # очищается после каждой итерации, список машин в которых есть нужный бензин
        min_queue = []      # очищается после каждой итерации, задуман как список таких элементов из списка machines, очередь к которым минимальна (но в одном сценарии не следует такой логике и тупо совпадает со списком machines, см. inf)
        for m_object in filling_machines.items():
            if raw_request[3] in m_object[1][1]:
                machines.append(m_object[0])
        print(machines, 'список machines')

        min_value = float('inf')
        for m_number in machines:
            if queue[m_number] < min_value and free_places[m_number] > 0:
                min_value = queue[m_number]
        if min_value == float('inf'):       # тогда и только тогда, когда все автоматы из machines заняты
            print(min_value)
            min_queue = machines        # ну типа, после_следующему циклу надо что-то перебирать (а раз все занято, то он один фиг переберет безрезультатно и пустит нас на следующую итерацию, после чего все очистится)
        for m_number in machines:
            if queue[m_number] == min_value:
                min_queue.append(m_number)

        for m_number in min_queue:
            if free_places[m_number] > 0:
                free_places[m_number] -= 1
                queue[m_number] += 1
                break
            else:
                continue

        print(min_queue, 'список min_queue')
        min_queue.clear()
        machines.clear()
        print(raw_request)
        print(f'Текущие очереди: {queue}')
        print(f'Текущие свободные места: {free_places}')
