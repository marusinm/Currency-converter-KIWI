import sys
import requests


class CurrencyDownloader:
    """Working with rest API to get currency rates"""

    BASE_URL = 'https://v3.exchangerate-api.com/bulk/5c110b20b14a95d3a024be2d/'
    CODES_SIGNS_URL = 'https://free.currencyconverterapi.com/api/v5/currencies'

    def __init__(self, amount, from_currency, to_currency):
        """
        init class variables
        :param from_currency: currency code or currency symbol
        :param to_currency: currency code or currency symbol
        :param amount: amount to convert
        """
        self.amount = amount

        # download all currencies and parse their codes and symbols into dict
        self.codes_symbols = self.__get_codes_and_signs(self.__get_all_currencies())

        self.from_currency = self.__is_currency_valid(from_currency)
        self.to_currency = self.__is_currency_valid(to_currency)

        if self.from_currency is None or self.to_currency is None:
            print("'From/To' currency code or symbol doesn't exists!")
            sys.exit()
        return

    def __get_all_currencies(self):
        """Get all available currencies and parse it to readable format"""
        try:
            response = requests.get(self.CODES_SIGNS_URL)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        data = response.json()
        return data

    def __get_codes_and_signs(self, data):
        """
        Get currencies codes and symbols from json input
        :param data: json data
        :return: dictionary keys - currencies codes, values - currencies symbols
        """
        codes = data['results'].keys()
        codes_signs = {}
        for key in codes:
            if 'currencySymbol' in data['results'][key].keys():
                codes_signs[key] = data['results'][key]['currencySymbol']
            else:
                codes_signs[key] = '-'

        return codes_signs

    def __is_currency_valid(self, currency):
        """
        Checks if currency code or sign exist for this class
        :param currency: currency to be checked
        :return: currency code, None otherwise
        """
        if currency == '':  # to_currency can be empty
            return ''

        if currency not in self.codes_symbols.keys():
            if currency not in self.codes_symbols.values():
                return None
            else:  # that mean we have just currency symbol but we need work with currency code - find it
                for key, value in self.codes_symbols.items():
                    if value == currency:
                        currency = key

        return currency

    def __get_currency_rate(self, currency=None):
        """
        Get exchange rate of self.from_currency to currency if defined (all currencies otherwise)
        :param currency: currency or None
        :return: dict of currencies codes and their rates or single float number of exchange rate
        """
        try:
            response = requests.get(
                self.BASE_URL + self.from_currency)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        # example: {"success":true,"timestamp":1526562187,"base":"EUR","date":"2018-05-17","rates":{"USD":1.181191}}
        data = response.json()
        if currency is None:
            return data['rates']
        else:
            return data['rates'][currency]

    def show_saved_codes_and_symbols(self):
        """
        Print downloaded currency codes and symbols
        :return:
        """
        print(self.codes_symbols)

    def get_input_currency_code(self):
        return self.from_currency

    def convert_single_currency(self):
        """
        Convert self.amount from one currency to another
        :return: singe float number
        """
        converted_num = float(self.amount) * float(self.__get_currency_rate(self.to_currency))
        return {self.to_currency: converted_num}

    def convert_multiple_currencies(self):
        """
        Convert self.amount from one currency to all others currencies
        :return: dict of converted amounts for every currency code
        """
        codes_signs = self.__get_currency_rate()
        for key in codes_signs:
            codes_signs[key] = float(codes_signs[key]) * float(self.amount)
        return codes_signs

    def convert(self, amount, input_currency, output_currency):
        """
        Converts amount from one input_currency to output_currency
        :param amount float to convert
        :param input_currency: from_currency
        :param output_currency: to_currency
        :return: dictionary of data which look like json outpus
        """

        if output_currency != '':
            data = self.convert_single_currency()
        else:
            data = self.convert_multiple_currencies()

        json_output = {
            "input": {
                "amount": amount,
                "currency": self.get_input_currency_code()
            },
            "output": data
        }

        return json_output
