# The following website contains weather information for a given location (website).
# a. Implement a “.py” script that uses both requests and Beautiful Soup libraries to extract
# all information of this page under section “Detailed Forecast”, storing it as a “. json”
# file (feel free to extract additional information that you may find relevant).

import json
import requests
import sys
from bs4 import BeautifulSoup
import os

file_dir = os.path.dirname(sys.argv[0])

def get_weather_data():
    url = 'https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    forecast = soup.find(id='detailed-forecast')
    data = {}
    for day in forecast.find_all('div', class_='row-forecast'):
        daytxt = day.find('div', class_='col-sm-2 forecast-label').text
        data[daytxt] = day.find('div', class_='col-sm-10 forecast-text').text
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
