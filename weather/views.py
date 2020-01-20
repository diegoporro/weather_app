import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
import time
from datetime import datetime


def index(request):
    year = datetime.now().year
    print(year)
    localtime = time.asctime(time.localtime(time.time()))
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=07484c8f08c5e67afd6b4e26108f5d5d'
    r = requests.get(url.format('Caracas')).json()
    random_ico = {
                'city': 'Caracas',
                'icon': r['weather'][0]['icon'],
            }

    print(r)
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
                'city': city.name,
                'country': r['sys']['country'],
                'temperature': r['main']['temp'],
                'temp_min': r['main']['temp_min'],
                'temp_max': r['main']['temp_max'],
                'humidity': r['main']['humidity'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
            }

        weather_data.append(city_weather)

    print(weather_data)

    context = {'weather_data': weather_data, 'form': form, 'localtime': localtime, 'year': year, 'random_ico': random_ico,}

    return render(request, 'weather/weather.html', context)
