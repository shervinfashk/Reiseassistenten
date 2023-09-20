import requests
from tabulate import tabulate
import sqlite3


def get_current(query):
    try:
        url = "https://api.weatherapi.com/v1/current.json"

        params = {"Key": "4b78e620f8d04e9cb05193741231609", "q": query}

        resp = requests.get(url, params=params)
        resp = resp.json()

        # temp = resp["current"]["temp_c"]
        # wind = resp["current"]["wind_kph"]
        # humidity = resp["current"]["humidity"]
        # uv = resp["current"]["uv"]

        temprature = resp["current"]["feelslike_c"]

        location = resp["location"]["name"]
        country = resp["location"]["country"]
        temp = str(resp["current"]["temp_c"]) + "°"
        feels_like = str(resp["current"]["feelslike_c"]) + "°"
        wind = str(resp["current"]["wind_kph"]) + " km/h"

        tabulate_info = [
            {
                "Location": location,
                "Country": country,
                "Temprature": temp,
                "Temprature feels like": feels_like,
                "Wind": wind,
            }
        ]

        return {"temprature": temprature, "tabulate_info": tabulate_info}
    except (KeyError, TypeError):
        pass


def packing_list(temprature):
    temp = temprature

    recommendations = {
        "Hot": [
            [
                "Breathable Clothes",
                "Lightweight and loose-fitting for airflow in high temperatures.",
            ],
            ["Sun Hat", "Maximum sun protection for face and neck."],
            ["Polarized Sunglasses", "Protects eyes from glare and harmful UV rays."],
            ["Flip-flops or Sandals", "Keeps feet cool and comfortable in the heat."],
            [
                "Moisture-wicking Activewear",
                "Wicks away sweat, keeping you dry during activities.",
            ],
        ],
        "Mild-Warm": [
            [
                "Light Cardigan or Pullover",
                "Great for layering on cooler evenings or mild days.",
            ],
            [
                "Cotton Shirts and Blouses",
                "Comfortable options for warm days, allowing air circulation.",
            ],
            [
                "Light Trousers and Skirts",
                "Versatile choices suitable for various activities.",
            ],
            ["Packable Sun Hat", "Offers sun protection and easy to carry."],
            [
                "Compact Travel Umbrella",
                "Provides shelter from unexpected rain or sun during travels.",
            ],
        ],
        "Cool-Mild": [
            [
                "Cozy Sweater or Fleece Jacket",
                "Keeps you warm and stylish in cooler weather.",
            ],
            ["Long-sleeved Tops and Layers", "Adds extra warmth without bulk."],
            ["Stylish Scarf or Shawl", "Adds style and warmth on cool days."],
            [
                "Touchscreen Gloves",
                "Allow phone use without removing gloves in chilly weather.",
            ],
            ["Comfortable Sneakers or Boots", "Perfect for exploring in comfort."],
        ],
        "Cold": [
            [
                "Insulated Winter Coat",
                "Essential for staying warm in cold temperatures.",
            ],
            [
                "Thermal Base Layers",
                "Keeps you warm and comfortable in sub-zero temperatures.",
            ],
            [
                "Insulated Gloves or Mittens",
                "Essential for protecting hands from freezing temperatures.",
            ],
            [
                "Fleece-lined Leggings or Thermal Pants",
                "Provide extra insulation for legs.",
            ],
            ["Waterproof Snow Boots", "Keep feet warm and dry in snowy conditions."],
        ],
    }

    category = None

    if temp >= 30:
        category = recommendations["Hot"]
        title = "Hot (30°C and above)"
    elif temp >= 20:
        category = recommendations["Mild-Warm"]
        title = "Mild-Warm (20-29°C)"
    elif temp >= 10:
        category = recommendations["Cool-Mild"]
        title = "Cool-Mild (10-19°C)"
    else:
        category = recommendations["Cold"]
        title = "Cold (Under 10°C)"

    display_info = [["Clothing item", "Reasoning"], *category]

    print(title)
    print(tabulate(display_info, tablefmt="simple_grid"))


def print_tabulate(tabulate_info):
    print(
        tabulate(tabulate_info, headers="keys", tablefmt="simple_grid", numalign="left")
    )


def menu():
    instructions = [
        {"Key": "T", "Action": "Compare temprature"},
        {"Key": "P", "Action": "Packing-list suggestion "},
        {"Key": "C", "Action": "Convert currency"},
        {"Key": "S", "Action": "Check security-rating"},
        {"Key": "L", "Action": "Change location"},
        {"Key": "E", "Action": "Exit"},
    ]

    print_tabulate(instructions)
    decision = input("What would you like to do? ").lower()
    return decision


def travel():
    departure = input("Where are you departing from? ")
    arrival = input("Where is your arrival destination? ")

    return {"departure": departure, "arrival": arrival}


def decide(decision, locations):
    if decision not in ["t", "p", "c", "e", "l", "s"]:
        print("\n")
        print("Your choice has to be one of the keys in the menu.")
        print("\n")
    elif decision == "t":
        print("\n")
        try:
            print_tabulate(get_current(locations["departure"])["tabulate_info"])
            print_tabulate(get_current(locations["arrival"])["tabulate_info"])
        except TypeError:
            print("We got no results for your search. Try to change your search.")
        print("\n")
    elif decision == "p":
        print("\n")
        packing_list(get_current(locations["arrival"])["temprature"])
        print("\n")
    elif decision == "c":
        print("\n")
        print(currency_convertor(locations))
        print("\n")
    elif decision == "s":
        print("\n")
        country_security(locations)
        print("\n")
    elif decision == "l":
        return "change"
    elif decision == "e":
        return "break"


def currency_convertor(locations):
    while True:
        try:
            amount = int(input("How many dollars (USD) would you like to exchange? "))
            try:
                arrival = get_current(locations["arrival"])["tabulate_info"][0]["Country"]
            except Exception:
                return ("Sorry. We got no result on your search")
            # departure = sql(departure)
            arrival = sql_currency(arrival)
            exchange_rate = rates(arrival, amount)
            if not exchange_rate:
                return "Sorry! Due to limiations in the API we can only display the 34 most popular currencies in the world."
            return exchange_rate
        except ValueError:
            print("You have to enter a number.")
            pass


def sql_currency(country):
    if len(country.split()) > 1:
        country = country.split()[0]
    conn = sqlite3.connect("currency_codes.db")
    curr = conn.cursor()
    code = curr.execute(
        "SELECT country, code FROM currency_codes WHERE Country LIKE ?",
        ("%" + country + "%",),
    )
    resultat = []
    for row in code:
        resultat.append(row)

    if len(resultat) == 1:
        return resultat[0][1]
    else:
        for land in resultat:
            print(land)

            svar = input("Is this the correct currency? ").lower()
            while svar not in ["yes", "no"]:
                print("You can only answer yes or no.")
                svar = input("Is this the correct currency? ").lower()

            if svar == "yes":
                return land[1]


def rates(arrival, amount):
    url = "https://api.freecurrencyapi.com/v1/latest"

    params = {"apikey": "fca_live_qTV4kZLIzwDuKfkhPlJkpw55lOtePXp20emSBgJR"}

    while True:
        try:
            resp = requests.get(url, params=params)
            resp = resp.json()
            print("\n")
            return (
                f"The current rate for 1 USD is {resp['data'][arrival]} {arrival}"
                + "\n"
                + f"{amount} USD costs {resp['data'][arrival] * amount} {arrival}"
            )
        except KeyError:
            break


def sql_code(country):
    if len(country.split()) > 1:
        country = country.split()[0]
    conn = sqlite3.connect("currency_codes.db")
    curr = conn.cursor()
    code = curr.execute(
        "SELECT country, countrycode FROM currency_codes WHERE Country LIKE ?",
        ("%" + country + "%",),
    )

    resultat = []
    for row in code:
        resultat.append(row)

    if len(resultat) == 1:
        return resultat[0][1]
    else:
        for land in resultat:
            print(land)

            svar = input("Is this the correct country code? ").lower()
            while svar not in ["yes", "no"]:
                print("You can only answer yes or no.")
                svar = input("Is this the correct country code? ").lower()

            if svar == "yes":
                return land[1]


def secure_api(country):
    url = "https://www.travel-advisory.info/api?countrycode=" + country
    resp = requests.get(url)
    resp = resp.json()
    return resp["data"][country]["advisory"]["message"]


def country_security(locations):
    try:
        arrival = get_current(locations["arrival"])["tabulate_info"][0]["Country"]
        country = sql_code(arrival)
        print(secure_api(country))
    except Exception:
        print("Sorry. We got no result on your search")
