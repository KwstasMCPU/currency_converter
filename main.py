import requests


url = 'http://data.fixer.io/api/'
LATEST =  'latest?access_key='
HISTORICAL_DATA = 'YYYY-MM-DD' # FORMAT



ACCESS_KEY = 'acde643bc15d7ce29bb0e1ec699715e2'

data = {}
data = requests.get(url+LATEST+ACCESS_KEY).json()
rates = data['rates']

#print(data['rates']['USD'])

def return_latest(from_currency, to_currency, amount):
    if from_currency != 'EUR':
        amount = amount / rates[from_currency]

    amount = amount * rates[to_currency]
    return round(amount, 2)

print(return_latest('USD','JPY',100))

