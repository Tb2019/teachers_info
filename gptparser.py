from selenium import webdriver
from selenium.webdriver.common.by import By
from cookie_pool import CookiePool
import time

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

class GptParser:
    def __init__(self):
        self.pool = CookiePool()

    def init_driver(self):
        cookies = self.pool.random_get_cookie()
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.coze.cn/home')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()

        time.sleep(2)

        # 切换到个人空间
        driver.find_element(by=By.XPATH,
                            value='//div[@class="item-inner--EUdR7GaW9jMUZmdET6Te" and contains(.//text(), "个人空间")]').click()
        time.sleep(1)
        # 选择目标机器人
        driver.find_element(by=By.XPATH, value='//a[@class="card-link--qE9ervT2yNAKfT4J70Mn"]').click()
        time.sleep(1)

        return driver
