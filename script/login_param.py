import logging
import random
import unittest
from time import sleep
from parameterized import parameterized
import requests

from api.loginAPI import loginAPI
from utils import assert_utils, read_imgVerify_data, read_register_data, read_param_data


class login(unittest.TestCase):
    phone1 = '13033447711'
    phone2 = '13033447712'
    phone3 = '13033447713'
    phone4 = '13033447714'
    pwd = 'test123'
    imgCode = '8888'
    smsCode = '666666'

    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # @parameterized.expand(read_imgVerify_data("imgVerify.json"))
    @parameterized.expand(read_param_data("imgVerify.json", "test_get_img_verify_code", "type,status_code"))
    def test01_get_img_code(self, type, status_code):
        # 根据不同的type类型准备不同的参数数据
        r = ''
        if type == 'float':
            r = random.random()
        elif type == 'int':
            r = random.random(10000000, 90000000)
        elif type == 'char':
            r = ''.join(random.sample('abcdefghijklmn'), 8)
        # 发送请求
        response = self.login_api.getImgCode(self.session, r)
        # 对响应结果进行断言
        self.assertEqual(status_code, response.status_code)

    # @parameterized.expand(read_register_data("register.json"))
    @parameterized.expand(read_param_data("register.json", "test_register",
                                          "phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone, status_code, status,description"))
    def test10_register(self, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone, status_code, status,
                        description):
        # 1. 获取图片验证码成功
        # 定义参数
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接受接口中的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2. 获取短信验证码成功
        # 定义参数(正确的手机号和验证码)
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, phone, self.imgCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 接受接口中的返回结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3. 使用参数化的测试数据进行注册，并返回对应的结果
        # 发送注册请求
        response = self.login_api.register(self.session, phone, pwd, imgVerifyCode, phoneCode, dyServer, invite_phone)
        logging.info("register response = {}".format(response.json()))
        # 对收到的响应进行断言
        assert_utils(self, response, status_code, status, description)


if __name__ == '__main__':
    unittest.main()
