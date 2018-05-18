from flask import Flask, request, jsonify
from currency_downloader import CurrencyDownloader

app = Flask(__name__)

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

    loader = CurrencyDownloader(amount, input_currency, output_currency)
    return jsonify(loader.convert(amount, input_currency, output_currency))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
