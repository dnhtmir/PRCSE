# The following website contains weather information for a given location (website).
# a. Implement a “.py” script that uses both requests and Beautiful Soup libraries to extract
# all information of this page under section “Detailed Forecast”, storing it as a “. json”
# file (feel free to extract additional information that you may find relevant).
# c. As an optional exercise, parse the degrees from °F to ºC and windspeed from mph to
# km/h. Additionally, make the first script (a.) configurable to fetch weather data from
# other locations. Similarly, adjust the second script (b.) so that users can query for
# weather data of all the supported locations

import json
import re
import requests
import sys
from bs4 import BeautifulSoup
import os

file_dir = os.path.dirname(sys.argv[0])

def fahrenheit_to_celsius(fahrenheit):
    celsius = (5/9) * (fahrenheit - 32)
    return celsius

def mph_to_kph(mph):
    return mph * 1.6

def get_weather_data():
    url = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forecast = soup.find(id='detailed-forecast')
    data = {}
    for day in forecast.find_all('div', class_='row-forecast'):
        daytxt = day.find('div', class_='col-sm-2 forecast-label').text
        desc = day.find('div', class_='col-sm-10 forecast-text').text
        index = 0
        phrase = []
        while True:
            i = desc[index::].strip().find('.')
            phrase.append(desc[index:i])
            index = i + 1
            if index != 0:
                break

        if len(phrase) >= 1:
            fahr = re.findall(r'\d+', phrase[0])
            cels = str(fahrenheit_to_celsius(float(fahr)))
            phrase[0].replace(fahr, cels)
        
        if len(phrase) >= 2:
            mph = re.findall(r'\d+', phrase[1])
            kph = str(mph_to_kph(float(fahr)))
            phrase[1].replace(mph, kph)


        data[daytxt] = desc
    return data

def save_weather_data(data, location):
    dir_name = os.path.join(file_dir, 'ex11_test_artifacts')
    os.makedirs(dir_name, exist_ok=True)
    with open(os.path.join(dir_name, location + '.json'), 'w') as file:
        json.dump(data, file, indent=4)
    
def main():
    location = 'SanFrancisco'
    data = get_weather_data()
    save_weather_data(data, location)

if __name__ == '__main__':
    if len(sys.argv) != 1:
        sys.exit("usage: " + sys.argv[0])
    main()
