import json  # импортируем модуль для работы с JSON
import requests  # импортируем модуль для работы с HTTP-запросами
from config import keys  # импортируем из файла config.py словарь с кодами валют


class APIException(Exception):  # создаем класс для обработки ошибок
    pass


class CriptoConverter:  # создаем класс для конвертации криптовалют
    @staticmethod  # создаем статический метод для получения курса валют
    def get_price(quote: str, base: str, amount: str):
        if quote == base:  # проверяем, не выбраны ли одинаковые валюты
            raise APIException(f'Нельзя конвертировать одинаковую валюту {base}.')
        try:
            quote_ticker = keys[quote]  # получаем код валюты из словаря
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {quote}. Доступны следующие валюты: {", ".join(keys.keys())}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {base}. Доступны следующие валюты: {", ".join(keys.keys())}')
        try:
            amount = float(amount)  # преобразуем количество валюты в число
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}! Количество должно быть числом.')

        try:
            response = requests.get(  # делаем GET-запрос на сервер
                f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}', timeout=15)
            print(response.status_code)  # парсим код статуса ответа от сервера в консоль
            if response.status_code != 200:  # проверяем, что ответ от сервера не содержит ошибок
                raise Exception(
                    f'Ошибка при запросе к серверу. Код ошибки: {response.status_code}. \nПожалуйста, попробуйте позже')
            try:
                total_base = json.loads(response.content)[keys[base]]  # получаем значение курса валют из JSON-ответа
            except (json.JSONDecodeError, ValueError):  # обрабатываем ошибки при обработке JSON-ответа
                raise Exception(f'Не удалось обработать ответ от сервера.')
        except requests.exceptions.ReadTimeout:  # обрабатываем ошибку превышения времени ожидания ответа от сервера
            raise Exception('Ошибка: превышено время ожидания ответа от сервера. Повторяем запрос...')
            return CriptoConverter.get_price(quote, base, amount)  # повторяем запрос
        return total_base * round(amount, 2)  # возвращаем конвертированную валюту
