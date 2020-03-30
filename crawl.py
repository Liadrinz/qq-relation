# -*- coding: utf-8 -*-
import os
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config import root, data_path, data_root, begin

if not os.path.exists(data_root):
    os.mkdir(data_root)
if not os.path.exists(data_root + data_path):
    os.mkdir(data_root + data_path)
print('正在启动浏览器...')
print('浏览器启动后请在页面登录，然后才能开启爬虫')
try:
    browser = webdriver.Firefox()
except:
    print('请安装火狐浏览器: http://www.firefox.com.cn/')
    exit(0)
try:
    wait = WebDriverWait(browser, 60)
    browser.get(root)
    wait.until(lambda drv : '留住感动' not in drv.title)
    blog_list = []
    ffl = wait.until(lambda _ : browser.find_element_by_id('feed_friend_list'))
    browser.execute_script('setInterval(() => {window.scrollBy(0, 60)})')
    print('爬虫开始')
except TimeoutException:
    browser.quit()
    print('登录超时，请重启后在1分钟内完成登录')
    exit(0)

def loop():
    fpc = None
    browser.find_element_by_id('tab_menu_friend').click()
    for i in range(10000):
        print('正在爬取第{0}页，请不要关闭或手动跳转页面...'.format(i))
        if i == 0:
            blog_list.append(browser.execute_script("return document.getElementById('feed_friend_list').innerHTML"))
        else:
            if fpc is None:
                fpc = wait.until(lambda _ : ffl.find_element_by_class_name('feed_page_container'))
            blog_list.append(browser.execute_script("return document.getElementsByClassName('feed_page_container')[0].getElementsByTagName('ul')[0].innerHTML"))
        if len(blog_list) >= 10:
            content = json.dumps(blog_list, ensure_ascii=False)
            with open('{0}/{1}/html_chunk{2}.json'.format(data_root, data_path, int(begin) + i // 10), 'wb') as f:
                f.write(content.encode('utf-8'))
            blog_list.clear()
        def loaded(drv):
            wait.until(lambda _ : ffl.find_element_by_class_name('feed_page_container'))
            if len(browser.execute_script("return document.getElementsByClassName('feed_page_container')[0].getElementsByTagName('ul')")) == 0:
                return False
            return int(browser.execute_script("return document.getElementsByClassName('feed_page_container')[0].getElementsByTagName('ul')[0].getAttribute('data-page')")) >= i - 1
        wait.until(loaded)

def main():
    try:
        loop()
    except TimeoutException:
        browser.quit()
    browser.quit()
    print('爬取空间动态结束')

if __name__ == '__main__':
    main()