import json
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from cookie_pool import CookiePool
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

pool = CookiePool()
keys = pool.get_keys()
# keys = ['宁仁波']

for key in keys:
    cookie_get = pool.from_key_get_cookie(key)

    # 原手工获得
    # cookie_get = '''[{"domain": ".coze.cn", "expiry": 1716543186, "httpOnly": false, "name": "msToken", "path": "/", "sameSite": "None", "secure": true, "value": "N31QYw4AsITQp7gP4TmBIZdG1sedCgpUvJHGxjdcdvJEo2zQHHsaVDcmKFNkVEIKLNNGxRgMaMdOlPCI3Q32BMKrJveV2XGUIvKkH4hW"}, {"domain": ".coze.cn", "expiry": 1747474387, "httpOnly": true, "name": "store-region-src", "path": "/", "sameSite": "Lax", "secure": false, "value": "uid"}, {"domain": ".coze.cn", "expiry": 1747474387, "httpOnly": true, "name": "store-region", "path": "/", "sameSite": "Lax", "secure": false, "value": "cn-ah"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "sessionid_ss", "path": "/", "sameSite": "None", "secure": true, "value": "0ab6475d0dda01b42c82ca26ac5f9b18"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "sessionid", "path": "/", "sameSite": "Lax", "secure": false, "value": "0ab6475d0dda01b42c82ca26ac5f9b18"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "uid_tt_ss", "path": "/", "sameSite": "None", "secure": true, "value": "cc7d1776a061583ef0185fc9907bb626"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "uid_tt", "path": "/", "sameSite": "Lax", "secure": false, "value": "cc7d1776a061583ef0185fc9907bb626"}, {"domain": ".coze.cn", "expiry": 1718530387, "httpOnly": true, "name": "passport_auth_status_ss", "path": "/", "sameSite": "None", "secure": true, "value": "4c1a1723b35fe5e3145e16f4ee1b4c3b%2C"}, {"domain": ".coze.cn", "expiry": 1726306387, "httpOnly": true, "name": "n_mh", "path": "/", "sameSite": "Lax", "secure": false, "value": "kCDBxze9oPGf8i6oa5WKcMVhiM683JSna70bsrUJC7A"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": false, "name": "passport_csrf_token", "path": "/", "sameSite": "None", "secure": true, "value": "42baa84aca79f267c6e03706ca7a4c93"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": false, "name": "passport_csrf_token_default", "path": "/", "sameSite": "Lax", "secure": false, "value": "42baa84aca79f267c6e03706ca7a4c93"}, {"domain": ".coze.cn", "expiry": 1747474385, "httpOnly": true, "name": "ttwid", "path": "/", "sameSite": "None", "secure": true, "value": "1%7CJ_T5EBGpnXZ22lk4lezHR_eRAqICw_94M0qbPcuPsBQ%7C1715938386%7C3b4d16bf036d303ca4353703b9b2d7811b487233a0c8822cab9372cdc4d4cf81"}, {"domain": ".coze.cn", "expiry": 1747042387, "httpOnly": true, "name": "sid_guard", "path": "/", "sameSite": "Lax", "secure": false, "value": "0ab6475d0dda01b42c82ca26ac5f9b18%7C1715938388%7C5184000%7CTue%2C+16-Jul-2024+09%3A33%3A08+GMT"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "sid_ucp_v1", "path": "/", "sameSite": "Lax", "secure": true, "value": "1.0.0-KGJmOTFlYzg1MDY5ZjUyODk3MGQ1NjAxZmFiODI0ODAyMzZjY2EwNGEKHwjQofCMx8z1ARDUyJyyBhjHkB8gDDD-s5yyBjgIQCYaAmhsIiAwYWI2NDc1ZDBkZGEwMWI0MmM4MmNhMjZhYzVmOWIxOA"}, {"domain": ".coze.cn", "expiry": 1747474387, "httpOnly": true, "name": "d_ticket", "path": "/", "sameSite": "Lax", "secure": false, "value": "e09b82cec224506ed454d886d4d3ccd5c5f49"}, {"domain": ".coze.cn", "expiry": 1747474387, "httpOnly": true, "name": "odin_tt", "path": "/", "sameSite": "Lax", "secure": false, "value": "e560e1a7e39f8badce7814556b36329c594287ee38f7762b01775c9e38992b5b0e84d8cc9256f589b9984143d3af3e55578974c8f0d86e9fbafb12eaf8d7d0d0"}, {"domain": ".coze.cn", "expiry": 1718530387, "httpOnly": true, "name": "passport_auth_status", "path": "/", "sameSite": "Lax", "secure": false, "value": "4c1a1723b35fe5e3145e16f4ee1b4c3b%2C"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "sid_tt", "path": "/", "sameSite": "Lax", "secure": false, "value": "0ab6475d0dda01b42c82ca26ac5f9b18"}, {"domain": "www.coze.cn", "expiry": 1747474386, "httpOnly": false, "name": "i18next", "path": "/", "sameSite": "Strict", "secure": false, "value": "zh-CN"}, {"domain": ".coze.cn", "expiry": 1721122387, "httpOnly": true, "name": "ssid_ucp_v1", "path": "/", "sameSite": "None", "secure": true, "value": "1.0.0-KGJmOTFlYzg1MDY5ZjUyODk3MGQ1NjAxZmFiODI0ODAyMzZjY2EwNGEKHwjQofCMx8z1ARDUyJyyBhjHkB8gDDD-s5yyBjgIQCYaAmhsIiAwYWI2NDc1ZDBkZGEwMWI0MmM4MmNhMjZhYzVmOWIxOA"}, {"domain": "www.coze.cn", "expiry": 1716543177, "httpOnly": true, "name": "x-jupiter-uuid", "path": "/", "sameSite": "Lax", "secure": false, "value": "17159383785236268"}]'''
    # cookie_get = json.loads(cookie_get)
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.coze.cn/home')
    cookies = cookie_get
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    time.sleep(2)

    # 主页问答
    # driver.find_element(by=By.XPATH, value='//textarea[@class="rc-textarea textarea--oTXB57QK8bQN2BKYJ2Bi textarea--oTXB57QK8bQN2BKYJ2Bi"]').send_keys('你可以干什么')
    # driver.find_element(by=By.XPATH, value='//button[@class="semi-button semi-button-primary semi-button-size-small semi-button-borderless send-button--tqxhKsM_tI4KvPKo9dkI semi-button-with-icon semi-button-with-icon-only"]').click()

    # 切换到个人空间
    driver.find_element(by=By.XPATH,
                        value='//div[@class="item-inner--EUdR7GaW9jMUZmdET6Te" and contains(.//text(), "个人空间")]').click()
    time.sleep(1)
    # 选择目标机器人
    driver.find_element(by=By.XPATH, value='//a[@class="card-link--qE9ervT2yNAKfT4J70Mn"]').click()
    time.sleep(2)

    if_over = input('结束了吗？是请输入1:')
    if if_over == '1':
        driver.close()
        continue



# 输入框
# element = driver.find_element(by=By.XPATH, value='//textarea[@class="rc-textarea textarea--oTXB57QK8bQN2BKYJ2Bi textarea--oTXB57QK8bQN2BKYJ2Bi"]')  #.send_keys('你可以干什么')
# content = '今天天气怎么样'
# pyperclip.copy(content)
# element.send_keys(Keys.CONTROL, 'v')
# time.sleep(2)
# 发送
# driver.find_element(by=By.XPATH, value='//div[@class="textarea-actions-right--vr4WgM3FUuUicP3kJDOU"]').click()
#
# try:
#     WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div:nth-child(2) > div > div > div > div > div.container--aSIvzUFX9dAs4AK6bTj0 > div.sidesheet-container.wrapper-single--UMf9npeM8cVkDi0CDqZ0 > div.message-area--TH9DlQU1qwg_KGXdDYzk > div > div.scroll-view--R_WS6aCLs2gN7PUhpDB0.scroll-view--JlYYJX7uOFwGV6INj0ng > div > div > div.wrapper--nIVxVV6ZU7gCM5i4VQIL.message-group-wrapper > div > div > div:nth-child(1) > div > div > div > div > div.chat-uikit-message-box-container__message > div > div.chat-uikit-message-box-container__message__message-box__footer > div > div.message-info-text--tTSrEd1mQwEgF4_szmBb > div:nth-child(3) > div > div')))
#     print('已经出现元素')
# except:
#     print('超时或者未出现等待元素')
# content = driver.find_element(by=By.XPATH, value='//div[@class="auto-hide-last-sibling-br paragraph_4183d"]').text
# if isinstance(content, list):
#     content = ''.join(content)
# content = json.loads(content)
# print(content)
