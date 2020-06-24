# -*- coding: UTF-8 -*-
# Date: 2020-03-08
# Author: fuzhuang.zhou
"""
    整页加载耗时：loadEventEnd - navigationStart
    白屏时间：domInteractive - navigationStart
    Dom解析耗时：domInteractive - domLoading
    Dom解析完资源加载时间 ：domContentLoadedEventEnd - domContentLoadedEventStart	
    整个dom结构解析时间：domComplete - domLoading
"""

from selenium import webdriver
import time
import argparse

load_time = list()
blank_time = list()
dom_parse_time = list()
load_source_time = list()
whole_dom_time = list()

cookie = "lianjia_uuid=c0cbcd95-ccff-49b6-a3f8-24c6024468fd; crosSdkDT2019DeviceId=-caz51p--wl8nrs-flpv6rnn1i1ss8s-w41wl8ght; HC_AA=379f3397836ccc0a51f85a539f0cc570; _smt_uid=5eb648ef.3e536a1b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22171f80cc1d33fd-06269beb4c7c37-30647d01-2073600-171f80cc1d4410%22%2C%22%24device_id%22%3A%22171f80cc1d33fd-06269beb4c7c37-30647d01-2073600-171f80cc1d4410%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; dorami_city=%255B%2522110000%2522%252C%2522%25u5317%25u4EAC%2522%252C%252211%2522%255D; dorami_client=mzhan; gr_user_id=b44142ab-ade1-47de-af66-4714a4c0dda9; grwng_uid=5ee9fb0c-2507-477b-a57a-83964a4842c2; login_ucid=1000000026522267; security_ticket_test=Pq6rOLqDSl14Y022UGjBp01gsU+b146Ohu7/FE9ri4pG5Dd8nWQcyPtM23PHmXxnncYswbS52McMgNRH08CofEekhwTKjYBBUqnbtwSppuAczaHYX47hiNBssNBLF8X/ihp7Aa/MAVCwYtAvbo22aM6i8ffMMzrsYMGCPzVatQU=; hc_token_bucky=2.006c9e07a5f9d7cf517d37b917aaf99f90; hc_token_bucky.sig=jFkv2BxgzsHKBkgvU4gvUiU6MLE; lianjia_ssid=3499cae4-f6ef-4802-a625-9e6ae5f17d84; security_ticket=es9TCr2RewPqGYO4j2AV34trm6BBqvIuW/qsmasbbD8xdJqboZ3Jh5ntpCYQOwyWvweXJEAtYWLyrwGl7a3OzKV325/TpyDL3u3exsRBV/wUuS1DJTXdfaS6jeW3E+Qc4F0ObrQHIGY0fXkHozGPfX2IEZ1lWLEueT7yrB0oHfs="


# 将cookie string转换成dict
def format_cookie():
    c = cookie.split(";")
    cookie_dict = {}
    for i in c:
        l = i.split("=")
        cookie_dict[l[0].strip()] = l[1]
    return cookie_dict


def print_timing():
    print("执行次数：%s次" % len(load_time))
    print("****************** 整页加载时间 *****************")
    get_result_time(load_time)
    print("****************** 白屏时间 *****************")
    get_result_time(blank_time)
    print("****************** Dom解析耗时 *****************")
    get_result_time(dom_parse_time)
    print("****************** Dom解析完资源加载时间 *****************")
    get_result_time(load_source_time)
    print("****************** 整个dom结构解析时间时间 *****************")
    get_result_time(whole_dom_time)


# 计算最大时间、最小时间、平均时间
def get_result_time(time_list):
    """
    :param time_list: 多次测试获取到的统计时间列表
    :return:
    """
    print("最大加载时间：%sms" % max(time_list))
    print("最小加载时间：%sms" % min(time_list))
    ave = sum(time_list) / len(time_list)
    print("平均加载时间：%sms" % int(ave))


# 统一打印页面统计时间
def handle_timing(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    get_page_time(page_timing)
    get_blank_time(page_timing)
    get_dom_parse_time(page_timing)
    get_source_time(page_timing)
    get_whole_dom_time(page_timing)


# 获取整页加载时间数据
def get_page_time(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    execute_time = page_timing["loadEventEnd"] - page_timing["navigationStart"]
    if 5000 > execute_time > 300:
        load_time.append(execute_time)


# 获取白屏统计时间数据
def get_blank_time(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    execute_time = page_timing["domInteractive"] - page_timing["navigationStart"]
    blank_time.append(execute_time)


# 获取dom解析耗时数据
def get_dom_parse_time(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    execute_time = page_timing["domInteractive"] - page_timing["domLoading"]
    dom_parse_time.append(execute_time)


# 获取dom解析完资源加载时间数据
def get_source_time(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    execute_time = page_timing["domContentLoadedEventEnd"] - page_timing["domContentLoadedEventStart"]
    load_source_time.append(execute_time)


# 整个dom结构解析时间数据
def get_whole_dom_time(page_timing):
    """
    :param page_timing: 页面统计数据
    :return:
    """
    execute_time = page_timing["domComplete"] - page_timing["domLoading"]
    whole_dom_time.append(execute_time)


# 浏览网页
def surfing(_url, need_login):
    """
    :param _url: 要测试的url
    :return: 统计的时间数据
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    if need_login:
        driver.get(_url)
        cookie_formatter = format_cookie()
        for k, v in cookie_formatter.items():
            cookie_dict = {'name': k, 'value': v, 'domain': 'm-dora.shoff.ke.com'}
            driver.add_cookie(cookie_dict)
    driver.set_page_load_timeout(10)
    try:
        driver.get(_url)
    except Exception as e:
        print(e)
    time.sleep(3)
    # data = driver.execute_script("return window.performance.getEntries()")
    page_timing = driver.execute_script("return window.performance.timing")
    driver.quit()
    return page_timing


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=True, type=int, help="循环次数")
    parser.add_argument('-n', help="测试名称")
    parser.add_argument('-u', required=True, help="文章url")
    parser.add_argument('-b', help="是否需要登陆，true or false")
    args = parser.parse_args()
    count = int(args.l)
    url = args.u
    name = args.n
    need_login = True if args.b == "true" else False
    while count > 0:
        data = surfing(url, need_login)
        time.sleep(5)
        count = count - 1
        handle_timing(data)
    print("******************** %s测试 *******************:" % name)
    print_timing()
