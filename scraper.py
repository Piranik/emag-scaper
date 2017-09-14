from bs4 import BeautifulSoup

import math
import re
import requests
import pika

PRODUCTS = {
	'phones': [
		{
			'name': 'iphone',
			'address': 'https://www.emag.ro/search/iphone'
		},
		{
			'name':'iphone 6s',
		    # 'address': 'https://www.emag.ro/search/telefoane-mobile/iphone+6s/c'
			'address': 'https://www.emag.ro/search/telefoane-mobile/iphone/c?ref=autosuggest'
		},
		{
			'name':'iphone 7',
		    'address': 'https://www.emag.ro/search/telefoane-mobile/iphone+6s/c'
		},
		{
			'name': 'samsung galaxy s7',
		    'address': 'https://www.emag.ro/search/telefoane-mobile/iphone+6s/c'
		},
		{
			'name':'samsung galaxy s7 edge',
		    'address': 'https://www.emag.ro/search/telefoane-mobile/iphone+6s/c'
		},
		{
			'name': 'samsung galaxy s8',
			'address': 'https://www.emag.ro/search/telefoane-mobile/iphone+6s/c'
		}]
}

def request_page(link):
	r = requests.get(link)
	return r.text


def get_pages_no(title):
	print title
	PRODUCTS_PER_PAGE = 60
	pattern = re.compile('(\d+)( [\w|\'\" ]+)')
	total_products = float(pattern.match(title).group(1))
	return int(math.ceil(total_products / PRODUCTS_PER_PAGE))


def product_links(main_link, pages_no):
	EMAG_LINK_START_PAGE_NO = 2
	links = [main_link]
	for i in range(2, pages_no+1):
		links.append('%s/p%d' % (main_link,i))
	return links



# if __name__ == "__main__":
# 	# soup = BeautifulSoup(html_doc, 'html.parser')
# 	html_page = request_page(PRODUCTS['phones'][0]['address'])
# 	# for type, products in PRODUCTS.iteritems():
# 	# 	for product in products:
# 	# html_page = request_page(product['address'])
# 	nr = 0
# 	soup = BeautifulSoup(html_page, 'html.parser')
# 	title_el = soup.find('h1', {'class': 'listing-page-title'}).select('span')[0]
# 	pages_no = get_pages_no(title_el.text)
# 	print pages_no
# 	links = product_links(PRODUCTS['phones'][0]['address'], pages_no)
# 	print links
# 	# for card in  soup.findAll("div", {"class" : "card-item"}):
# 	# 	price_element = card.find("p", {"class": "product-new-price"})
# 	# 	price = price_element.text
# 	# 	if price:
# 	# 		print nr
# 	# 		nr += 1
# 	# 		print card['data-name']
# 	# 		print price

