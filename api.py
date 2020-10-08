import requests
import multiprocessing
from parse import parse


def market_stat():
    """
    :return: 开市返回True 未开市返回False
    """
    response = requests.get('http://qt.gtimg.cn/?q=marketStat').text
    result = parse(
        'v_marketStat="{current_time}|{hk}_{hk_stat_en}_{hk_stat_zh}|{sh}_{sh_stat_en}_{sh_stat_zh}|{sz}_{sz_stat_en}_{sz_stat_zh}|{us}_{us_stat_en}_{us_stat_zh}|{sq}_{sq_stat_en}_{sq_stat_zh}|{ds}_{ds_stat_en}_{ds_stat_zh}|{zs}_{zs_stat_en}_{zs_stat_zh}|{newsh}_{newsh_stat_en}_{newsh_stat_zh}|{newsz}_{newsz_stat_en}_{newsz_stat_zh}|{newhk}_{newhk_stat_en}_{newhk_stat_zh}|{newus}_{newus_stat_en}_{newus_stat_zh}|{repo}_{repo_stat_en}_{repo_stat_zh}|{uk}_{uk_stat_en}_{uk_stat_zh}|{kcb}_{kcb_stat_en}_{kcb_stat_zh}|{it}_{it_stat_en}_{it_stat_zh}|{my}_{my_stat_en}_{my_stat_zh}|{eu}_{eu_stat_en}_{eu_stat_zh}|{ah}_{ah_stat_en}_{ah_stat_zh}|{de}_{de_stat_en}_{de_stat_zh}|{jw}_{jw_stat_en}_{jw_stat_zh}|{cyb}_{cyb_stat_en}_{cyb_stat_zh}|{usa}_{usa_stat_en}_{usa_stat_zh}|{usb}_{usb_stat_en}_{usb_stat_zh}";',
        response)
    if result['sh_stat_en'] == 'open' and result['sz_stat_en'] == 'open':
        return True
    else:
        return False


class TTJJW(multiprocessing.Process):
    def __init__(self, fund_code, data_dict, name_dict):
        multiprocessing.Process.__init__(self)
        self.fund_code = fund_code
        self.data_dict = data_dict
        self.name_dict = name_dict

    def run(self):
        response = requests.get('http://fundgz.1234567.com.cn/js/' + self.fund_code + '.js')
        status_code = response.status_code
        if status_code == 200:
            processed = parse('jsonpgz({"fundcode":"{code}","name":"{name}","jzrq":"{jztime}","dwjz":"{dwjz}","gsz":"{zxgz}","gszzl":"{chg}","gztime":"{gztime}"});', response.text)
            self.data_dict[self.fund_code]['天天基金网'].insert(0, processed['zxgz'])
            self.data_dict[self.fund_code]['天天基金网'].insert(1, processed['chg'] + '%')
            self.name_dict[self.fund_code] = processed['name']


class XLJJ(multiprocessing.Process):
    def __init__(self, fund_code, data_dict):
        multiprocessing.Process.__init__(self)
        self.fund_code = fund_code
        self.data_dict = data_dict

    def run(self):
        response = requests.get('https://hq.sinajs.cn/list=fu_' + self.fund_code).text
        processed = parse('var hq_str_fu_' + self.fund_code + '="{name},{time},{zxgz},{dwjz},{ljdwjz},{unknown},{chg},{date}";', response)
        try:
            self.data_dict[self.fund_code]['新浪基金'].insert(0, processed['zxgz'])
            self.data_dict[self.fund_code]['新浪基金'].insert(1, str(round(float(processed['chg']), 2)) + '%')
        except TypeError:
            pass


class AJJ(multiprocessing.Process):
    def __init__(self, fund_code, data_dict):
        multiprocessing.Process.__init__(self)
        self.fund_code = fund_code
        self.data_dict = data_dict

    def run(self):
        fund_data = requests.get('http://fund.10jqka.com.cn/data/client/myfund/' + self.fund_code).json()
        if fund_data['error']['id'] == 0:
            hq_code = fund_data['data'][0]['hqcode']
            response = requests.get('http://gz-fund.10jqka.com.cn/?module=api&action=chart&info=vm_fd_' + hq_code).text
            processed = parse(
                "vm_fd_" + hq_code + "='{date1};0930-1130,1300-1500|{date2}~{yesterday_value}~{chart}'",
                response)['chart'].split(';')
            for index in range(len(processed)):
                processed[index] = processed[index].split(',')
            self.data_dict[self.fund_code]['爱基金'].insert(0, str(round(float(processed[-1][1]), 4)))
            self.data_dict[self.fund_code]['爱基金'].insert(1, str(round(((float(processed[-1][1]) - float(processed[-1][2])) / float(processed[-1][2]) * 100), 2)) + '%')


class JJMMW(multiprocessing.Process):
    def __init__(self, fund_code, data_dict):
        multiprocessing.Process.__init__(self)
        self.fund_code = fund_code
        self.data_dict = data_dict

    def run(self):
        response = requests.get('http://www.jjmmw.com/fund/ajax/jjgz_timechart/?fund_id=' + self.fund_code).json()
        if response['flag'] == 1:
            self.data_dict[self.fund_code]['基金买卖网'].insert(0, str(round(response['latest']['estnav'], 4)))
            self.data_dict[self.fund_code]['基金买卖网'].insert(1, str(round(response['latest']['estchngpct'], 2)) + '%')


class TXCJ(multiprocessing.Process):
    def __init__(self, fund_code, data_dict):
        multiprocessing.Process.__init__(self)
        self.fund_code = fund_code
        self.data_dict = data_dict

    def run(self):
        response = requests.get('http://web.ifzq.gtimg.cn/fund/newfund/fundSsgz/getSsgz?app=web&symbol=jj' + self.fund_code).json()
        if response['code'] == 0:
            self.data_dict[self.fund_code]['腾讯财经'].insert(0, str(response['data']['data'][-1][1]))
            self.data_dict[self.fund_code]['腾讯财经'].insert(1, str(round((response['data']['data'][-1][2] / float(response['data']['yesterdayDwjz']) * 100), 2)) + '%')
