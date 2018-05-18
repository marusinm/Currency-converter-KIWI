import sys
import requests

class CurrencyDownloader:
    """Working with rest API to get currency rates"""

    def __init__(self, amount, from_currency, to_currency):
        """
        init class variables
        :param from_currency: currency code or currency symbol
        :param to_currency: currency code or currency symbol
        :param amount: amount to convert
        """
        self.amount = amount
        self.from_currency = from_currency
        self.to_currency = to_currency

        # download all currencies and parse their codes and symbols into dict
        self.codes_symbols = self.get_codes_and_signs(self.get_all_currencies())

        # check validity of from_currency code or symbol
        if from_currency not in self.codes_symbols.keys():
            if from_currency not in self.codes_symbols.values():
                print("'From' currency code or symbol doesn't exists!")
                sys.exit()
            else:
                for key, value in self.codes_symbols.items():
                    if value == from_currency:
                        self.from_currency = key

        # check validity of from_currency code or symbol
        if to_currency != '':  # to_currency can be empty
            if to_currency not in self.codes_symbols.keys():
                if to_currency not in self.codes_symbols.values():
                    print("'To' currency code or symbol doesn't exists!")
                    sys.exit()
                else:
                    for key, value in self.codes_symbols.items():
                        if value == to_currency:
                            self.to_currency = key

    @staticmethod
    def get_all_currencies():
        """Get all available currencies and parse it to readable format"""
        try:
            response = requests.get('https://free.currencyconverterapi.com/api/v5/currencies')
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        data = response.json()
        return data

    @staticmethod
    def get_codes_and_signs(data):
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

    def __get_single_currency_rate(self):
        """
        Get exchange rate of self.from_currency to self.to_currency
        :return: float number of exchange rate
        """
        try:
            response = requests.get(
                "https://v3.exchangerate-api.com/bulk/5c110b20b14a95d3a024be2d/" + self.from_currency)
            response.raise_for_status()
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        # example: {"success":true,"timestamp":1526562187,"base":"EUR","date":"2018-05-17","rates":{"USD":1.181191}}
        data = response.json()
        return data['rates'][self.to_currency]

    def __get_multiple_currency_rate(self):
        """
        Get exchange rates of self.from_currency to every other currencies
        :return: dict of currencies codes and their rates
        """
        try:
            response = requests.get(
                "https://v3.exchangerate-api.com/bulk/5c110b20b14a95d3a024be2d/"+self.from_currency)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            sys.exit(1)

        # example: {"success":true,"timestamp":1526562187,"base":"EUR","date":"2018-05-17","rates":{"USD":1.181191}}
        data = response.json()
        return data['rates']

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
        converted_num = float(self.amount) * float(self.__get_single_currency_rate())
        return {self.to_currency: converted_num}

    def convert_multiple_currencies(self):
        """
        Convert self.amount from one currency to all others currencies
        :return: dict of converted amounts for every currency code
        """
        codes_signs = self.__get_multiple_currency_rate()
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
