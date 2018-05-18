#!/usr/bin/python

import sys
import getopt
import json
from flask import Flask, request, jsonify
from currency_downloader import CurrencyDownloader

app = Flask(__name__)


def parse_options(argv):
    """
    Handle all options
    :param argv: args from CLI
    :return: parsed amount, input_currency, output_currency
    """
    amount = -1.0
    input_currency = ''
    output_currency = ''
    help = 'currency_converter.py --amount <amount> --input_currency <input_currency> --output_currency <output_currency>'
    try:
        opts, args = getopt.getopt(argv, "h", ["amount=", "input_currency=", "output_currency="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt == "--amount":
            amount = float(arg)
        elif opt == "--input_currency":
            input_currency = arg
        elif opt == "--output_currency":
            output_currency = arg

    if amount < 0:
        print('Amount must be positive!')
        sys.exit(1)
    if input_currency == '':
        print('Input currency must be provided!')
        sys.exit(1)

    return amount, input_currency, output_currency


@app.route('/')
def index():
    return "index"


# example: GET /currency_converter?amount=10.0&input_currency=€&output_currency=CZK HTTP/1.1
@app.route('/currency_converter')
def currency_converter():
    args = request.args.to_dict()
    amount = request.args['amount']
    input_currency = request.args['input_currency']
    if len(args) == 3:
        output_currency = request.args['output_currency']
    else:
        output_currency = ''

    return jsonify(convert(amount, input_currency, output_currency))

def convert(amount, input_currency, output_currency):
    loader = CurrencyDownloader(amount, input_currency, output_currency)
    if output_currency != '':
        data = loader.convert_single_currency()
    else:
        data = loader.convert_multiple_currencies()

    json_output = {
        "input": {
            "amount": amount,
            "currency": loader.get_input_currency_code()
        },
        "output": data
    }

    return json_output


# example python3.6 currency_converter.py --amount 10 --input_currency EUR --output_currency CZK
# python3.6 currency_converter.py --amount 10 --input_currency € --output_currency CZK
if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80)

    amount, input_currency, output_currency = parse_options(sys.argv[1:])
    print(json.dumps((convert(amount, input_currency, output_currency)), indent=4, sort_keys=True))
