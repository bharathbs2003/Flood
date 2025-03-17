# import requests
# import datetime

# def get_data(date, month, year, days, location):
#     a = datetime.date(year, month, date)
#     b = a - datetime.timedelta(days)
    
#     k = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?&aggregateHours=" + str(24 * days) + "&startDateTime=" + str(b) + "T00:00:00&endDateTime=" + str(a) + "T00:00:00&unitGroup=uk&contentType=json&dayStartTime=0:0:00&dayEndTime=0:0:00&location=" + location + ",India&key=29VR6BSVRWYP3RFQFK9LZQNVC"
#     x = requests.get(k).json()['locations']
    
#     for i in x:
#         y = x[i]

#     y = y['values'][0]
#     final = [y['temp'], y['maxt'], y['wspd'], y['cloudcover'], y['precip'], y['humidity'], y['precipcover']]

#     return final

# states = ['Karnataka', 'Gujarat', 'Rajasthan', 'Maharashtra', 'Madhya Pradesh']
# import csv
# import random
# f = open('data1.csv', mode='w', newline = '')
# writer = csv.writer(f, delimiter=',')


# for i in states:
#     for j in range(1, 31):
#         a = random.randint(1, 28)
#         b = random.randint(1, 12)
#         c = random.randint(2013, 2019)

#         k = get_data(a, b, c, 15, i)

#         if k[4] != None:
#             if k[4] < 20:
#                 print(k)
#                 print(j)
#                 writer.writerow(k + [0])



# def extract_date(x):
#     k = x.split(" ")

#     a = int(k[0])

#     d = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}
#     b = d[k[1][0:len(k[1]) - 1].lower()]

#     c = int(k[2])

#     return [a, b, c]

# def process(k):
#     x = extract_date(k[1])

#     return get_data(x[0], x[1], x[2], 15, k[0])


# f = open('data.csv', mode='w', newline = '')
# writer = csv.writer(f, delimiter=',')

# with open('mined.csv', mode='r') as csv_file:
#     csv_reader = csv.reader(csv_file)
    
#     for row in csv_reader:
#         print(row)
        
#         writer.writerow(process(row) + [1])

import requests
import datetime
import csv
import random

# Dictionary for Indian states with approximate latitude and longitude
state_coordinates = {
    'Karnataka': (15.3173, 75.7139),
    'Gujarat': (22.2587, 71.1924),
    'Rajasthan': (27.0238, 74.2179),
    'Maharashtra': (19.7515, 75.7139),
    'Madhya Pradesh': (23.4733, 77.9479)
}

def get_data(date, month, year, days, latitude, longitude):
    end_date = datetime.date(year, month, date)  
    start_date = end_date - datetime.timedelta(days=days)

    # Converting date to "YYYY-MM-DD" format
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,cloud_cover_mean,relative_humidity_2m_max&temperature_unit=celsius&wind_speed_unit=kmh&precipitation_unit=mm&timezone=Asia/Kolkata"
    
    response = requests.get(url)
    data = response.json()
    
    if "error" in data:
        print("Error:", data["reason"])
        return None

    # Extracting weather values (only using the last day's data)
    y = data['daily']
    final = [
        y['temperature_2m_max'][-1],  # Max Temperature
        y['temperature_2m_min'][-1],  # Min Temperature
        y['wind_speed_10m_max'][-1],  # Wind Speed
        y['precipitation_sum'][-1],   # Total Precipitation
        y['cloud_cover_mean'][-1],    # Cloud Cover
        y['relative_humidity_2m_max'][-1]  # Humidity
    ]

    return final

# Creating CSV file
with open('data1.csv', mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    
    for state, coords in state_coordinates.items():
        latitude, longitude = coords
        
        for j in range(1, 31):
            a = random.randint(1, 28)
            b = random.randint(1, 12)
            c = random.randint(2013, 2019)

            k = get_data(a, b, c, 15, latitude, longitude)

            if k and k[3] is not None:  # Ensure precipitation data is valid
                if k[3] < 20:
                    print(f"{state} - Data: {k} (Day {j})")
                    writer.writerow(k + [0])

# Processing existing mined data
def extract_date(x):
    k = x.split(" ")
    a = int(k[0])

    d = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 
         'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
    
    b = d[k[1][0:len(k[1]) - 1].lower()]
    c = int(k[2])

    return [a, b, c]

def process(k):
    x = extract_date(k[1])
    state = k[0]

    if state in state_coordinates:
        latitude, longitude = state_coordinates[state]
        return get_data(x[0], x[1], x[2], 15, latitude, longitude)
    return None

# Processing mined.csv and writing output to data.csv
with open('data.csv', mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=',')

    with open('mined.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            print("Processing row:", row)
            
            processed_data = process(row)
            if processed_data:
                writer.writerow(processed_data + [1])
