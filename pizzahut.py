# 获取必胜客在全国的餐厅的地点
# 包括 城市、餐厅名字、地址、电话、有无早餐、支付方式

import requests
import random
from urllib import parse  # 用于对中文进行rul编码
import time  # 获取时间戳，用于cookie
from lxml import etree
import csv

# 随机选取 user-agent
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 S'
    'afari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.307'
    '29; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.96'
    '3.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NE'
    'T CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Ver'
    'sion/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Vers'
    'ion/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 M'
    'obile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Versio'
    'n/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10',
    'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 S'
    'afari/534.13',
    'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobi'
    'le Safari/534.1+',
    'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.7'
    '0 Safari/534.6 TouchPad/1.0',
    'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) Appl'
    'eWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)',
    'UCWEB7.0.2.37/28/999',
    'NOKIA5700/ UCWEB7.0.2.37/28/999',
    'Openwave/ UCWEB7.0.2.37/28/999',
    'Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999',

]
Hm_lvt_time = time.time()


def get_city():  # 返回一个用于获取城市名字的函数
    require_time_temp = time.time()
    city_temp_code = parse.quote('北京市')
    head_temp = dict()
    head_temp['User-Agent'] = random.choice(user_agent_list)
    head_temp = {
        'Host': 'www.pizzahut.com.cn',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://www.pizzahut.com.cn/StoreList',
        'Cookie': 'AlteonP=CbvNbQnySd5XtVBH7ETDBQ$$; gr_user_id=83cd48d2-531e-47fd-a7'
                  '84-b0fe52d46cfd; _u_=1; Hm_lvt_7226f1398a8a1aae74384b0f7635de6f={}; H'
                  'm_lpvt_7226f1398a8a1aae74384b0f7635de6f={}; __Request'
                  'VerificationToken=l-u_u_Y4mMgknlYj-x9JQI-qTR3yuQzb8Zf9qvU_lD_iMWltIuv'
                  'GkKKAl6Hs1-qFceT2huTPaLHYNZFIlbVxd011FC0B3Yr1dWd9c-jjuwPe32FIv-8WaJUG'
                  'KWXWNXq8qHhNcO5AaN6_OUst3ntBbw2; gr_session_id_a58d28f5fdbbcb8b=e9179'
                  'cb1-90b9-4a4d-9726-f1a9ff04ad5b; gr_session_id_a58d28f5fdbbcb8b_e917'
                  '9cb1-90b9-4a4d-9726-f1a9ff04ad5b=tr'
                  'ue; iplocation={}%7C0%7C0'.format(Hm_lvt_time, require_time_temp, city_temp_code)
    }
    response_for_cityname = requests.post(url='http://www.pizzahut.com.cn/StoreList',
                                          headers=head_temp,
                                          )
    response_for_cityname.encoding = 'utf-8'

    return response_for_cityname


def city_circle(response):  # 每一列表页的response
    # 获取省份和其城市
    resultlx = etree.HTML(response.text)
    prov_divs = resultlx.xpath('//div[@class="city_window"]')[0].xpath('.//div[@class="this_f_letters"]')
    # 省份列表
    city_dict = dict()  # 键名是省份，键值是省内城市的列表
    for prov_div in prov_divs:  # 遍历省份
        city_temp_list = []
        aas = prov_div.xpath('.//a')
        prov_name = aas[0].xpath('./strong/text()')[0]  # 省份名称
        # print(prov_name)
        for a in aas[1:]:  # 遍历省内城市
            city_name = a.xpath('./text()')[0]
            city_temp_list.append(city_name)
            # print(city_name)
            # break
        city_dict[prov_name] = city_temp_list  # 创建一个 省份-城市 字典
    return city_dict
    # #####


def get_each_info(response):

    # 获取餐厅信息
    resultlx = etree.HTML(response)
    divs = resultlx.xpath('//div[@class="re_RNew"]')
    for div in divs:
        list_for_csv_temp = []
        name = div.xpath('.//p[1]/text()')[0]
        list_for_csv_temp.append(name)
        addr = div.xpath('.//p[2]/text()')[0]
        list_for_csv_temp.append(addr)
        tele = div.xpath('.//p[3]/text()')[0]
        list_for_csv_temp.append(tele)
        # print(name, '\n', addr, '\n', tele)
        divs_imgs = div.xpath('./div//img')
        if divs_imgs:
            # for div_img in divs_imgs:
            #     item = div_img.xpath('./@alt')[0].strip()  # 有无早餐，礼品卡，支付宝
            #     list_for_csv_temp.append(item)
            #     # print(item, end='--')
            map(lambda x: list_for_csv_temp.append(x.xpath('./@alt')[0].strip()), divs_imgs)
        print('写入csv')
        writer.writerow(list_for_csv_temp)
        # print('\n')
    # ######


def get_listpage(cityname):

    # ajax 翻页

    for i in range(1, 100):  # Ajax 加载应该不会超过 100 页
        require_time = time.time()
        city_code = parse.quote(cityname)
        head = dict()
        head['User-Agent'] = random.choice(user_agent_list)
        head = {
            'Host': 'www.pizzahut.com.cn',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'http://www.pizzahut.com.cn/StoreList',
            'Cookie': 'AlteonP=CbvNbQnySd5XtVBH7ETDBQ$$; gr_user_id=83cd48d2-531e-47fd-a7'
                      '84-b0fe52d46cfd; _u_=1; Hm_lvt_7226f1398a8a1aae74384b0f7635de6f={}; H'
                      'm_lpvt_7226f1398a8a1aae74384b0f7635de6f={}; __Request'
                      'VerificationToken=l-u_u_Y4mMgknlYj-x9JQI-qTR3yuQzb8Zf9qvU_lD_iMWltIuv'
                      'GkKKAl6Hs1-qFceT2huTPaLHYNZFIlbVxd011FC0B3Yr1dWd9c-jjuwPe32FIv-8WaJUG'
                      'KWXWNXq8qHhNcO5AaN6_OUst3ntBbw2; gr_session_id_a58d28f5fdbbcb8b=e9179'
                      'cb1-90b9-4a4d-9726-f1a9ff04ad5b; gr_session_id_a58d28f5fdbbcb8b_e917'
                      '9cb1-90b9-4a4d-9726-f1a9ff04ad5b=tr'
                      'ue; iplocation={}%7C0%7C0'.format(Hm_lvt_time, require_time, city_code)
        }
        data = {
            'pageIndex': str(i),
            'pageSize': "10",
        }
        response = requests.post(url='http://www.pizzahut.com.cn/StoreList/Index',
                                 headers=head,
                                 data=data)
        time.sleep(2)  # 请求完等 2s
        response.encoding = 'utf-8'
        resultlx_temp = etree.HTML(response.text)
        divs = resultlx_temp.xpath('//div[@class="re_RNew"]')  # 判断是否获取到真实的内容
        # 如果在这个城市下，已经遍历完所有的餐厅信息，虽然还能获取到网页内容，但是已经没用了。
        if divs:
            get_each_info(response.text)  # 调用函数
            # 直接传入解析的函数，不用return
        # print(response.text)
        else:
            print('没有下一页了')
            break


if __name__ == '__main__':
    file = open('information.csv', 'a', newline='')
    writer = csv.writer(file)
    init_page = get_city()  # 获取一个初始的网页，来找出所有的省份和城市
    prov_city_all = city_circle(init_page)  # 把所有城市按照省份整理在一个字典里
    for prov in prov_city_all:
        print('-'*30, prov, '-'*30)
        writer.writerow([prov])
        writer.writerow(['餐厅', '地址', '电话'])
        for each_city in prov_city_all[prov]:
            print('-'*15, prov, '---', each_city)
            get_listpage(each_city)
