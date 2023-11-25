import os
import re
import requests
from bs4 import BeautifulSoup
from .models import Category, Product


def pizza_parcer():
    url = "https://dominos.by/pizza"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        pizza_containers = soup.find_all('div', class_="product-card product-card--vertical")

        print(pizza_containers)

        for pizza_container in pizza_containers:
            pizza_name = pizza_container.find('div', class_="product-card__title").text
            pizza_description = pizza_container.find('div', class_="product-card__description").text
            pizza_price = pizza_container.find('p', class_="product-card__modification-info-price").text
            image_url = pizza_container.find('img', class_="media-image__element product-card-media__element")['src']

            print("Название пиццы:", pizza_name)
            print("Состав:", pizza_description)
            print("Цена пиццы:", pizza_price)
            print("Фото URL:", image_url)

            image_response = requests.get(image_url)


            if image_response.status_code == 200:
                image_filename = os.path.join('media', os.path.basename(image_url))
                with open(image_filename, 'wb') as image_file:
                    image_file.write(image_response.content)

                category, created = Category.objects.get_or_create(name='Пицца')

                price_search = re.search(r'\d+\.?\d*', pizza_price)
                if price_search:
                    price = float(price_search.group())

                    product = Product.objects.get_or_create(
                        category=category,
                        name=pizza_name,
                        price=price,
                        description=pizza_description,
                        image= image_filename
                        )

                    product.save()

    else:
        print("Failed to retrieve the webpage.", response.status_code)


def sauce_parcer():
    url = "https://dominos.by/sauce"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        sauce_containers = soup.find_all('div', class_="product-card product-card--vertical")

        print(sauce_containers)

        for sauce in sauce_containers:
            sauce_name = sauce.find('div', class_="product-card__title").text
            sauce_price = sauce.find('p', class_="product-card__modification-info-price").text
            sauce_url = sauce.find('img', class_="media-image__element product-card-media__element")['src']

            print("Название пиццы:", sauce_name)
            print("Цена пиццы:", sauce_price)
            print("Фото URL:", sauce_url)

            image_response = requests.get(sauce_url)


            if image_response.status_code == 200:
                image_filename = os.path.join('media', os.path.basename(sauce_url))
                with open(image_filename, 'wb') as image_file:
                    image_file.write(image_response.content)

                category, created = Category.objects.get_or_create(name='Соусы')

                price_search = re.search(r'\d+\.?\d*', sauce_price)
                if price_search:
                    price = float(price_search.group())

                    product = Product.objects.get_or_create(
                        category=category,
                        name=sauce_name,
                        price=price,
                        image= image_filename
                        )

                    product.save()

    else:
        print("Failed to retrieve the webpage.", response.status_code)




def drinks_parcer():
    url = "https://dominos.by/drinks"

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        drink_containers = soup.find_all('div', class_="product-card product-card--vertical")


        for drink in drink_containers:
            drink_name = drink.find('div', class_="product-card__title").text
            drink_price = drink.find('p', class_="product-card__modification-info-price").text
            drink_url = drink.find('img', class_="media-image__element product-card-media__element")['src']

            image_response = requests.get(drink_url)


        if image_response.status_code == 200 and len(drink_url)<100:
            image_filename = os.path.join('media', os.path.basename(drink_url))
            with open(image_filename, 'wb') as image_file:
                image_file.write(image_response.content)

            category, created = Category.objects.get_or_create(name='Напитки')

            price_search = re.search(r'\d+\.?\d*', drink_price)
            if price_search:
                price = float(price_search.group())

                product = Product.objects.get_or_create(
                    category=category,
                    name=drink_name,
                    price=price,
                    image= image_filename
                    )

                product.save()

    else:
        print("Failed to retrieve the webpage.", response.status_code)