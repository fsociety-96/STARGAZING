# -*- coding: utf-8 -*-

import socket
import sys
import requests
import os
from dotenv import load_dotenv


load_dotenv()

air_quality_api         =   os.getenv("air_quality_api")
get_weather_api         =   os.getenv("get_weather_api") 
get_sunmooninfo_api     =   os.getenv("get_sunmooninfo_api")

def internet_check()->None:
    IPaddress = socket.gethostbyname(socket.gethostname())
    if IPaddress =="127.0.0.1":
        print("Please check your internet connnection :(")
        sys.exit(0)
        

def get_air_quality(city:str)->None:
    """
    Function to check the air quality.
    
    Parameters
    ----------
    city : str
        
    Returns
    -------
    None.
    
    """
    aqui = 0
    aqui_api        =   f"https://api.waqi.info/feed/{city}{air_quality_api}"
    request_check   =   requests.get(aqui_api)
    
    
    if (request_check.status_code) == 200:
        json_data   =   request_check.json()
        if json_data['status'] == 'ok':
            aqui    =   json_data['data']['aqi']
            if aqui == "-":
                print("Sorry, No data available, We are working on that.")
                sys.exit(0)
                
        else:
            print("Sorry, No data available, We are working on that.")
            sys.exit(0)
    else:
        print("Sorry, No data available, We are working on that ")
        sys.exit(0)
    
    print(f"Air quality data for {city.title()} : ")      
    if   aqui == 0:
        print(f"'aqui' = {aqui}\n,'Sorry, No data available, We are working on that' ",file = sys.stderr)
        sys.exit(0)
    elif aqui <= 50 :
        print(f"'aqui' = {aqui}\n'Excellent day for stargazing'")  
    elif aqui <= 100 : 
        print(f"'aqui' = {aqui}\n'Good day for stargazing'")
    elif aqui <= 150 :
        print(f"'aqui' = {aqui}\n'Lightly polluted air. Okay day for stargazing'")
    elif aqui <= 200 :
        print(f"'aqui' = {aqui}\n'Moderately polluted. Bad day for stargazing'")
    elif aqui <= 500:
        print(f"'aqui' = {aqui}\n'Extremely polluted. Worst day for stargazing'")
    elif aqui  > 500:
        print(f"'aqui' = {aqui}\n'Run for your life!'")   
        
def get_weather(city:str)->None:   
    """
    Function to get the weather data
    Refer https://openweathermap.org/current for JSON data format
    
    Parameters
    ----------
    city : str
        
    Returns
    -------
    None.

    """
    
    weather_api     =   f"https://api.openweathermap.org/data/2.5/weather?q={city}{get_weather_api}"        
    request_check   =   requests.get(weather_api)  
    print(f"\nToday's weather in {city.title()} :")
    
    if (request_check.status_code) == 200:
        json_data   =   request_check.json()
        if json_data['cod'] == '404':
            print("Sorry, No weather data available, We are working on that.",file=sys.stderr)
            sys.exit(0)
        else:
            weather     =   json_data['weather'][0]['main']
            description =   json_data['weather'][0]['description'].title()
            print(f"Weather     : {weather:10} \nDescription : {description:10}")
    else: 
        print("Sorry, No weather data available, We are working on that.",file=sys.stderr)
        sys.exit(0)

def get_sunmooninfo(city:str)->None:
    """
    This function get the timings of sun and moon.

    Parameters
    ----------
    city : str
        

    Returns
    -------
    None.

    """
    moon_api        =   f"https://api.ipgeolocation.io/astronomy?{get_sunmooninfo_api}{city}"
    request_check   =   requests.get(moon_api)
    print("\nTiming for Pune  : ")
    
    if (request_check.status_code)==200:
        json_data       = request_check.json()
        sunrise_time    = json_data['sunrise']
        sunset_time     = json_data['sunset']
        moonrise_time   = json_data['moonrise']
        moonset_time    = json_data['moonset'] 
        
        if int(sunrise_time[0:2]) > int(moonset_time[0:2]):
            print(f"Best time for the stargazing in the morning is {moonset_time} to {sunrise_time} ")
        
        print(f"Best time for the stargazing in the evening is {sunset_time} to {moonrise_time} ")    
    else:
        print("Sorry, No weather data available, We are working on that.",file=sys.stderr)
        sys.exit(0)


if __name__=="__main__":
    internet_check()
    city_name = input("Please enter an indian city name you want to go for stargazing : ").strip()
    if city_name.isdigit():
         print("Please enter a valid city name ",file=sys.stderr)
         sys.exit(0)
    get_air_quality(city_name)
    get_weather(city_name)
    get_sunmooninfo(city_name)     
    

        