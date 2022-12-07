import googlemaps # pip install googlemaps
import requests
import pandas as pd

API_KEY = open('API.txt').read()
map_client = googlemaps.Client(API_KEY)


def get_place_info(city):
    try:
        next_page_token = ""
        clientsName = []  # List to store name of the product
        telephoneNumbers = []  # List to store price of the product
        locations = []  # List to store rating of the product
        while True:
            if not next_page_token:
                response = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=Soccorso%20Stradale%20{city}&key={API_KEY}').json()
            else:
                response = requests.get(f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=Soccorso%20Stradale%20{city}&pagetoken={next_page_token}&key={API_KEY}').json()

            for result in response.get('results'):
                details = requests.get(f'https://maps.googleapis.com/maps/api/place/details/json?place_id={result["place_id"]}&fields=formatted_address,name,formatted_phone_number&key={API_KEY}').json().get("result")
                if "name" in details:
                    clientsName.append(details["name"])
                else:
                    clientsName.append("")
                if "formatted_phone_number" in details:
                    telephoneNumbers.append(details["formatted_phone_number"])
                else:
                    telephoneNumbers.append("")
                if "formatted_address" in details:
                    locations.append(details["formatted_address"])
                else:
                    locations.append("")
            if "next_page_token" not in response:
                break
            else:
                next_page_token = response["next_page_token"]
        df = pd.DataFrame({'Contractor': clientsName, 'Tel. Number': telephoneNumbers, 'Location': locations})
        writer = pd.ExcelWriter(f'{city}.xlsx')
        # write dataframe to excel
        df.to_excel(writer)
        writer.save()
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    get_place_info('Sondrio')