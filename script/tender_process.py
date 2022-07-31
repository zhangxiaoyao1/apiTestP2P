import logging
import random
import unittest

import requests

import app
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI
from utils import DButils, assert_utils, request_third_api


class test_tender_process(unittest.TestCase):
    phone = '13033447715'
    tender_id = 697
    imVerifyCode = '8888'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.tender_api = tenderAPI()
        cls.trust_api = trustAPI()
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.session.close()
        sql1 = "delete from mb_member_register_log where phone in" \
               "（'13033447711' , '13033447712' ,'13033447713' ,'13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql1)
        logging.info("delete sql = {}".format(sql1))

        sql2 = "delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in" \
               " ('13033447711' , '13033447712' ,'13033447713' ,'13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql2)
        logging.info("delete sql = {}".format(sql2))
        sql3 = "delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone in " \
               "('13033447711' , '13033447712' ,'13033447713' ,'13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql3)
        logging.info("delete sql = {}".format(sql3))
        sql4 = "delete from mb_member WHERE phone in " \
               "('13033447711' , '13033447712' ,'13033447713' ,'13033447714','13033447715');"
        DButils.delete(app.DB_MEMBER, sql4)
        logging.info("delete sql = {}".format(sql4))

    def test01_register_success(self):
        # 1、成功获取图片验证码
        r = random.random()
        # 调用接口类中的接口
        response = self.login_api.getImgCode(self.session, str(r))
        # 接收接口的返回结果，进行断言
        self.assertEqual(200, response.status_code)
        # 2、成功获取短信验证码
        # 定义参数（正确的手机号和验证码）
        # 调用接口类中的发送短信验证码的接口
        response = self.login_api.getSmsCode(self.session, self.phone, self.imVerifyCode)
        logging.info("get sms code response = {}".format(response.json()))
        # 对收到的响应结果，进行断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 3、成功注册——输入必填项
        # 调用接口类中的发送注册请求的接口
        response = self.login_api.register(self.session, self.phone, 'test123')
        logging.info("register response = {}".format(response.json()))
        # 对结果进行断言
        assert_utils(self, response, 200, 200, "注册成功")

    def test02_login_success(self):
        """登录成功"""
        # 准备参数
        # 调用接口类中的发送登录的接口
        response = self.login_api.login(self.session, self.phone, "test123")
        # 对结果进行断言
        assert_utils(self, response, 200, 200, '登录成功')

    def test03_trust_success(self):
        """开户"""
        # 获取开户信息
        response = self.trust_api.trust_register(self.session)
        logging.info('trust response = {}'.format(response.json()))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 3.获取开户信息响应中的html内容（为后续的请求地址和参数）
        from_data = response.json().get('description').get("form")
        logging.info('form response = {}'.format(from_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = request_third_api(from_data)
        logging.info('third-interface response = {}'.format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('UserRegister OK', response.text)

    def test04_recharge_success(self):
        """充值"""
        # 获取充值验证码
        r = random.random()
        response = self.trust_api.get_recharge_verify_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        logging.info('get recharge verify code response = {}'.format(response.text))

        # 充值
        amount = '1000'
        response = self.trust_api.recharge(self.session, amount)
        logging.info('recharge response = {}'.format(response.text))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 获取响应中form表单中的数据，并提取为后续第三方请求的参数
        form_data = response.json().get('description').get("form")
        logging.info('form response = {}'.format(form_data))
        # 调用第三方请求的接口
        response = request_third_api(form_data)
        logging.info('third recharge response = {}'.format(response.text))
        # 断言response是否正确
        self.assertEqual('NetSave OK', response.text)

    def test05_get_loaninfo(self):
        """获取投资产品详情"""
        # 请求投资产品的详情
        response = self.tender_api.get_loaninfo(self.session, self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        # 断言投资详情是否正确
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual('697', response.json().get("data").get("loan_info").get("id"))

    def test06_tender(self):
        """投资"""
        # 发送投资请求
        amount = '1000'
        response = self.tender_api.tender(self.session, self.tender_id, amount)
        logging.info('tender response = {}'.format(response.json()))
        # 断言投资结果是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 获取响应中form表单中的数据，并提取为后续第三方请求的参数
        form_data = response.json().get('description').get("form")
        logging.info('form response = {}'.format(form_data))
        # 调用第三方请求的接口
        response = request_third_api(form_data)
        logging.info('third-interface response = {}'.format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('InitiativeTender OK', response.text)

    def test07_get_tenderlist(self):
        """获取我的投资列表"""
        status = 'tender'
        response = self.tender_api.get_tenderlist(self.session, status)
        logging.info("get_tender response = {}".format(response.json))
        self.assertEqual(200, response.status_code)
