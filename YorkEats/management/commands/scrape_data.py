from django.core.management.base import BaseCommand
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen


#https://www.geeksforgeeks.org/python-convert-a-list-to-dictionary/
def convert(lst):
   res_dict = {}
   for i in range(0, len(lst), 2):
       res_dict[lst[i].get_text().strip()] = lst[i + 1].get_text().strip()
   return res_dict

#Learned commands from https://www.youtube.com/watch?v=GkxpJyuP0Oc

class Command(BaseCommand):
    help = 'Updates json data with web scraped dining directory'

    def handle(self, *args, **kwargs):

        #Open a fetch html from york dining directory page
        url = "https://www.yorku.ca/foodservices/dining-directory/"
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        #Find all the card elements (which store the info for each restaurant)
        card_htmls = soup.find_all(attrs={'class':'card border-0 mb-5'})

        card_htmls.pop()

        data = {}
        for card_html in card_htmls:
            #If information exists, assign it to the appropriate variable
            if card_html.find("h2") is not None:
                location_name = card_html.find("h2").text
            else:
                location_name = "No name"
            if card_html.find("a") is not None:
                location_link = card_html.find("a").get("href")
            else:
                location_link = "#"
            if card_html.find("i", attrs={"alt": "location:"}) is not None and card_html.find("i", attrs={"alt": "location:"}) != "":
                location = card_html.find("i", attrs={"alt": "location:"}).find_next().text.strip()
            else:
                location = "Unknown location"
            if card_html.find("i", attrs={"alt": "menu offering:"}) is not None:
                menu_offering = card_html.find("i", attrs={"alt": "menu offering:"}).find_next().text.strip()
            else:
                menu_offering = "No genre of cuisine provided"
            if card_html.find("i", attrs={"alt": "payment options:"}) is not None:
                payment_options = card_html.find("i", attrs={"alt": "payment options:"}).find_next().text.strip()
            else:
                payment_options = "No payment options provided"
            if card_html.find("i", attrs={"alt": "menu"}) is not None:
                menu = card_html.find("i", attrs={"alt": "menu"}).find_next().text.strip()
                menu_href = card_html.find("i", attrs={"alt": "menu"}).find_next("a").get("href")
            else:
                menu = "No menu provided"
                menu_href = "#"
            if card_html.find("i", attrs={"alt": "dietary options:"}) is not None:
                dietary_options = card_html.find("i", attrs={"alt": "dietary options:"}).find_next().text.strip()
            else:
                dietary_options = "No dietary options provided"
            if card_html.find("i", attrs={"alt": "opening days and hours:"}) is not None:
                opening_days = convert(card_html.find("i", attrs={"alt": "opening days and hours:"}).find_next().find_all(attrs={"class": "col"}))
            else:
                opening_days = {}

            #Update dictionary with new info
            new_data = {card_htmls.index(card_html): {
                "location_name" : location_name,
                'location': location,
                'location_link' : location_link,
                'menu_offering': menu_offering,
                'payment_options': payment_options,
                'menu': {
                    'menu_name': menu,
                    'menu_href': menu_href
                },
                'dietary_options': dietary_options,
                'opening_days': opening_days
            }}
            data.update(new_data)

        #https://www.javatpoint.com/save-json-file-in-python
        #convert dictionary to json file
        dining_dir = open("YorkEats/data/dining_dir.json", "w")
        json.dump(data, dining_dir, indent=4)
        dining_dir.close()

        print("Successfully scraped dining directory")