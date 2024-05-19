from selenium import webdriver
import time

from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

cookie_get = [{'domain': '.coze.cn', 'expiry': 1716520177, 'httpOnly': False, 'name': 'msToken', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'ZyeTg2e6AMPjUTI4Ubl4gpJdMeADgOgbqDCEA3_iHuBsGrXJk-7EUJ_AaDG-0Oq5l78c-w52zMQ87x1i4c4PRdN_VRJjD9AEkl3d-HFs'}, {'domain': '.coze.cn', 'expiry': 1747451377, 'httpOnly': True, 'name': 'store-region-src', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'uid'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'ssid_ucp_v1', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1.0.0-KGFjN2JkNTRlNDc2NTNhMDk3YmQwM2VmZGJhYjZiNjRmOTE3ZDBkM2YKHwiUk9DgxsyRBBDxlJuyBhjHkB8gDDDTgpuyBjgIQCYaAmxxIiBkMzhhNGMzNjg5ODUyNzExNDA3NDZlYTBjZGFhZWRmZA'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'sessionid_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'd38a4c368985271140746ea0cdaaedfd'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'sessionid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'd38a4c368985271140746ea0cdaaedfd'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'uid_tt_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': 'a47f1d065ddd0a5b250fd2b64abced0c'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'uid_tt', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'a47f1d065ddd0a5b250fd2b64abced0c'}, {'domain': '.coze.cn', 'expiry': 1718507377, 'httpOnly': True, 'name': 'passport_auth_status_ss', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '113ff33af8441af07d32d141525e106e%2C'}, {'domain': '.coze.cn', 'expiry': 1726283377, 'httpOnly': True, 'name': 'n_mh', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'PBPLPX8Wz3JwOLEjR3H5ZMLBXfiaMZ0iO2BBvwlSnQY'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': False, 'name': 'passport_csrf_token', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '5a8835e605ad0c91fa74c951d2761ae2'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': False, 'name': 'passport_csrf_token_default', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '5a8835e605ad0c91fa74c951d2761ae2'}, {'domain': '.coze.cn', 'expiry': 1747451375, 'httpOnly': True, 'name': 'ttwid', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': '1%7CochV48RDuXcKETxohN4CdJjMlqn1YgqXRm3KOV_z1vc%7C1715915376%7Cd729a6fb58ed6ecc408f631a9729b6bdf94118afa564af0159e537b1776b5cc8'}, {'domain': '.coze.cn', 'expiry': 1747019377, 'httpOnly': True, 'name': 'sid_guard', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'd38a4c368985271140746ea0cdaaedfd%7C1715915377%7C5184000%7CTue%2C+16-Jul-2024+03%3A09%3A37+GMT'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'sid_ucp_v1', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': '1.0.0-KGFjN2JkNTRlNDc2NTNhMDk3YmQwM2VmZGJhYjZiNjRmOTE3ZDBkM2YKHwiUk9DgxsyRBBDxlJuyBhjHkB8gDDDTgpuyBjgIQCYaAmxxIiBkMzhhNGMzNjg5ODUyNzExNDA3NDZlYTBjZGFhZWRmZA'}, {'domain': '.coze.cn', 'expiry': 1747451377, 'httpOnly': True, 'name': 'd_ticket', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1152ebb367a87853d7ede9889d0a9e6bbd4e6'}, {'domain': '.coze.cn', 'expiry': 1747451377, 'httpOnly': True, 'name': 'odin_tt', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '64e06daaffc184c204034886d0bedcd3d666a79bc7031b8ecd45665cc690af78c5d761e9fda3d5556170264e7570b54deddf07a24288ee84b3d16475d028851c'}, {'domain': '.coze.cn', 'expiry': 1718507377, 'httpOnly': True, 'name': 'passport_auth_status', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '113ff33af8441af07d32d141525e106e%2C'}, {'domain': '.coze.cn', 'expiry': 1721099377, 'httpOnly': True, 'name': 'sid_tt', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'd38a4c368985271140746ea0cdaaedfd'}, {'domain': 'www.coze.cn', 'expiry': 1747451376, 'httpOnly': False, 'name': 'i18next', 'path': '/', 'sameSite': 'Strict', 'secure': False, 'value': 'zh-CN'}, {'domain': '.coze.cn', 'expiry': 1747451377, 'httpOnly': True, 'name': 'store-region', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'cn-ah'}, {'domain': 'www.coze.cn', 'expiry': 1716520169, 'httpOnly': True, 'name': 'x-jupiter-uuid', 'path': '/space/7369789547451875382/bot', 'sameSite': 'Lax', 'secure': False, 'value': '17159153705071666'}]


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
driver.find_element(by=By.XPATH, value='//div[@class="item-inner--EUdR7GaW9jMUZmdET6Te" and contains(.//text(), "个人空间")]').click()
time.sleep(1)
# 选择目标机器人
driver.find_element(by=By.XPATH, value='//a[@class="card-link--qE9ervT2yNAKfT4J70Mn"]').click()
time.sleep(1)
# 输入框
driver.find_element(by=By.XPATH, value='//textarea[@class="rc-textarea textarea--oTXB57QK8bQN2BKYJ2Bi textarea--oTXB57QK8bQN2BKYJ2Bi"]').send_keys('你可以干什么')
# 发送
driver.find_element(by=By.XPATH, value='//div[@class="textarea-actions-right--vr4WgM3FUuUicP3kJDOU"]').click()

# # sucess_index = driver.find_element(by=By.XPATH, value='//div[@class="des--LwdZfGwrna85Y4fCeLBR"]')
# success_bot = driver.find_element(by=By.XPATH, value='//div[@class="left-sheet-config--PLf9q929mqs4ZlidOgkc"]')
# print(success_bot)