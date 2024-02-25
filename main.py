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


def cl_key(arr):
    first_concatenation = str(arr[0])[-8:-3] + ' ' + arr[-1] + ' '
    second_concatenation = first_concatenation + arr[1] + ' ' + arr[2]
    return second_concatenation


def sort_dict(some_dict):
    tup_sequence = some_dict.items()
    tup_seq_sorted = sorted(tup_sequence, key=lambda x: x[1][0])
    result = dict(tup_seq_sorted)
    return result


with open('filling_machines.txt', encoding='utf-8') as f1:
    filling_machines = {}
    for row in f1:
        machine = row.split()
        filling_machines['Machine' + ' ' + machine[0]] = (int(machine[1]), list(machine[2:]))

petrol80, petrol92, petrol95, petrol98 = 43.0, 49.0, 52.5, 67.2
free_places = {}
queue = {}
departure_times = {}
for m_object in filling_machines.items():
    free_places[m_object[0]] = m_object[1][0]
    queue[m_object[0]] = 0

with open('input.txt', encoding='utf-8') as f2:
    for row in f2:
        raw_request = row.split()
        concatenation = str(datetime.date.today()) + ' ' + raw_request[0]
        raw_request[0] = str(datetime.datetime.strptime(concatenation, '%Y-%m-%d %H:%M'))
        raw_request.insert(2, str(calculate(raw_request[1])))
        delta = datetime.timedelta(minutes=int(raw_request[2]))
        raw_request.insert(3, str(datetime.datetime.strptime(concatenation, '%Y-%m-%d %H:%M') + delta))
        client_key = cl_key(raw_request)
        departure_times = sort_dict(departure_times)

        for key in departure_times:
            datetime_obj_departure = datetime.datetime.strptime(departure_times[key][0], '%Y-%m-%d %H:%M:%S')
            datetime_obj_new = datetime.datetime.strptime(raw_request[0], '%Y-%m-%d %H:%M:%S')
            if datetime_obj_departure <= datetime_obj_new:
                free_places[departure_times[key][1]] += 1
                queue[departure_times[key][1]] -= 1
                obj_for_print = departure_times[key][0][-8:-3]
                print(f'В {obj_for_print} клиент {key} заправил свой автомобиль и покинул АЗС.')
                for i in filling_machines:
                    print(f'Автомат №{i[-1]} максимальная очередь: {filling_machines[i][0]} Марки бензина: {" ".join(filling_machines[i][1])} ->{"*" * queue[i]}')
                departure_times = dict(list(departure_times.items())[1:])
            else:
                break

        machines = []
        min_queue = []
        for m_object in filling_machines.items():
            if raw_request[4] in m_object[1][1]:
                machines.append(m_object[0])

        min_value = float('inf')
        for m_number in machines:
            if queue[m_number] < min_value and free_places[m_number] > 0:
                min_value = queue[m_number]
        if min_value == float('inf'):
            min_queue = machines
        for m_number in machines:
            if queue[m_number] == min_value:
                min_queue.append(m_number)

        for m_number in min_queue:
            if free_places[m_number] > 0:
                free_places[m_number] -= 1
                queue[m_number] += 1
                departure_times[client_key] = [raw_request[3], m_number]
                print(f'В {row.split()[0]} новый клиент: {client_key} встал в очередь к автомату №{m_number[-1]}')
                for i in filling_machines:
                    print(f'Автомат №{i[-1]} максимальная очередь: {filling_machines[i][0]} Марки бензина: {" ".join(filling_machines[i][1])} ->{"*" * queue[i]}')
                break
            else:
                continue

        min_queue.clear()
        machines.clear()
