import datetime
import math
import random
import ru_local as ru


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

sold_liters = {'АИ-80': 0, 'АИ-92': 0, 'АИ-95': 0, 'АИ-98': 0}
clients_left = 0
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
        petrol_grade = raw_request[4]
        liters_sold = int(raw_request[1])

        for key in departure_times:
            datetime_obj_departure = datetime.datetime.strptime(departure_times[key][0], '%Y-%m-%d %H:%M:%S')
            datetime_obj_new = datetime.datetime.strptime(raw_request[0], '%Y-%m-%d %H:%M:%S')
            if datetime_obj_departure <= datetime_obj_new:
                free_places[departure_times[key][1]] += 1
                queue[departure_times[key][1]] -= 1
                obj_for_print = departure_times[key][0][-8:-3]
                print(ru.IN, obj_for_print, ru.CLIENT, key, ru.LEFT)
                for i in filling_machines:
                    print(ru.AUTOMAT, i[-1], ru.MAX_QUEUE, filling_machines[i][0], ru.PETROL, " ".join(filling_machines[i][1]), ' ->', "*" * queue[i], sep = '')
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
            clients_left += 1
            min_queue = machines
            print(ru.IN, row.split()[0], ru.NEW, ru.CLIENT, client_key, ru.NOT_STAY)
            for i in filling_machines:
                print(ru.AUTOMAT, i[-1], ru.MAX_QUEUE, filling_machines[i][0], ru.PETROL, " ".join(filling_machines[i][1]), ' ->', "*" * queue[i], sep = '')
        for m_number in machines:
            if queue[m_number] == min_value:
                min_queue.append(m_number)
        for m_number in min_queue:
            if free_places[m_number] > 0:
                free_places[m_number] -= 1
                queue[m_number] += 1
                departure_times[client_key] = [raw_request[3], m_number]
                sold_liters[petrol_grade] += liters_sold
                print(ru.IN, row.split()[0], ru.NEW, ru.CLIENT, client_key, ru.STAY, m_number[-1], sep = '')
                for i in filling_machines:
                    print(ru.AUTOMAT, i[-1], ru.MAX_QUEUE, filling_machines[i][0], ru.PETROL, " ".join(filling_machines[i][1]), ' ->', "*" * queue[i], sep = '')
                break
            else:
                continue

        min_queue.clear()
        machines.clear()

    departure_times = sort_dict(departure_times)
    for key in departure_times:
        free_places[departure_times[key][1]] += 1
        queue[departure_times[key][1]] -= 1
        obj_for_print = departure_times[key][0][-8:-3]
        print(ru.IN, obj_for_print, ru.CLIENT, key, ru.LEFT)
        for i in filling_machines:
            print(ru.AUTOMAT, i[-1], ru.MAX_QUEUE, filling_machines[i][0], ru.PETROL, " ".join(filling_machines[i][1]), ' ->', "*" * queue[i], sep = '')


total = 0
for petrol_grade, liters_sold in sold_liters.items():
    print(ru.NUMBER_LITERS, petrol_grade,':', liters_sold)
    if petrol_grade == 'АИ-80':
        total += liters_sold*petrol80
    if petrol_grade == 'АИ-92':
        total += liters_sold*petrol92
    if petrol_grade == 'АИ-95':
        total += liters_sold*petrol95
    if petrol_grade == 'АИ-98':
        total += liters_sold*petrol98

print(ru.TOTAL_PROFIT, total)
print(ru.AMOUNT_LEFT, clients_left)
