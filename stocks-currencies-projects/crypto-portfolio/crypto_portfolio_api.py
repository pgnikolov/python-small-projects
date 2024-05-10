import requests
import json

url = "https://real-time-finance-data.p.rapidapi.com/market-trends"

querystring = {"trend_type": "CRYPTO", "country": "us", "language": "en"}

headers = {
    "X-RapidAPI-Key": "31cab704a2msh1af613df96dd45bp115431jsnd7745fec4db5",
    "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

btc_rate = data['data']['trends'][0]
btc_usd = float(btc_rate['exchange_rate'])

eth_data = data['data']['trends'][1]
eth_usd = float(eth_data['exchange_rate'])

bnb_data = data['data']['trends'][3]
bnb_usd = float(bnb_data['exchange_rate'])

doge_data = data['data']['trends'][6]
doge_usd = float(doge_data['exchange_rate'])

link_data = data['data']['trends'][7]
link_usd = float(link_data['exchange_rate'])

ltc_data = data['data']['trends'][8]
ltc_usd = float(ltc_data['exchange_rate'])

waves_data = data['data']['trends'][16]
waves_usd = float(waves_data['exchange_rate'])

mana_data = data['data']['trends'][21]
mana_usd = float(mana_data['exchange_rate'])

crypto_prices = {'btc': {'price': btc_usd, 'quantity': 10}, 'eth': {'price': eth_usd, 'quantity': 20.5},
                 'bnb': {'price': bnb_usd, 'quantity': 22.65}, 'doge': {'price': doge_usd, 'quantity': 12111},
                 'link': {'price': link_usd, 'quantity': 11257}, 'ltc': {'price': ltc_usd, 'quantity': 559},
                 'waves': {'price': waves_usd, 'quantity': 14257}, 'mana': {'price': mana_usd, 'quantity': 12547}}


command = input('Do you want to update the quantity of some asset? (Yes/No):')

while True:
    if command == "No":
        break
    elif command == "Yes":
        asset = input("Plese enter the asset you want to change").lower()
        print(f"Current quantity of {asset.upper()} is {crypto_prices[asset]['quantity']} ")
        crypto_prices[asset]['quantity'] = float(input("Please enter the new value:"))
    command = input('Do you want to update the quantity of other asset? (Yes/No):')


total_value_portfolio = 0

for crypto, values in crypto_prices.items():
    total_value = values["price"] * values['quantity']
    total_value_portfolio += total_value
    print(f"Total value of your {crypto.upper()} asset is: ${total_value:.2f}")
    print(f"Current price of {crypto.upper()} is: ${crypto_prices[crypto]['price']}\n")

# Print the updated dictionary
print(f"Total value of you crypto portfolio is: ${total_value_portfolio:.2f}")
