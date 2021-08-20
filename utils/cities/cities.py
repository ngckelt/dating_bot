import json


def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def check_city(user_city: str):
    response = {'equal': False, 'candidate': None}
    with open('utils/cities/russian-cities.json') as f:
        cities = json.loads(f.read())
    user_city = user_city.capitalize()
    for city in cities:
        delta = levenshtein(user_city, city['name'])
        if delta == 0:
            response['equal'] = True
            break
    for city in cities:
        delta = levenshtein(user_city, city['name'])
        if 0 < delta <= 2:
            response['candidate'] = city['name']
            break
    return response





