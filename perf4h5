# -*- coding: UTF-8 -*-
# Date: 2020-03-08
# Author: fuzhuang.zhou
"""
    整页时间：loadEventEnd-navigationStart
    domready时间：domContentLoadedEventEnd - navigationStart
    解析 DOM 树结构的时间：domComplete - responseEnd
    白屏时间 ：responseStart - navigationStart
    内容加载完成的时间：responseEnd - requestStart
    执行 onload 回调函数的时间：loadEventEnd - loadEventStart
"""

from selenium import webdriver
import time
import threading
import argparse

load_time = list()
# responseEnd - fetchStart
responseEnd = list()
# domInteractive - responseEnd
domInteractive = list()
# domContentLoadedEventEnd - domInteractive
domContentLoadedEventEnd = list()


def concurrency_run(n=1):
    """
    :param n: 需要并发的次数
    :return:
    """
    def wrap_func(func):
        def inner(*args, **kwargs):
            for i in range(n):
                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.start()
        return inner
    return wrap_func


def get_result_time(time_list):
    print("最大加载时间：%sms" % max(time_list))
    print("最小加载时间：%sms" % min(time_list))
    ave = sum(time_list) / len(time_list)
    print("平均加载时间：%sms" % ave)


def get_page_time():
    print("执行次数：%s次" % len(load_time))
    print("****************** 整页加载时间 *****************")
    get_result_time(load_time)


def get_response_end_time():
    print("***************** responseEnd *****************")
    get_result_time(responseEnd)


def get_dom_interactive_time():
    print("**************** domInteractive ****************")
    get_result_time(domInteractive)


def get_dom_load_end_time():
    print("************ domContentLoadedEventEnd ***********")
    get_result_time(domContentLoadedEventEnd)


def data_handle(page_data):
    execute_time = round(page_data["duration"], 0)
    print(execute_time)
    if 5000 > execute_time > 300:
        load_time.append(execute_time)
    responseEnd.append(round(page_data["responseEnd"] - page_data["fetchStart"], 0))
    if page_data["domInteractive"] - page_data["responseEnd"] > 100:
        domInteractive.append(round(page_data["domInteractive"] - page_data["responseEnd"], 0))
    domContentLoadedEventEnd.append(round(page_data["domContentLoadedEventEnd"] - page_data["domInteractive"], 0))


# @concurrency_run(1)
def surfing(_url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)
    try:
        driver.get(_url)
    except Exception as e:
        print(e)
    time.sleep(3)
    data = driver.execute_script("return window.performance.getEntries()")
    # data = driver.execute_script("return window.performance.timing")
    # execute_time = round(data[0]["duration"], 0)
    # print(data[0])
    # print(execute_time)
    # if 5000 > execute_time > 500:
    #     load_time.append(execute_time)
    driver.quit()
    return data[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=True, type=int, help="循环次数")
    parser.add_argument('-t', help="文章类型")
    parser.add_argument('-u', required=True, help="文章url")
    args = parser.parse_args()
    count = int(args.l)
    url = args.u
    name = args.t
    while count > 0:
        data = surfing(url)
        time.sleep(5)
        count = count - 1
        print(count)
        data_handle(data)

    print("******************** 测试%s *******************:" % name)
    get_page_time()
    get_response_end_time()
    get_dom_interactive_time()
    get_dom_load_end_time()
