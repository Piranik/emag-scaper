def get_last_price(product):
    prices = product.get('prices')
    if prices:
        return prices[-1]
    return None