import requests, json

class Weather:
    temperature =''
    pressure = ''
    humidity = ''
    description = ''
    def __init__(self, temp, press, humid, desc) -> None:
        self.temperature = temp
        self.pressure = press
        self.humidity = humid
        desc = desc.capitalize()
        self.description = desc
        print(desc)

def GetWeather(): 
    api_key = "f865f5d50710787d96f3299c5b341fc1"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    city_name = "Kharkiv"

    units = "metric"
    lang = 'ru'
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units="+units +"&lang="+lang

    response = requests.get(complete_url)
    x = response.json()
    print(x)

    if x["cod"] != "404":
    
        y = x["main"]

        current_temperature = y["temp"]
    
        current_pressure = y["pressure"]

        current_humidity = y["humidity"]
    
        z = x["weather"]
        weather_description = z[0]["description"]
    
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) +
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidity) +
            "\n description = " +
                        str(weather_description))
        return Weather(current_temperature,current_pressure,current_humidity,weather_description)
    
 