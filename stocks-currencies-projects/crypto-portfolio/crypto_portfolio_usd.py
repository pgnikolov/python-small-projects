import requests
import json

# open the current portfolio with previous updated amount and price

with open('small-pyhon-projects/stocks-currencies-projects/crypto_portfolio_usd.json', 'r') as f:
    crypto_portfolio_usd = json.load(f)

print(crypto_portfolio_usd)

command = input("Do you want to add new asset to portfolio? Yes/No:")

while command == "Yes":
    asset = input("Please enter crypto symbol:")
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = (f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&'
           f'from_currency={asset}&to_currency=USD&apikey=0LRABBD5TM69JCFA')

    r = requests.get(url)
    data_crypto = r.json()
    print(data_crypto)
    if asset.lower() not in crypto_portfolio_usd:
        quantity = float(input(f"Please enter the amount of {asset} you have: "))
        rate = data_crypto['Realtime Currency Exchange Rate']['5. Exchange Rate']
        crypto_portfolio_usd.setdefault(asset.lower(), {"price": float(rate), "quantity": quantity})
    # if asset is not in portfolio we add it
    elif asset.lower() in crypto_portfolio_usd:
        rate = data_crypto['Realtime Currency Exchange Rate']['5. Exchange Rate']
        crypto_portfolio_usd[asset.lower()]['price'] = float(rate)
        print(f"The {asset} is allready in your portfolio and its price is updated")

    command = input("Do you want to update your portfolio? Yes/No:")

# Getting the last exchange rates for every asset in portfolio:
for crypto, value in crypto_portfolio_usd.items():
    url = (f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&'
           f'from_currency={crypto.upper()}&to_currency=USD&apikey=0LRABBD5TM69JCFA')

    r = requests.get(url)
    data_crypto = r.json()
    rate = data_crypto['Realtime Currency Exchange Rate']['5. Exchange Rate']
    crypto_portfolio_usd[crypto]["price"] = float(rate)


# write the new data to portfolio file

with open('small-pyhon-projects/stocks-currencies-projects/crypto_portfolio_usd.json', 'w') as f:
    json.dump(crypto_portfolio_usd, f)


# print the info for every asset in portfolio
total_value_portfolio = 0

for crypto, values in crypto_portfolio_usd.items():
    total_value = values["price"] * values['quantity']
    total_value_portfolio += total_value
    print(f"Total value of your {crypto.upper()} asset is: ${total_value:.2f}")
    print(f"You have {crypto_portfolio_usd[crypto]['quantity']} {crypto.upper()}")
    print(f"Current price of {crypto.upper()} is: ${crypto_portfolio_usd[crypto]['price']}\n")

print(f"Total value of you crypto portfolio is: ${total_value_portfolio:.2f}")

