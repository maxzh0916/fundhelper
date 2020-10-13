import api
import check
import push_msg

import multiprocessing

if __name__ == '__main__':
    check.trading_time()  # 检查交易时间
    fund_list = check.code()  # 检查基金代码，并返回正确的列表
    source_list = check.source()  # 检查数据来源，并返回正确的基金列表

    # 通信相关
    manager = multiprocessing.Manager()
    data_dict = manager.dict()
    name_dict = manager.dict()
    for code in fund_list:
        data_dict[code] = manager.dict(
            {source: manager.list()
             for source in source_list})
        name_dict[code] = str()

    # 进程相关
    pool = list()
    # 启动爬虫
    for code in fund_list:
        get_name = api.Get_Name(code, name_dict)
        pool.append(get_name)
        if '天天基金网' in source_list:
            ttjjw = api.TTJJW(code, data_dict)
            pool.append(ttjjw)
        if '新浪基金' in source_list:
            xljj = api.XLJJ(code, data_dict)
            pool.append(xljj)
        if '爱基金' in source_list:
            ajj = api.AJJ(code, data_dict)
            pool.append(ajj)
        if '基金买卖网' in source_list:
            jjmmw = api.JJMMW(code, data_dict)
            pool.append(jjmmw)
        if '腾讯财经' in source_list:
            txcj = api.TXCJ(code, data_dict)
            pool.append(txcj)
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    push_msg.server_chan(name_dict, data_dict)
