import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

tests = {'single sale': 'https://www.gap.com/browse/product.do?pid=876220002&rrec=true&mlink=5001,1,division_gapdivision1_rr_1&clink=1#pdp-page-content',
         'single standard': 'https://www.gap.com/browse/product.do?pid=432730002&cid=1127945&pcid=1127945&vid=1&nav=meganav%3ABoys%3ACategories%3AShop%20All%20Styles#pdp-page-content',
         'multi sale': 'https://www.gap.com/browse/product.do?pid=879680032&cid=14403&pcid=14403&vid=1&cpos=26&cexp=2859&kcid=CategoryIDs%3D14403&cvar=25415&ctype=Listing&cpid=res24062217322534520794886#pdp-page-content',
         'multi standard': 'https://www.gap.com/browse/product.do?pid=11695010020000&cid=1127945&pcid=1127945&vid=1&nav=meganav%3ABoys%3ACategories%3AShop+All+Styles#pdp-page-content'}


def flatten(xss):
  return [float(x) for xs in xss for x in xs]

def select_single(prices):
  prices = [price_element.split('$')[1:] for price_element in prices]
  prices = flatten(prices) #get all of the prices into a list
  if len(prices) == 1:
    print('not on sale. price: $', prices[0])
    return {'sale price': None, 'standard price': prices[0]}
  elif len(prices) == 2:
    print('on sale. sale price: $', prices[0])
    return {'sale price': prices[0], 'standard price': prices[1]}
  else:
    sale_price = min(prices)
    print('multiple sales? current min price: $', sale_price)
    return {'sale price': sale_price, 'standard price': prices[-1]}

def select_multiple(soup):
  text = soup.select('.swatch-group') #get the data off the page
  text = [price_element.get_text('|', strip=True).split('|') for price_element in text][0] #get all of the text
  prices = {}
  current = 'label'
  for item in text:
    if '$' in item:
      if current == 'label':
        sale_price = float(item.split('$')[1])
        standard_price = sale_price
      else:
        sale_price = float(item.split('$')[1])
      current = 'num'
    else:
      prices[item.lower()] = (sale_price, standard_price)
      current = 'label'
  return prices


def test_get_price(URL):
  response = requests.get(URL, headers=HEADERS) #open my virtual browser
  soup = BeautifulSoup(response.content, 'html.parser') #set up
  prices = soup.select('.pdp-pricing') #get the data off the page
  prices = [price_element.get_text(strip=True) for price_element in prices] #get all of the text
  if '(' not in prices[0]:
    prices = select_single(prices)
  else:
    prices = select_multiple(soup)
  print(prices)
