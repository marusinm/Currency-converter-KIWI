# Currency-converter-KIWI
kiwi junior python developer task

## How to run it (use Docker of run it on localhost)

### Docker

You can use pre-prepared Dockerfile for example: 
```
docker build -t kiwi_task .
docker run -p 80:80 kiwi_task
```
Or you can download it from Docker Hub

### Run it on localhost
Use run.sh for unix base systems or just enter /task folder and run currency_converter.py as python script 
```
# install packages
pip3 install requests
pip3 install flask

./run.sh
```

## App contains?

- CLI application
- web API application

## Parameters
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

## Functionality
- if output_currency param is missing, convert to all known currencies

## Output
- json with following structure.
```
{
    "input": {
        "amount": <float>,
        "currency": <3 letter currency code>
    },
    "output": {
        <3 letter currency code>: <float>
    }
}
```
## Examples

### CLI
```
./currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36
    }
}
```
```
./currency_converter.py --amount 0.9 --input_currency ¥ --output_currency AUD
{
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20
    }
}
```
```
./currency_converter.py --amount 10.92 --input_currency £
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```
### API
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.20,
    }
}
```

```
GET /currency_converter?amount=10.92&input_currency=£ HTTP/1.1
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```