# Reiseassistenten

A command-line interface travel helper created using Python

Description: This program is a travel helper which provides the user with information about the departure and arrival destination. The program allows the user to compare tempratures, provides a suggestion for clothes to bring, compare currencies and check the safety rating of the arrival location. The program uses multiple API's. The API's used are: [FreeCurrency](https://freecurrencyapi.com/), [WeatherAPI](https://www.weatherapi.com/) and [Travel-Advisory](https://www.travel-advisory.info/data-api).

My ambition with this program is to showcase that I understand basic programming concepts. I am happy with the way the program works, but I dont think the program is user-friendly. There was multiple limitations in the API's since I used free versions which decreases the value for endusers. My aim is that my next program will be created with the users needs as the first priority instead of being limited by my knowledge and API limits. 

I have not been able create unit tests for the program yet. It has only been tested manually, let me know if there is any issues.

---
## Functions

This program has a lot of functions. I am going to highlight one of them and describe them here. For further descriptions of the functions, look at the comments in [functions.py](https://github.com/shervinfashk/reisehjelperen/blob/main/functions.py)

sql_currency(country) is a "sub-function" in the currency_convertor(locations) function. The sql_currency(country) is provided a country as the parameter and returns country's currency code. The currency code is required to be able to use the [FreeCurrency API](https://freecurrencyapi.com/). The first this this function does is to sjekk the lenght of the paramter provides. The reason for this is that countries provided by [WeatherAPI](https://www.weatherapi.com/) and the names in the database dont always match up and if the SQL query result in more then one result if can return the wrong currency code. For example the country provided by the API may have the name "United States of America" while this country's name in the database is "United States". Another example of this is when searching for "India" you get two results. "British Indian Ocean Territory" and "India". To solve this issue the user get the choice to look at all the results if the result list is longer then one and decide which country is correct.



---

## Installation

Use [pip](https://pip.pypa.io/en/stable/) to install the package `tabulate`, `sqlite3` and `requests`
```
$ pip install tabulate
```

```
$ pip install requests
```

```
$ pip install sqlite3
```

---

## Usage

Use [python](https://www.python.org/) to run the application
```
$ python project.py
```

---
