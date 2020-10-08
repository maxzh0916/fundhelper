import api
import setting
import re


def trading_time():
    if setting.TRADING_TIME:
        market_stat = api.market_stat()
        if not market_stat:
            print('非交易时间，退出程序')
            exit()


def code():
    fund_list = []
    re_fund_list = re.compile('^\\d{6}$')
    for i in setting.FUND_LIST:
        try:
            result = re.match(re_fund_list, i).group()
            fund_list.append(result)
        except AttributeError:
            print(str(i) + ' 不是正确的基金代码，请检查后再试')
    return fund_list


def source():
    source_list = []
    for i in setting.SOURCE_LIST:
        if i == '天天基金网':
            source_list.append('天天基金网')
        elif i == '新浪基金':
            source_list.append('新浪基金')
        elif i == '爱基金':
            source_list.append('爱基金')
        elif i == '基金买卖网':
            source_list.append('基金买卖网')
        elif i == '腾讯财经':
            source_list.append('腾讯财经')
        else:
            print(str(i) + ' 不是正确的数据来源，请检查后再试')
    return source_list
