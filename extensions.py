import json
import requests
from config import keys

class APIException(Exception):
    pass

class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Нельзя переводить одинаковые валюты {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')
        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f'Не удалось обработать количество {amount}')
        response = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(response.content)[keys[base]]
        print(response)
        print(total_base)
        if response.status_code != 200:
            raise Exception('Ошибка при запросе к API')
        basee = json.loads(response.content)
        if quote not in base:
            raise Exception('Валюта не найдена')
        return total_base * round(amount, 2)