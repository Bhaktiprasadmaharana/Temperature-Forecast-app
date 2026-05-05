from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# View function for the homepage
def home(request):
    # Check if city is submitted via POST request, otherwise default to 'indore'
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    # Base URL to fetch weather data for the given city (you need to append your API key)
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=baafccb3e69024262ef620f3b229ad8b'
    
    # Parameters to request temperature in metric units (Celsius)
    PARAMS = {'units': 'metric'}

    # Your Google Custom Search API Key (keep it secret)
    API_KEY = 'AIzaSyCRjmHoXXEtEcI62o7hiJFGdxFYWbZ0H4c'

    # Your Google Custom Search Engine ID
    SEARCH_ENGINE_ID = '176295dedf9e94fd2'

    # Prepare query to fetch city-related image from Google Images
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    
    # Final URL to call Google Custom Search for images
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Send request and parse JSON response to get image URL
    try:
        response = requests.get(city_url)
        data = response.json()
        search_items = data.get("items")
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        elif search_items and len(search_items) > 0:
            image_url = search_items[0]['link']
        else:
            image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
    except Exception:
        image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'

    try:
        # Try fetching weather data from OpenWeather API
        data = requests.get(url, params=PARAMS).json()

        # Extract useful weather info from response
        description = data['weather'][0]['description']  # Weather description (e.g., clear sky)
        icon = data['weather'][0]['icon']  # Icon code for weather
        temp = data['main']['temp']  # Temperature
        day = datetime.date.today()  # Get current date

        # Pass all data to template and render HTML
        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except (KeyError, IndexError, Exception):
        # If something goes wrong (like invalid city), show an error
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')

        # Render template with fallback (default) values
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred,
            'image_url': image_url
        })
