from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVistorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start(self):
        # 小A假期在家做题，突然有道题不会了，想去论坛上问问
        # 他打开网站
        self.browser.get('http://127.0.0.1:8000')

        # 注意到网页的标题是“Login”
        self.assertIn('Login', self.browser.title)

        # 输入用户名密码，登录
        input_username = self.browser.find_element_by_id('username')
        input_username.send_keys('test')
        input_pw = self.browser.find_element_by_id('password')
        input_pw.send_keys('test1234')
        input_pw.send_keys(Keys.ENTER)

        # 他看到提示说账号或密码错误
        error_message = self.browser.find_element_by_id('error_message')
        self.assertIn('账号或密码错误', error_message.text)

        # 重新输入
        input_username = self.browser.find_element_by_id('username')
        input_username.send_keys('test')
        input_pw = self.browser.find_element_by_id('password')
        input_pw.send_keys('test12345')
        input_pw.send_keys(Keys.ENTER)

        # 登录成功，跳转到首页，他看到标题是“DonghuBBS”
        self.assertIn('DonghuBBS', self.browser.title)

        # 他点击导航栏的你问我答链接
        self.browser.find_element_by_link_text('你问我答').click()

        # 在下面输入框输入标题和内容，点击发表
        input_title = self.browser.find_element_by_id('title')
        input_title.send_keys('问一道高数题，求定积分')
        input_content = self.browser.find_element_by_id('content')
        input_content.send_keys(r'$$\int_1^2(x^2+\frac{1}{x^4})dx$$')
        input_submit = self.browser.find_element_by_id('submit').click()

        # 他看到页面自动刷新，他发的内容已经显示出来了
        title = self.browser.find_element_by_class_name('listGroup')
        self.assertIn('问一道高数题，求定积分', title.text)

        # 以一个预期的错误结束测试
        self.fail('结束测试!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')