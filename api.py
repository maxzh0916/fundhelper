import requests
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

