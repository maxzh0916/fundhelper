import api

fund_list = []

if __name__ == '__main__':
    market_stat = api.market_stat()
    if market_stat:
        print('get fund value')
