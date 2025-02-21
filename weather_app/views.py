from django.shortcuts import render,HttpResponse,redirect
import requests
from django.http import JsonResponse
from . models import City
# Create your views here.

def home(request):

    #Define API key and base url of OpenWeatherMap
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
    API_KEY = "0dd6738336e74cfbb8e6241eebe487e9"
    
    
    #Check if the request is a POST (when adding a new city)
    
    if request.method=="POST":
        #Get the city name from the form
        city_name =request.POST.get('city')
        #Fecth weather data for the city from the API
        response = requests.get(url.format(city_name,API_KEY)).json()
        
        #Check if the city exist in the API
        if response['cod'] == 200:
            #Save the new city to the database
            City.objects.create(name = city_name)
        
        return redirect('home')
    #Fetch weather data for all the city 
    weather_data=[]
    try:
        cities = City.objects.all()#get all city from the database
        for city in cities:
            response = requests.get(url.format(city.name,API_KEY))
            data = response.json()
            if data['cod']==200:
                city_weather ={
                    'city':city.name,
                    'temperature':data['main']['temp'],
                    'descrition':data['weather'][0]['description'],
                    'icon':data['weather'][0]['icon']
                }   
                weather_data.append(city_weather) 
            else:
                City.objects.filter(name=city.name).delete()
                
    except requests.RequestException as e:
        print("Error connecting to weather data service,Please try again later on")
        
    context ={'weather_data':weather_data}
    
    return render(request,'index.html',context)

#get name response['name']
#get temperature response['main]['temp']
#get description response['weather'][0]['description']
#get icon response['weather'][0]['icon']