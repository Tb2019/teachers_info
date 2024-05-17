from selenium import webdriver
import time
import loguru
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

driver.get('https://www.coze.cn/space/7369789547451875382/bot/7369789715555926053')
time.sleep(1)
driver.find_element(by=By.XPATH, value='//span[@class="semi-checkbox-inner-display"]').click()
driver.find_element(by=By.XPATH, value='//input[@class="semi-input semi-input-default"]').send_keys('17355385975')
driver.find_element(by=By.XPATH, value='//span[@class="semi-button-content"]').click()
loguru.logger.info('请扫码登录')
# time.sleep(10)  # 设置固定等待扫码的时间
while True:  # 不固定等待时间
    try:
        sucess_index = driver.find_element(by=By.XPATH, value='//div[@class="des--LwdZfGwrna85Y4fCeLBR"]')
    except:
        sucess_index = None
    try:
        success_bot = driver.find_element(by=By.XPATH, value='//div[@class="left-sheet-config--PLf9q929mqs4ZlidOgkc"]')
    except:
        success_bot = None
    if sucess_index or success_bot:
        loguru.logger.info('登录成功')
        break
    else:
        loguru.logger.info('等待扫码中...')
        time.sleep(2)

cookie_get = driver.get_cookies()
print(cookie_get)

driver.delete_all_cookies()
time.sleep(5)
driver.refresh()

driver.get('https://www.coze.cn/space/7369789547451875382/bot/7369789715555926053')
cookies = cookie_get
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()
