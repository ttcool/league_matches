'''
爬取suning商品信息:
    请求url:
        https://www.suning.com/
    提取商品信息:
        1.商品详情页
        2.商品名称
        3.商品价格
        4.颜色
'''
from selenium import webdriver
from selenium.webdriver import  Chrome,ChromeOptions
from urllib.request import urlopen, urlretrieve
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from multiprocessing import Process
import pandas as pd
from lxml import etree
import time, requests
import csv
import os
import subprocess

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


def link_to_url(link):
    try:
        r = requests.get(link, headers=headers)
        r.raise_for_status
        r.encoding = 'utf-8'
        return r.text
    except:
        print('此页无法链接！！！')
        return ''

def imgDownload(imgUrl,img_name):
    urlretrieve(imgUrl, '%s.jpg'%img_name)

# 解析提取商品详细信息
def get_good_name_from_text(context):
    try:
        soup = BeautifulSoup(context, 'lxml', from_encoding="utf-8")
        # 商品名称
        good_name = soup.select(".breadcrumb-title")[0].attrs['title']
        # 商品颜色
        good_color = soup.find_all("li", class_="clr-item")

        # 商品详细参数
        good_param = []
        res_elements = etree.HTML(context)
        # 指定属性的获取方式
        table = res_elements.xpath('//table[@id="bzqd_tag"]')
        table = etree.tostring(table[0], encoding='utf-8').decode()
        # pandas读取table
        df = pd.read_html(table, encoding='utf-8', header=0)[0]
        # 转换成列表嵌套字典的格式
        results = list(df.T.to_dict().values())
        # 最后能够看到一个包含很多字典的list
        #print('包装清单',results)
        good_param.append(('包装清单', results[0].get('包装清单.1')))
        res_elements = etree.HTML(context)
        table1 = res_elements.xpath('//table[@id="itemParameter"]')
        table1 = etree.tostring(table1[0], encoding='utf-8').decode()
        # pandas读取table
        df1 = pd.read_html(table1, encoding='utf-8', header=0)[0]
        # 转换成列表嵌套字典的格式
        results1 = list(df1.T.to_dict().values())
        # 最后能够看到一个包含很多字典的list
        for i in results1:
            #print(i)
            good_param.append((i.get('主体'), i.get('主体.1')))

        color_list = []
        for i in good_color:
            color_list.append(i.attrs["title"])
        return good_name, ','.join(color_list), good_param
    except:
        print('无法解析数据')
        return ''


def get_good(driver):
    try:
        # 通过JS控制滚轮滑动获取所有商品信息
        js_code = '''
            window.scrollTo(0,4000);
        '''
        driver.execute_script(js_code)  # 执行js代码

        # 等待数据加载
        time.sleep(10)

        # 查找所有商品div
        good_list = driver.find_elements_by_class_name('product-box')
        n = 1
        for good in good_list:
            # 根据属性选择器查找
            # 商品链接
            good_url = good.find_element_by_css_selector(
                '.res-info .title-selling-point a').get_attribute('href')
            # 商品图片img
            good_img_url = good.find_element_by_css_selector(
                '.res-img .img-block a img').get_attribute('src')

            good_sa_data = good.find_element_by_css_selector(
                '.res-info .title-selling-point a').get_attribute('sa-data')
            # 商品ID
            good_prd_id = (good_sa_data.split(',')[1]).split(':')[1]
            # 商品店铺ID
            good_shop_id = (good_sa_data.split(',')[2]).split(':')[1]

            # 商品店铺名称
            good_shop_name = good.find_element_by_css_selector(
                '.res-info .store-stock a').text
            # 商品评论数
            good_prd_evaluate = ''
            try:
                good_prd_evaluate = good.find_element_by_css_selector('.res-info .evaluate-old .info-evaluate a').text
            except:
                with open('suning_mobile_fail.csv', 'a', newline="", encoding='utf-8') as f:
                    csv_writer = csv.writer(f, delimiter='|')
                    csv_writer.writerow([good_url,good_prd_id])
            # 商品价格
            good_price = good.find_element_by_css_selector(
                '.res-info .price-box .def-price').text

            #p = Process(target=imgDownload, args=(good_img_url,good_shop_id,))
            #p.start()
            #p.join()
            context = link_to_url(good_url)
            good_content = []
            if get_good_name_from_text(context):
                good_name, good_color, good_param = get_good_name_from_text(context)

                good_content = [
                    good_prd_id,
                    good_shop_id,
                    good_shop_name,
                    good_prd_evaluate,
                    good_img_url,
                    good_name,
                    good_price,
                    good_url,
                    good_color,
                    good_param
                ]

            else:
                with open('suning_mobile_fail.csv', 'a', newline="", encoding='utf-8') as f:
                    csv_writer = csv.writer(f, delimiter='|')
                    csv_writer.writerow([good_url,good_prd_id])

            if good_content:
                import json
                with open('suning_mobile_success.csv', 'a', newline="", encoding='utf-8') as f:
                    csv_writer = csv.writer(f, delimiter='|')
                    csv_writer.writerow(good_content)
            

        next_tag = driver.find_element_by_id('nextPage')
        next_tag.click()
        time.sleep(10)
        # 递归调用函数
        get_good(driver)
        time.sleep(10)
    finally:
        driver.close()


if __name__ == '__main__':
    # good_name = input('请输入爬取商品信息:').strip()
    good_name = "手机"
    opt = ChromeOptions()  # 创建Chrome参数对象
    opt.add_argument('--no-sandbox')
    opt.headless = True  # 把Chrome设置成可视化无界面模式，windows/Linux 皆可
    opt.webdriver = 'chromedriver'
    binary_location = '/usr/bin/google-chrome'
    chrome_driver_binary= './chromedriver'
    os.environ["webdriver.chrome.driver"] = chrome_driver_binary
    driver = Chrome(executable_path='./chromedriver',options=opt)  # 创建Chrome无界面对象
    driver.implicitly_wait(50)
    # 1、往苏宁主页发送请求
    driver.get('https://www.suning.com/')

    # 2、输入商品名称，并回车搜索
    input_tag = driver.find_element_by_id('searchKeywords')
    input_tag.send_keys(good_name)
    input_tag.send_keys(Keys.ENTER)
    time.sleep(2)

    get_good(driver)
