import random
import datetime

list_check = []
four_digit = 10000
for _ in range(four_digit):
    list_check.append(True)
short = ["AC", "TS", "WS", "AA", "DL", "UA"]
cities = ["Ottawa", "Montreal", "Quebec City", "Halifax", "Winnipeg", "Edmonton", "Calgary", "Vancouver", "Detroit",
          "Philadelphia", "New York", "Washington", "Boston", "Chicago", "Atlanta", "Houston", "Las Vegas",
          "Los Angeles", "San Francisco", "Miami", "Phoenix", "San Antonio"]
companies = {"AC": "Air Canada", "TS": "Air Transat", "WS": "WestJet", "AA": "American Airlines",
             "DL": "Delta Airlines", "UA": "United Airlines"}
models = ["A318", "A319", "A320", "A321", "A330", "A350", "A380", "B737", "B747", "B757", "B767", "B777", "B787"]
flights = []
today = datetime.datetime.today()
time = [today.year, today.month, today.day, today.hour, today.minute]
data = {"Ottawa": (352, (59, 68), (814, 467)),
        "Montreal": (501, (70, 87), (835, 455)),
        "Quebec City": (731, (90, 101), (848, 438)),
        "Halifax": (1266, (123, 125), (882, 459)),
        "Winnipeg": (1904, (154, 158), (712, 434)),
        "Edmonton": (2708, (247, 250), (645, 397)),
        "Calgary": (2713, (250, 260), (637, 409)),
        "Vancouver": (3363, (288, 310), (589, 412)),
        "Detroit": (344, (69, 88), (786, 493)),
        "Philadelphia": (541, (88, 103), (832, 498)),
        "New York": (551, (98, 112), (836, 501)),
        "Washington": (564, (82, 101), (823, 515)),
        "Boston": (692, (92, 116), (850, 482)),
        "Chicago": (702, (107, 124), (759, 499)),
        "Atlanta": (1185, (131, 144), (784, 563)),
        "Houston": (2097, (204, 218), (707, 593)),
        "Las Vegas": (3138, (284, 290), (596, 517)),
        "Los Angeles": (3498, (310, 333), (568, 529)),
        "San Francisco": (3648, (321, 337), (559, 500)),
        "Miami": (1986, (184, 204), (812, 626)),
        "Phoenix": (3013, (260, 280), (613, 540)),
        "San Antonio": (2319, (205, 225), (673, 585))}


def flight_number():
    start = random.choice(short)
    start1 = start
    loop = True
    while loop:
        min_s = 0
        max_s = 9
        a = random.randint(min_s, max_s)
        b = random.randint(min_s, max_s)
        c = random.randint(min_s, max_s)
        if a == 0 and b == 0 and c == 0:
            d = random.randint(min_s+1, max_s)  # make sure no flight's number is 0000
        else:
            d = random.randint(min_s, max_s)
        if list_check[a*1000+b*100+c*10+d]:
            loop = False
            start += (str(a)+str(b)+str(c)+str(d))
            list_check[a*1000+b*100+c*10+d] = False
    return [start, start1]


def final_generate():
    minutes_in_day = 1440
    real = flight_number()
    number = real[0]
    company = companies[real[1]]
    destination = random.choice(cities)
    departure1 = random.randint(0, minutes_in_day-1)
    arrival1 = departure1 + random.randint(data[destination][1][0], data[destination][1][1])
    three_hours = 180
    departure2 = (arrival1 + three_hours) % minutes_in_day
    arrival2 = (departure2 + arrival1 - departure1) % minutes_in_day
    model = random.choice(models)
    min_minutes = 20
    for s in flights:
        if s[3] == destination and abs(s[4] - departure1) <= min_minutes:
            return False  # checks if two flights going to same destination would be way too close in terms of time
    flights.append([number, company, "Toronto", destination, departure1, arrival1, model])  # leaving Toronto
    flights.append([number, company, destination, "Toronto", departure2, arrival2, model])  # coming back to Toronto
    return True


number_of_flights = 500
for _ in range(number_of_flights):
    while not final_generate():
        final_generate()


def pos_cities(keyword):
    first = keyword.title()
    second = keyword.lower()
    out = []
    for s in cities:
        if first in s:
            out.append(s)
        elif second in s:
            out.append(s)
    return out


def direct(flight):
    results = []
    length = len(flight)
    for i in flights:
        partial = i[0][:length]
        if partial == flight:
            results.append(i)
    return results


def real_time():
    minutes = 60
    hours = 24
    days = 30
    months = 12
    m1 = [1, 3, 5, 7, 8, 10, 12]
    m2 = [4, 6, 9, 11]
    for item in range(len(time)):
        time[item] = int(time[item])
    time[4] += 1
    if time[4] >= minutes:
        time[3] += 1
        time[4] = 0
    if time[3] >= hours:
        time[2] += 1
        time[3] = 0
    if (time[1] == 2 and time[2] >= days) or (time[1] in m1 and time[2] > days) or (time[1] in m2 and time[2] > days+1):
        time[1] += 1
        time[2] = 0
    if time[1] > months:
        time[0] += 1
    for i in range(1, len(time)):
        time[i] = str(time[i]).rjust(2, "0")
    first = '-'.join([str(time[0]), str(time[1]), str(time[2])])
    second = ':'.join([str(time[3]), str(time[4])])
    return first + " " + second


def big_board(time1):
    dep = []
    arr = []
    final = []
    board_size = 10
    flights.sort(key=lambda x: x[4])
    for i in range(len(flights)):
        if flights[i][4] >= time1 and flights[i][3] != "Toronto":
            for j in range(i+1, i+len(flights)+1):
                j %= len(flights)
                if flights[j][3] != "Toronto":
                    dep.append(flights[j])
                if len(dep) == board_size:
                    break
            break
    for i in range(len(flights)):
        if flights[i][4] >= time1 and flights[i][3] == "Toronto":
            for j in range(i+1, i+len(flights)+1):
                j %= len(flights)
                if flights[j][3] == "Toronto":
                    arr.append(flights[j])
                if len(arr) == board_size:
                    break
            break
    for i in range(min(len(dep), len(arr))):
        final.append([dep[i], arr[i]])
    return final
