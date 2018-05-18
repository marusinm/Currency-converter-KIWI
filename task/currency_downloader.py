import sys
import requests


#
# codes_symbols = {'ALL': 'Lek', 'XCD': '$', 'EUR': '€', 'BBD': '$', 'BTN': '-', 'BND': '$', 'XAF': '-', 'CUP': '$', 'USD': '$',
#         'FKP': '£', 'GIP': '£', 'HUF': 'Ft', 'IRR': '﷼', 'JMD': 'J$', 'AUD': '$', 'LAK': '₭', 'LYD': '-', 'MKD': 'ден',
#         'XOF': '-', 'NZD': '$', 'OMR': '﷼', 'PGK': '-', 'RWF': '-', 'WST': '-', 'RSD': 'Дин.', 'SEK': 'kr',
#         'TZS': 'TSh', 'AMD': '-', 'BSD': '$', 'BAM': 'KM', 'CVE': '-', 'CNY': '¥', 'CRC': '₡', 'CZK': 'Kč', 'ERN': '-',
#         'GEL': '-', 'HTG': '-', 'INR': '₹', 'JOD': '-', 'KRW': '₩', 'LBP': '£', 'MWK': '-', 'MRO': '-', 'MZN': '-',
#                  'ANG': 'ƒ', 'PEN': 'S/.', 'QAR': '﷼', 'STD': '-', 'SLL': '-', 'SOS': 'S', 'SDG': '-', 'SYP': '£', 'AOA': '-',
#                  'AWG': 'ƒ', 'BHD': '-', 'BZD': 'BZ$', 'BWP': 'P', 'BIF': '-', 'KYD': '$', 'COP': '$', 'DKK': 'kr', 'GTQ': 'Q',
#                  'HNL': 'L', 'IDR': 'Rp', 'ILS': '₪', 'KZT': 'лв', 'KWD': '-', 'LSL': '-', 'MYR': 'RM', 'MUR': '₨', 'MNT': '₮',
#                  'MMK': '-', 'NGN': '₦', 'PAB': 'B/.', 'PHP': '₱', 'RON': 'lei', 'SAR': '﷼', 'SGD': '$', 'ZAR': 'R', 'SRD': '$',
#                  'TWD': 'NT$', 'TOP': '-', 'VEF': '-', 'DZD': '-', 'ARS': '$', 'AZN': 'ман', 'BYR': 'p.', 'BOB': '$b',
#                  'BGN': 'лв', 'CAD': '$', 'CLP': '$', 'CDF': '-', 'DOP': 'RD$', 'FJD': '$', 'GMD': '-', 'GYD': '$', 'ISK': 'kr',
#                  'IQD': '-', 'JPY': '¥', 'KPW': '₩', 'LVL': 'Ls', 'CHF': 'Fr.', 'MGA': '-', 'MDL': '-', 'MAD': '-', 'NPR': '₨',
#                  'NIO': 'C$', 'PKR': '₨', 'PYG': 'Gs', 'SHP': '£', 'SCR': '₨', 'SBD': '$', 'LKR': '₨', 'THB': '฿', 'TRY': '-',
#                  'AED': '-', 'VUV': '-', 'YER': '﷼', 'AFN': '؋', 'BDT': '-', 'BRL': 'R$', 'KHR': '៛', 'KMF': '-', 'HRK': 'kn',
#                  'DJF': '-', 'EGP': '£', 'ETB': '-', 'XPF': '-', 'GHS': '-', 'GNF': '-', 'HKD': '$', 'XDR': '-', 'KES': 'KSh',
#                  'KGS': 'лв', 'LRD': '$', 'MOP': '-', 'MVR': '-', 'MXN': '$', 'NAD': '$', 'NOK': 'kr', 'PLN': 'zł', 'RUB': 'руб',
#                  'SZL': '-', 'TJS': '-', 'TTD': 'TT$', 'UGX': 'USh', 'UYU': '$U', 'VND': '₫', 'TND': '-', 'UAH': '₴',
#                  'UZS': 'лв', 'TMT': '-', 'GBP': '£', 'ZMW': '-', 'BTC': 'BTC', 'BYN': 'p.'}


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
            # response = requests.get(
            #     "http://data.fixer.io/api/latest?access_key=3ab64743315376e9f5989fafad92b597&base=" +
            #     self.from_currency +
            #     "&symbols=" +
            #     self.to_currency)
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
            # url_params = ''
            # for key in self.codes_symbols:
            #     url_params += key + ','
            #
            # response = requests.get(
            #     "http://data.fixer.io/api/latest?access_key=3ab64743315376e9f5989fafad92b597&base=" +
            #     self.from_currency +
            #     "&symbols=" +
            #     url_params)
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
