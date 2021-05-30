import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


class Parser:
    URL = "https://coinmarketcap.com/currencies/"

    def get_page(self, token_slug):
        try:
            response = requests.get(self.URL + token_slug)
        except ConnectionError:
            return False
        if response.status_code == 200:
            return response
        else:
            return False

    @staticmethod
    def parse_page(page):
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @staticmethod
    def parse_price(page):
        price = page.find('div', class_="priceValue___11gHJ")
        return price.text[1:]

    @staticmethod
    def prettify_price(price):
        price = price.replace(',', '')
        price = float(price)
        return price

    def get_price(self, token_slug):
        page = self.get_page(token_slug)

        if not page:
            return False
        soup = self.parse_page(page)
        price = self.parse_price(soup)
        price = self.prettify_price(price)
        return price

    def check_if_exists(self, token):
        page = self.get_page(token)
        if not page: return False
        return True


if __name__ == '__main__':
    a = Parser()
    print(a.get_price("Bitcoin"))