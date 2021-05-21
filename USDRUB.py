import requests
from bs4 import BeautifulSoup


class USDRUBParser:
    __URL = "https://quote.rbc.ru/ticker/59111"

    def _get_page(self):
        response = requests.get(self.__URL)
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
        price = page.find('div', class_="chart__info__row js-ticker").find('span', class_="chart__info__sum")
        return price.text

    @staticmethod
    def prettify_price(price):
        price = price.replace(',', '.')[1:]
        price = float(price)
        return price


    def get_price(self):
        page = self._get_page()
        soup = self.parse_page(page)
        price = self.parse_price(soup)
        price = self.prettify_price(price)
        return price


if __name__ == '__main__':
    parser = USDRUBParser()
    print(parser.get_price())
