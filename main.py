import api
import setting

if __name__ == '__main__':
    if setting.TREADING_TIME:
        market_stat = api.market_stat()
        if not market_stat:
            print('非交易时间，退出程序')
            exit()

    for code in setting.FUND_LIST:
        ttjjw = api.TTJJW(code)
        xljj = api.XLJJ(code)
        ajj = api.AJJ(code)
        jjmmw = api.JJMMW(code)
        txcj = api.TXCJ(code)
        threads = [ttjjw, xljj, ajj, jjmmw, txcj]
        for t in threads:
            t.start()
            t.join()

        print(ttjjw.result(), xljj.result(), ajj.result(), jjmmw.result(), txcj.result())
