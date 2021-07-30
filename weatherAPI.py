# importing requests and json
import requests, json
# base URL
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# city = search_by_city()
API_KEY = "f913d3af2769af8058e470383aff14db"

def search (city):
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
    # getting data in the json format
        data = response.json()
    # getting the main dict block
        main = data['main']
    # getting temperature
        temperature = main['temp']
    # getting the humidity
        humidity = main['humidity']
    # getting the pressure
        pressure = main['pressure']
    # weather report
        print(main)
#         print(f"{CITY:-^30}")
#         print(f"Temperature: {temperature}")
#         print(f"Humidity: {humidity}")
#         print(f"Pressure: {pressure}")
#         print(f"Weather Report: {report[0]['description']}")
        return main
    # updating the URL

# search('maplewood')