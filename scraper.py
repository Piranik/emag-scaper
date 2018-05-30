import re
import logging
from bs4 import BeautifulSoup

import math
import re
import requests
import pika
import time

from storage.lib.emag_mongo_driver import EmagProductMongoDriver

LOG_FILENAME = 'example.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

PRODUCTS = {
    'phones': {
        'emag_address': ['https://www.emag.ro/telefoane-mobile/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/smartphone/'],
    },
    'tv': {
        'emag_address': ['https://www.emag.ro/telefoane-mobile/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/smartphone/'],
    },
    'video_cards': {
        'emag_address': ['https://www.emag.ro/placi_video/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/placi-video/'],
    },
    'processors': {
        'emag_address': ['https://www.emag.ro/procesoare/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/procesoare/'],
    },
    'motherboards': {
        'emag_address': ['https://www.emag.ro/placi_baza/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/placi-de-baza/'],
    },
    'ram-memory': {
        'emag_address': ['https://www.emag.ro/memorii/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/memorii/'],
    },
    'ssd-memory': {
        'emag_address': ['https://www.emag.ro/solid-state_drive_ssd_/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/ssd/'],
    },
    'hdd-memory': {
        'emag_address': ['https://www.emag.ro/hard_disk-uri/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/hard-disk-uri/']
    },
    'power-suply': {
        'emag_address': ['https://www.emag.ro/surse-pc/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/surse/']
    },
    'case': {
        'emag_address': ['https://www.emag.ro/carcase/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/carcase/']
    },
    'cooler': {
        'emag_address': ['https://www.emag.ro/coolere_procesor/c, https://www.emag.ro/coolere_hard_disk/c',
                         'https://www.emag.ro/ventilatoare-pc/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/coolere/']
    },
    'monitors': {
        'emag_address': ['https://www.emag.ro/monitoare-lcd-led/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/monitoare-led/']
    },
    'laptop': {
        'emag_address': ['https://www.emag.ro/laptopuri/c'],
        'pcgarage_address': ['https://www.pcgarage.ro/ultrabook/', 'https://www.pcgarage.ro/notebook-laptop-2-in-1/',
                             'https://www.pcgarage.ro/notebook-laptop/'],
    },
    'desktop-pc': {
        'emag_address': ['https://www.emag.ro/desktop-pc/c'],
        'pcgarage_address': [],
    }
}


def _data_is_useful(component, unnecessary_data):
    for data in unnecessary_data:
        if data in component:
            return False
    return True


def request_page(link):
    print link
    r = requests.get(link)
    return r.text


def get_pages_no(html_dom):
    title_el = html_dom.find('h1', {'class': 'listing-page-title'}).select('span')[1]
    title_pattern = re.compile('(\d+)( [\w|\'\" ]+)')
    page_no_pattern = re.compile('(\d+) (\w+) (\d+)')
    print title_el.text

    total_products = int(title_pattern.match(title_el.text).group(1))
    pages_no_ul = html_dom.find('ul', {'class': 'pagination'})
    print pages_no_ul
    pages_no_span = pages_no_ul.find('span', {'class': 'visible-xs visible-sm'})
    pages_no = int(page_no_pattern.match(pages_no_span.text).group(3))
    return pages_no


def category_links(main_link, pages_no):
    EMAG_LINK_START_PAGE_NO = 2
    return ['%s/p%d/c' % (main_link[:-2], i) for i in range(2, pages_no + 1)]


def correct_names(category, search_query, name):
    if category == 'mobile_phone' and search_query == 'iphone':
        name = name.replace('_grey', '_gray')
    return name

def emag_unique_names(category, product):
    unique_name = None
    unique_identifier = None
    if category == 'mobile_phone':
        emag_phone_prefix = 'telefon mobil'
        print product['name']
        try:
            prefix_pos = product['name'].lower().index(emag_phone_prefix)
            name_components = product['name'][prefix_pos + len(emag_phone_prefix):].lower().split(',')
            print name_components
            name_components = [component.strip().replace(' ', '_') for component in name_components]
            unique_name = '_'.join(name_components)
            unique_name = correct_names(category, 'iphone', unique_name)
        except ValueError as err:
            print 'cannot create unique identifier for %r' % product
    if category == 'tv':
        emag_tv_prefix = 'televizor'
        print product['name']
        try:
            # prefix_pos = product['name'].lower().index(emag_tv_prefix)
            # name_components = product['name'][prefix_pos + len(emag_tv_prefix):].lower().split(',')
            # print name_components
            # name_components = [component.strip().replace(' ', '_') for component in name_components]
            # unique_name = '_'.join(name_components)
            name_components = filter(
                lambda component: _data_is_useful(component, PRODUCTS['phones'][0]['emag']['remove_data']),
                product['name'].split(','))

            unique_identifier = name_components[PRODUCTS['phones'][0]['emag']['identifier_index']]
        except ValueError as err:
            print 'cannot create unique identifier for %r' % product

    return unique_name, unique_identifier

def pcgarage_unique_names(category, product):
    unique_name = None
    if category == 'mobile_phone':
        try :
            pcgarage_phone_prefix = 'smartphone'
            print product['name']
            prefix_pos = product['name'].lower().index(pcgarage_phone_prefix)
            name_components = product['name'][prefix_pos + len(pcgarage_phone_prefix):].lower().split(',')
            print name_components
            name_components = ([name_components[i] for i in PRODUCTS['phones'][1]['pcgarage']['name_indexes']] +
                name_components[-2:])
            unique_name = '_'.join(map(lambda component: component.strip().replace(' ', '_'), name_components))
            unique_name = correct_names(category, 'iphone', unique_name)
        except ValueError:
            print 'cannot create unique identifier for %r' % product

    return unique_name

unique_names_identifiers_dispatch = {
    'emag': emag_unique_names,
    'pcgarage': pcgarage_unique_names
}

# POC: try to create an unique identifier for all shops that we are looking to analyze
def get_unique_name(source_name, category, product):
    return unique_names_identifiers_dispatch[source_name](category, product)

def parse_products(html_dom, category):
    products = []
    for card in html_dom.findAll("div", {"class": "card-item"}):
        price = None
        product_link = None
        product_code = None
        price_element = card.find("p", {"class": "product-new-price"})
        price = price_element.text
        product_link_element = card.find("a", {"class": "js-product-url"})

        if product_link_element:
            product_link = product_link_element['href']
            product_html = BeautifulSoup(request_page(product_link), 'html.parser')
            product_code_element = product_html.find("span", {"class": "product-code-display"})
            if product_code_element:
                product_code = '_'.join(product_code_element.text.split(" ")[2:])[:-1]

        if price:
            try:
                name = card['data-name']
                name.replace(u'\xa0', '0')
                inserted_time = int(time.time())

                price = price.split(' ')[0]
                # remove dot if exists and place it after last two digits
                price = [digit for digit in price if digit != '.']
                price.insert(len(price) - 2, '.')
                price = ''.join(price)

                product = {
                    'category': category,
                    'name': name.strip(),
                    'prices': [
                        {'start_timestamp': inserted_time, 'finish_timestamp': inserted_time, 'value': float(price)}],
                    'product_id': product_code,
                    'link': product_link,
                    'created_at': inserted_time,
                    'updated_at': inserted_time
                }

                print 'Name %s, %s, %s, %s' % (
                product['name'], product['prices'], product['product_id'], product['link'])
                EmagProductMongoDriver().insert_product(product)
            except Exception as e:
                logging.error('Error encountered %s' %
                              ('Name %s, %s, %s, %s' % (product['name'], product['prices'], product['product_id'], product['link'])))
                logging.error(e)


            products.append(product)

    return products

def parse_emag_category(link):
    html_page = request_page(PRODUCTS['phones']['emag_address'][0])
    category = 'phones'
    html_dom = BeautifulSoup(html_page, 'html.parser')
    pages_no = get_pages_no(html_dom)
    links = category_links(PRODUCTS['phones']['emag_address'][0], pages_no)

    products = parse_products(html_dom, category)
    for link in links:
        html_page = request_page(link)
        html_dom = BeautifulSoup(html_page, 'html.parser')
        products.extend(parse_products(html_dom, category))

    return products


def parse_emag():
    return parse_emag_category(None)


def parse_pcgarage():
    html_page = request_page(PRODUCTS['phones'][1]['pcgarage']['address'])
    soup = BeautifulSoup(html_page, 'html.parser')
    for product in soup.findAll('div', {'class': 'product-box'}):
        name = product.find('a').get('title')
        price = product.find('p', {'class': 'price'}).text
        product = {
            'name': name.strip(),
            'price': price
        }
        print product
        print 'Name %s, %s' % get_unique_name('pcgarage', 'mobile_phone', product)


if __name__ == "__main__":
    parse_emag()
    # parse_pcgarage()
    # parse_pcgarage()
    # parse_pcgarage_page(html_page, 'iphone')
    # parse_emag(html, 'iphone')



