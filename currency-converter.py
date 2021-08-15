import requests
import json


class ExchangeCache:
    def __init__(self):
        self.memory = {}

    def add_base_currency(self, base_currency_code):
        self.memory[base_currency_code] = {}

    def add_base_currency_exchange_info(self, base_currency_code,
                                        target_currency_code,
                                        exchange_info):
        self.memory[base_currency_code].update({target_currency_code: exchange_info[target_currency_code]})

    def get_exchange_cache(self):
        return self.memory

    def get_exchange_rate(self, base_currency_code, target_currency_code):
        return self.memory[base_currency_code][target_currency_code]['rate']

    def remove_from_memory(self, element):
        self.memory.pop(list(element.keys())[0])

    def is_currency_exchange_info(self, base_currency_code, target_currency_code):
        return bool(target_currency_code in list(self.memory[base_currency_code].keys()))

    def clear_memory(self):
        self.memory.clear()


def get_base_currency_code():
    return input()


def get_target_currency_code():
    return input()


def get_money_to_exchange():
    return float(input())


def request_exchange_rates(currency_code):
    return requests.get(f'http://www.floatrates.com/daily/{currency_code}.json')


def print_dict(dictionary, slice_=False, range_=None):
    # print_dict(exchange_cache.get_exchange_cache()[base_currency_code], slice_=True, range_=1)
    if slice_ and range_:
        dictionary = dict(list(dictionary.items())[:range_])  # get (range_ - 1) dict elements.
    else:
        dictionary = dict(list(dictionary.items())[:])  # get (range_ - 1) dict elements.
    print(json.dumps(dictionary, indent=4))


def main():
    exchange_cache = ExchangeCache()

    base_currency_code = get_base_currency_code().lower()

    exchange_rates = request_exchange_rates(base_currency_code)

    if exchange_rates:
        exchange_rates_dict = exchange_rates.json()

        exchange_cache.add_base_currency(base_currency_code)
        n = 0

        # print(exchange_cache.get_exchange_cache()[base_currency_code]['usd']['rate'])
        while True:
            target_currency_code = get_base_currency_code().lower()
            if target_currency_code == '':
                break
            if n == 0:
                n += 1
                if base_currency_code != 'usd':
                    exchange_cache.add_base_currency_exchange_info(base_currency_code, 'usd', exchange_rates_dict)
                if base_currency_code != 'eur':
                    exchange_cache.add_base_currency_exchange_info(base_currency_code, 'eur', exchange_rates_dict)
            money_to_exchange = get_money_to_exchange()
            print('Checking the cache...')
            if exchange_cache.is_currency_exchange_info(base_currency_code, target_currency_code):
                print('Oh! It is in the cache!')
            else:
                print('Sorry, but it is not in the cache!')
                exchange_cache.add_base_currency_exchange_info(base_currency_code, target_currency_code,
                                                               exchange_rates_dict)
            exchange_amount = money_to_exchange * exchange_cache.get_exchange_rate(base_currency_code, target_currency_code)
            print(f"You received {round(exchange_amount, 2)} {target_currency_code.upper()}.")


if __name__ == '__main__':
    main()
