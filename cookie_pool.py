from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from loguru import logger
import redis

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

class CookiePool:
    def __init__(self,host='localhost', port=6379, password='123456', db=1):
        self.user_name = input('请输入你的姓名:')
        # self.phone_num = input('请输入你的电话号码:')
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def get_cookie(self):
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://www.coze.cn/home')
        time.sleep(1)
        self.driver.find_element(by=By.XPATH, value='//span[@class="semi-checkbox-inner-display"]').click()  # 同意协议
        self.driver.find_element(by=By.XPATH, value='//span[@class="semi-button-content"]').click()  # 选择抖音登录
        # self.driver.find_element(by=By.XPATH, value='//input[@class="semi-input semi-input-default"]').send_keys(self.phone_num)  # 填写号码
        # self.driver.find_element(by=By.XPATH, value='//span[@class="semi-button-content"]').click()  # 提交号码登录

        logger.info('请扫码登录')
        logger.info('等待扫码中...')

        while True:  # 不固定等待时间
            try:
                sucess_index = self.driver.find_element(by=By.XPATH, value='//div[@class="logo--ygHzgHcQawt_wjEH3kdX facade--RXmt6TFgUUaz4nGd61fY"]')
            except:
                sucess_index = None
            # try:
            #     success_bot = self.driver.find_element(by=By.XPATH,
            #                                       value='//div[@class="left-sheet-config--PLf9q929mqs4ZlidOgkc"]')
            # except:
            #     success_bot = None
            # if sucess_index or success_bot:
            if sucess_index:
                logger.info('登录成功')
                break
            else:
                time.sleep(2)

        self.cookie_get = json.dumps(self.driver.get_cookies())
        print(self.cookie_get)

        self.driver.delete_all_cookies()
        time.sleep(2)
        self.driver.refresh()
        self.driver.close()

        self.save_cookie(self.cookie_get)
        logger.info('cookie保存成功')

    def save_cookie(self, cookie):
        self.db.sadd(self.user_name, cookie)

    def random_get_cookie(self):
        pass


if __name__ == '__main__':
    CookiePool().get_cookie()
