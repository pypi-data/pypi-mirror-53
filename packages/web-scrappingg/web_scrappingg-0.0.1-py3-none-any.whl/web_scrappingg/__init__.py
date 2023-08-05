#Importing the packages

import urllib.request
from bs4 import BeautifulSoup as soup
import requests
import json

#Getting the User input to which he would like to see the weather info

user_input = input(" Enter the city name that you would like to  see the wather conditions: ")
print(" Getting the weather Info of " + user_input + ".....")

# add it to the following URL to get the Place_ID here
response = requests.get("https://api.weather.com/v3/location/search?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&language=en-IN&locationType=locale&query=" + user_input)

# This gives the Json Data
r = response.content

# prettifying the Json Data here
parsed_json = (json.loads(r))
p_data = json.dumps(parsed_json, indent=4, sort_keys=True)
a = json.loads(p_data)

# Getting the place_Id from the Json Dictionary
b = a["location"]["placeId"][0]

#Getting the weather info by adding the above place_ID to the URL

my_url = "https://weather.com/en-IN/weather/today/l/"+b

# 
req = urllib.request.Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()

#html parsing
page_soup = soup(html, "html.parser")

print(page_soup.find(class_="today_nowcard-sidecar component panel").text)
print(page_soup.find(class_="today_nowcard-main component panel today-card-night-cloudy-mostly").text)
	
		
	
	

