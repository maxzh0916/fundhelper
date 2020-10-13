import requests
import setting
import time


def server_chan(name_dict, data_dict):
    text = str()
    for code in data_dict.keys():
        text = text + '======' + name_dict[code] + '======\n\n'
        for source in data_dict[code].keys():
            text = text + source + '：' + data_dict[code][source][
                0] + ', ' + str(data_dict[code][source][1]) + '%' + (
                    '↑' if data_dict[code][source][1] > 0 else '↓') + '\n\n'
    if setting.SERVER_CHAN_PUSH:
        params = {
            'text': time.strftime("%Y-%m-%d", time.localtime()) + '每日推送',
            'desp': text
        }
        response = requests.post('https://sc.ftqq.com/' + setting.SCKEY +
                                 '.send',
                                 data=params).json()
        if response['errmsg'] == 'success':
            print('推送成功')
        elif response['errmsg'] == 'bad pushtoken':
            print('SCKEY错误，请检查SCKEY')
        elif response['errmsg'] == '不要重复发送同样的内容':
            print('不要重复发送同样的内容')
