import api
import setting
import push_msg
from multiprocessing import Queue

if __name__ == '__main__':
    data_queue = Queue()

    # 检测交易时间
    if setting.TRADING_TIME:
        market_stat = api.market_stat()
        if not market_stat:
            print('非交易时间，退出程序')
            exit()

    # 启动进程
    for code in setting.FUND_LIST:
        ttjjw = api.TTJJW(code, data_queue)
        xljj = api.XLJJ(code, data_queue)
        ajj = api.AJJ(code, data_queue)
        jjmmw = api.JJMMW(code, data_queue)
        txcj = api.TXCJ(code, data_queue)
        processes = [ttjjw, xljj, ajj, jjmmw, txcj]
        for t in processes:
            if t.name in setting.SOURCE:
                t.start()

    while 1:
        try:
            print(data_queue.get_nowait())
        except:
            pass
    # push_msg.server_chan(data_queue)
