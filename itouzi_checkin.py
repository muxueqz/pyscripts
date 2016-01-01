#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# 爱投资自动签到
# itouzi.com auto checkin
from selenium import webdriver
from time import sleep
from os import getenv
from random import randint

def main():
    useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
#    profile = webdriver.FirefoxProfile()
#    profile.set_preference("general.useragent.override", useragent)
#    driver = webdriver.Firefox(profile)

    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.settings.userAgent'] = useragent
    driver = webdriver.PhantomJS()
    driver.get('http://baidu.com')

    # 先登录
    url = 'https://www.itouzi.com/newuser/index/login?ret_url=http%3A%2F%2Fwww.itouzi.com'
    driver.get(url)

    username_input = driver.find_element_by_id("username")
    password_input = driver.find_element_by_id("password")

    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element_by_id("loginSubBtn").click()

    sleep(randint(60, 200))

    url = 'http://bbs.itouzi.com/plugin.php?id=dsu_paulsign:sign'
    driver.get(url)
    # 点击签到按钮
    last = driver.find_element_by_class_name("jifen").text.split('\n')[1]
    driver.find_element_by_class_name("qiandao").click()
    sleep(randint(60, 100))
    now = driver.find_element_by_class_name("jifen").text.split('\n')[1]
    print 'yesterday: %s, now: %s' % (last, now)
    driver.quit()

if __name__ == '__main__':
    username = getenv('itouzi_username')
    password = getenv('itouzi_password')
    main()
