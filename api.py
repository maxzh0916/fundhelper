import requests
import threading
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


class TTJJW(threading.Thread):
    def __init__(self, fund_code):
        threading.Thread.__init__(self)
        self.fund_code = fund_code
        self.fund_name = str()
        self.evalue = str()
        self.chg = str()

    def run(self):
        response = requests.get('http://fundgz.1234567.com.cn/js/' + self.fund_code + '.js').text
        processed = parse('jsonpgz({"fundcode":"{code}","name":"{name}","jzrq":"{jztime}","dwjz":"{dwjz}","gsz":"{zxgz}","gszzl":"{chg}","gztime":"{gztime}"});', response)
        self.fund_name = processed['name']
        self.evalue = processed['zxgz']
        self.chg = processed['chg']

    def result(self):
        return self.fund_code, self.evalue, self.chg, self.fund_name, self.name


class XLJJ(threading.Thread):
    def __init__(self, fund_code):
        threading.Thread.__init__(self)
        self.fund_code = fund_code
        self.evalue = str()
        self.chg = str()

    def run(self):
        response = requests.get('https://hq.sinajs.cn/list=fu_' + self.fund_code).text
        processed = parse('var hq_str_fu_' + self.fund_code + '="{name},{time},{zxgz},{dwjz},{ljdwjz},{unknown},{chg},{date}";', response)
        self.evalue = processed['zxgz']
        self.chg = processed['chg']

    def result(self):
        return self.fund_code, self.evalue, self.chg, self.name


class AJJ(threading.Thread):
    def __init__(self, fund_code):
        threading.Thread.__init__(self)
        self.fund_code = fund_code
        self.evalue = str()
        self.chg = str()

    def run(self):
        fund_data = requests.get('http://fund.10jqka.com.cn/data/client/myfund/' + self.fund_code).json()
        hq_code = fund_data['data'][0]['hqcode']
        response = requests.get('http://gz-fund.10jqka.com.cn/?module=api&action=chart&info=vm_fd_' + hq_code).text
        processed = parse(
            "vm_fd_" + hq_code + "='{date1};0930-1130,1300-1500|{date2}~{yesterday_value}~{chart}'",
            response)['chart'].split(';')
        for index in range(len(processed)):
            processed[index] = processed[index].split(',')
        self.evalue = processed[-1][1]
        self.chg = str(round((float(processed[-1][1]) - float(processed[-1][2])) / float(processed[-1][2]), 4))


    def result(self):
        return self.fund_code, self.evalue, self.chg, self.name


class JJMMW(threading.Thread):
    def __init__(self, fund_code):
        threading.Thread.__init__(self)
        self.fund_code = fund_code

    def run(self):
        print(self.fund_code)

    def result(self):
        return 'jjmmw'


class TXCJ(threading.Thread):
    def __init__(self, fund_code):
        threading.Thread.__init__(self)
        self.fund_code = fund_code

    def run(self):
        print(self.fund_code)

    def result(self):
        return 'txcj'
