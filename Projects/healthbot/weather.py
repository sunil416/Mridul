#from bothealth.logger import logging
#from bothealth.exception.exception import AppException
import pyowm

class WeatherData:
    def __init__(self):
        self.owmapikey = '7ef2b110894b07745af0d96d1e7bd786'
        self.owm = pyowm.OWM(self.owmapikey)
        self.mgr = self.owm.weather_manager()

    def processRequest(self, req):
        try:
            result = req.get("queryResult")
            parameters = result.get("parameters")
            
            # FIX: use geo-city (or geo-state if needed)
            city = parameters.get("geo-city")
            if not city:
                raise ValueError("City not found in request parameters")

            # New API call
            observation = self.mgr.weather_at_place(city)
            w = observation.weather

            # Weather details
            wind_speed = str(w.wind().get('speed'))
            humidity = str(w.humidity)
            temp = w.temperature('celsius')
            temp_min_celsius = str(temp.get('temp_min'))
            temp_max_celsius = str(temp.get('temp_max'))

            speech = (
                f"Today's weather in {city}: "
                f"Humidity: {humidity}, "
                f"Wind Speed: {wind_speed}, "
                f"Minimum temperature: {temp_min_celsius}°C, "
                f"Maximum temperature: {temp_max_celsius}°C."
            )

        except Exception as e:
            speech = f"Sorry, I couldn't fetch the weather due to: {str(e)}"

        return {
            "fulfillmentText": speech,
            "displayText": speech
        }

