from django.shortcuts import render
import os
import requests

def get_weather(request):
    error_message = ''

    if request.method == 'POST':
        location = request.POST.get('location', '')

        # Get the path to the 'api_key.txt' file
        api_key_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'api_key.txt'))

        try:
            # Open the file using the absolute path
            api_key = open(api_key_path, 'r').read()
        except FileNotFoundError:
            # Handle the case where the file is not found
            error_message = "API key file not found. Please check the file path."
            return render(request, 'index.html', {'error_message': error_message})

        result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}')

        if result.status_code != 200:
            # Handle unsuccessful cases
            error_message = "Invalid Location"
        elif result.json()['cod'] == "404":
            # Handle not found locations
            error_message = "Please enter a valid location"
        else:
            description = result.json()['weather'][0]['description']
            temperature = float((result.json()['main']['temp']) - 273.15) * 9/5 + 32
            temp_min = float((result.json()['main']['temp_min']) - 273.15) * 9/5 + 32
            temp_max = float((result.json()['main']['temp_max']) - 273.15) * 9/5 + 32
            city = result.json()['name']
            country = result.json()['sys']['country']

            context = {'temperature': temperature, 'description': description, 'temp_min': temp_min, 'temp_max': temp_max, 'city': city, 'country': country}
            print(result.json())
            return render(request, 'result.html', context)

    return render(request, 'index.html', {'error_message': error_message})

def index(request):
    return render(request, 'index.html')

def result(request):
    return render(request, 'result.html', {'result_data': 'Placeholder Result Data'})