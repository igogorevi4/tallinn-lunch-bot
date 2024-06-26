import requests
from bs4 import BeautifulSoup
import yaml
import sys

telegram_bot_token = sys.argv[1]
telegram_chat_id = sys.argv[2]
rotermann_url = "https://rotermann.ee/tana-lounaks/"


def send_telegram_message(message):
    requests.post('https://api.telegram.org/bot' + telegram_bot_token + '/sendMessage?chat_id=' + telegram_chat_id + '&text=' + message)
    # print("Success")


def collect_rotterman_dishes_list():
    response = requests.get(rotermann_url)
    soup = BeautifulSoup(response.content, "html.parser")

    restaurants = {}
    restaurant_sections = soup.find_all("div", class_="lunch--inner")

    for section in restaurant_sections:
        restaurant_name = section.find("h3").text.strip()
        dishes = []

        dish_items = section.find_all("div", class_="single-offer--content")
        price_items = section.find_all("div", class_="single-offer--price")

        for dish_item, price_item in zip(dish_items, price_items):
            dish_name = dish_item.find("p").text.strip()
            price = price_item.find("p").text.strip()
            dish_name = dish_name + ': ' + price
            dishes.append(dish_name)

        restaurants[restaurant_name] = dishes
    return restaurants


for restaurant, dishes in collect_rotterman_dishes_list().items():
    dict_to_send = {}

    dict_to_send[restaurant] = dishes

    send_telegram_message(dict_to_send)
