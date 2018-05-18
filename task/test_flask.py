from flask import Flask, url_for, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello/')
def hello():
    return 'Hello, world'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Post"
    else:
        return "Get"


json = {
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20,
    }
}


@app.route('/get_json')
def get_json():
    return jsonify(json)

# example: GET /currency_converter?amount=10.0&input_currency=€&output_currency=CZK HTTP/1.1
@app.route('/currency_converter')
def currency_converter():
    # print(amount = request.args.get('amount', type=float))
    # print(input_currency = request.args.get('input_currency', type=str))
    # print(output_currency = request.args.get('output_currency', default='', type=str))
    amount=request.args['amount']
    input_currency=request.args['input_currency']
    output_currency=request.args['output_currency']

    return 'amount: ' + amount + " input_currency: " + input_currency + " output_currency: " + output_currency


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('show_user_profile', username='John Doe'))
    print(url_for('show_post', post_id="1234"))
