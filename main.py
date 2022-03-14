from selenium import webdriver
import pandas

url = 'https://coinmarketcap.com/'

class Coin:
    full_name = ""
    short_name = ""
    price = 0.0
    p24h = ""
    p7d = ""
    market_cap = 0.0
    volume24h = 0.0
    circulating_supply = 0
    
driver = webdriver.Chrome('./chromedriver')
driver.get(url)
driver.execute_script("window.scrollTo(0,1250);")
coins = []
coins_rows = driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0:25]
for coin_row in coins_rows:
    
    new_coin = Coin()
    new_coin.full_name = coin_row.find_elements_by_tag_name('p')[1].text
    new_coin.short_name = coin_row.find_elements_by_tag_name('p')[2].text
    new_coin.price = float(coin_row.find_elements_by_tag_name('span')[2].text.replace('$', '').replace(',', ''))
    
    if coin_row.find_elements_by_tag_name('span')[4].get_attribute('class') == 'icon-Caret-up':
        new_coin.p24h = "+" + coin_row.find_elements_by_tag_name('span')[3].text
    else:
        new_coin.p24h = "-" + coin_row.find_elements_by_tag_name('span')[3].text
        
    if coin_row.find_elements_by_tag_name('span')[6].get_attribute('class') == 'icon-Caret-up':
        new_coin.p7d= "+" + coin_row.find_elements_by_tag_name('span')[5].text
    else:
        new_coin.p7d = "-" + coin_row.find_elements_by_tag_name('span')[5].text
    
    new_coin.market_cap = float(coin_row.find_elements_by_tag_name('span')[8].text.replace('$', '').replace(',', ''))
    
    new_coin.volume24h = float(coin_row.find_elements_by_tag_name('p')[4].text.replace('$', '').replace(',', ''))
    
    new_coin.circulating_supply = int(''.join(filter(str.isdigit, coin_row.find_elements_by_tag_name('p')[6].text.replace(',', ''))))
    
    coins.append(new_coin)
    
    
df = pandas.DataFrame([vars(coin) for coin in coins])
df.index = df.index + 1
df.to_csv('parsedData.csv', sep=';')
print(df)

def search_coin(coin_name: str):
    search_results = df[df.eq(coin_name).any(1)]
    if(not search_results.empty):
        return search_results
    else:
        return 'Not found'

while True:
    print('Input coin full or short name to get info from dataframe >>', end=" ")
    print(search_coin(str(input())))