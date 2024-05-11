import requests
import datetime

while True:
    city_name = input("Please, enter city name: ")
    
    # city_name = 'Breda'
    # api for current weater
    url = (f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&'
           f'appid=548a48090e1be38d7e828325f094465b&units=metric')
    # api for 5 day every 3 hours forecast
    url_forcast = (f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&'
                   f'appid=548a48090e1be38d7e828325f094465b&units=metric')

    r = requests.get(url)
    rf = requests.get(url_forcast)
    wd = r.json()
    wfd = rf.json()
    if wd['cod'] == '404' or wfd['cod'] == '404':
        print("Invalid location! Please check your city name!")
        continue
    break

weather_view = wd['weather'][0]['description']

# use round() to make temp whole number to the closest one

temp = round(wd['main']['temp'])
feeling = round(wd['main']['feels_like'])
highest = round(wd['main']['temp_max'])
lowest = round(wd['main']['temp_min'])

# format the timestamp to datetime and adjusting the place of date and the place of time
sunrise_time = datetime.datetime.fromtimestamp(wd['sys']['sunrise']).strftime("%H:%M:%S %d/%m/%Y")
sunset_time = datetime.datetime.fromtimestamp(wd['sys']['sunset']).strftime("%H:%M:%S %d/%m/%Y")

# print(wfd['city'])
# # dict_keys(['cod', 'message', 'cnt', 'list', 'city'])

print(f"The weather in {city_name} is with {weather_view} and current temperature of {temp}°C ")
print(f"It feels like {feeling}°C")
print(f"Today's highest is {highest}°C and today's lowest is {lowest}°C")
print(f"Today the sunrise is at {sunrise_time}")
print(f"Today the sunset is at {sunset_time}")
