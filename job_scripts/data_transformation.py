def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def classify_weather(description):
    if 'rain' in description:
        return 'Rainy'
    elif 'clear' in description:
        return 'Clear'
    elif 'cloud' in description:
        return 'Cloudy'
    else:
        return 'Other'

def transform_weather_data(raw_data_list):
    transformed_data = []
    for raw_data in raw_data_list:
        transformed_entry = {
            "city": raw_data["name"],
            "temperature_celsius": round(kelvin_to_celsius(raw_data["main"]["temp"]), 2),
            "humidity": raw_data["main"]["humidity"],
            "pressure": raw_data["main"]["pressure"],
            "weather_description": raw_data["weather"][0]["description"],
            "weather_classification": classify_weather(raw_data["weather"][0]["description"]),
            "timestamp": raw_data["dt"]
        }
        transformed_data.append(transformed_entry)
    return transformed_data
