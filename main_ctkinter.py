#Import Necessary Modules
import os
import requests
from dotenv import load_dotenv
from PIL import Image, ImageTk
import customtkinter as ctk
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel, CTkImage

# Load environment variables from .env file
load_dotenv()

# Define constants
FONT = ("Times New Roman", 10, "bold")
BG = "#6c9cf0"
API_KEY = os.getenv("API_KEY")
URL = "https://api.openweathermap.org/data/2.5/weather"
PARAMETER = {
    "q": "",
    "units": "metric",
    "appid": API_KEY
}

# Function to fetch weather data
def fetch_weather_data(city_name):
    PARAMETER["q"] = city_name
    response = requests.get(url=URL, params=PARAMETER)
    data = response.json()
    return data, response.status_code


# Function to parse weather data
def parse_weather_data(data):
    city_name = data.get("name")
    city_temp = round(data.get("main").get("temp"))
    humidity_val = data.get("main").get("humidity")
    wind_speed = data.get("wind").get("speed")
    weather_description = (data.get("weather")[0].get("description")).title()
    weather_condition = (data.get("weather")[0].get("main")).lower()
    return city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition


# Function to update labels with weather data
def update_labels(city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition):
    city_name_label.configure(text=f"{city_name}")
    humidity_value.configure(text=f"{humidity_val}%")
    wind_speed_value.configure(text=f"{wind_speed}km/h")
    city_temp_label.configure(text=f"{city_temp}°c | {weather_description}")

    atmosphere = ["mist", "haze", "smoke", "dust", "fog", "sand", "ash", "squall", "tornado"]
    print(weather_condition)

    if weather_condition in atmosphere:
        window.weather_img = CTkImage(Image.open("./assets/images/atmosphere.png"), size=(224,224))
    else:
        window.weather_img = CTkImage(Image.open(f"./assets/images/{weather_condition}.png"), size=(224,224))
    city_condition_label.configure(image=window.weather_img)


# Function to display all the weather data
def display_widgets():
    city_condition_label.grid()
    city_temp_label.grid()
    city_name_label.grid()
    humidity_icon.grid()
    humidity_value.grid()
    humidity_label.grid()
    wind_speed_icon.grid()
    wind_speed_label.grid()
    wind_speed_value.grid()


# Function to remove all widgets
def remove_widgets():
    city_condition_label.grid_remove()
    city_temp_label.grid_remove()
    city_name_label.grid_remove()
    humidity_icon.grid_remove()
    humidity_value.grid_remove()
    humidity_label.grid_remove()
    wind_speed_icon.grid_remove()
    wind_speed_value.grid_remove()
    wind_speed_label.grid_remove()


# Function to get weather data
def get_weather_data():
    city_name = search_entry.get()
    data, status_code = fetch_weather_data(city_name)
    if status_code == 200:
        city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition = parse_weather_data(data)
        update_labels(city_name, city_temp, humidity_val, wind_speed, weather_description, weather_condition)
        display_widgets()
    else:
        remove_widgets()
        error_label = create_text_label(window, text="City not found. Please try again.", font=("Times New Roman", 20, "bold"), row=4, column=2)
        error_label.grid()

# Function to create a label with text
def create_text_label(window, text, font, row, column):
    label = CTkLabel(window, text=text, font=font, fg_color="transparent")
    label.grid(row=row, column=column)
    label.grid_remove()
    return label


# Function to create a label with an image
def create_image_label(window, image, row, column):
    label = CTkLabel(window, text="", image=image)
    label.grid(row=row, column=column)
    label.grid_remove()
    return label


# set mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# Create Main Window
window = CTk()
window.title("Weather App")
window.config(padx=30, pady=30)

# Importing Images 
search_img = CTkImage(Image.open("./assets/images/searchbtn.png"))
condition_img = CTkImage(Image.open("./assets/images/clouds.png"), size=(224, 224))
humidity_img = CTkImage(Image.open("./assets/images/humidity.png"))
wind_speed_img = CTkImage(Image.open("./assets/images/wind.png"))


# Search Entry
search_entry = CTkEntry(
    window, justify = "left", width=75, placeholder_text="City Name", 
    fg_color="transparent", corner_radius=32)
search_entry.grid(row=0, column=0, columnspan=4, padx=3, sticky='nsew')

# Search Button
search_btn = CTkButton(
    window, text="Search", width= 5, image=search_img, command=get_weather_data, 
    corner_radius=32, fg_color = "transparent", border_width=1)
search_btn.grid(row=0, column=4)

# Create Labels
city_condition_label = create_image_label(window, image=condition_img, row=1, column=2)
city_temp_label = create_text_label(window, text="7°c | Sunny", font=("Times New Roman", 20, "bold"), row=2, column=2)
city_name_label = create_text_label(window, text="New York", font=("Times New roman", 25, "bold"), row=3, column=2)

humidity_icon = create_image_label(window, image=humidity_img, row=4, column=0)
humidity_value = create_text_label(window, text="48%", font=("Times New Roman", 13, "bold"), row=4, column=1)
humidity_label = create_text_label(window, text="Humidty", font=FONT, row=5, column=1)

wind_speed_icon = create_image_label(window, image=wind_speed_img, row=4, column=3)
wind_speed_value = create_text_label(window, text="10.29 km/h", font=("Times New Roman", 13, "bold"), row=4, column=4)
wind_speed_label = create_text_label(window, text="Wind Speed", font=FONT, row=5, column=4)


# Start the main loop
window.mainloop()