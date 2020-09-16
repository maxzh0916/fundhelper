import api
import setting
import push_msg

if __name__ == '__main__':
    data = []
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
        data.append((ttjjw.result(), xljj.result(), ajj.result(), jjmmw.result(), txcj.result()))
    push_msg.server_chan(data)
