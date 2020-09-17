import requests
import setting
import time


def server_chan(data):
    text = str()
    for i in data:
        if i[0]:
            text = text + '=====' + i[0][3] + i[0][0] + '=====\n\n'
            text = text + '天天基金网：' + i[0][1] + ',' + i[0][2] + '\n\n'
        if i[1]:
            text = text + '新浪基金：' + i[1][1] + ',' + i[1][2] + '\n\n'
        if i[2]:
            text = text + '爱基金：' + i[2][1] + ',' + i[2][2] + '\n\n'
        if i[3]:
            text = text + '基金买卖网：' + i[3][1] + ',' + i[3][2] + '\n\n'
        if i[4]:
            text = text + '腾讯财经：' + i[4][1] + ',' + i[4][2] + '\n\n\n\n'
    if setting.SERVER_CHAN_PUSH:
        params = {'text': time.strftime("%Y-%m-%d", time.localtime()) + '每日推送',
                  'desp': text
                  }
        response = requests.post('https://sc.ftqq.com/' + setting.SCKEY + '.send', data=params).json()
        if response['errmsg'] == 'success':
            print('推送成功')
        elif response['errmsg'] == 'bad pushtoken':
            print('SCKEY错误，请检查SCKEY')
