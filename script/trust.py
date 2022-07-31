import random
import unittest, logging, requests

from bs4 import BeautifulSoup
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from utils import assert_utils, request_third_api


class trust(unittest.TestCase):
    def setUp(self) -> None:
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 开户请求
    def test01_trust_request(self):
        # 1.认证通过的账号登录
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')

        # 2.发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info('trust response = {}'.format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 3.发送第三方的开户请求
        from_data = response.json().get('description').get("form")
        logging.info('form response = {}'.format(from_data))
        # 解析form表单中的内容，并提取第三方请求的参数

        soup = BeautifulSoup(from_data, 'html.parser')
        third_url = soup.form['action']
        logging.info('third request url = {}'.format(third_url))

        data = {}

        for input in soup.find_all('input'):
            data.setdefault(input['name'], input['value'])
        logging.info('third request data = {}'.format(data))

        response = requests.post(third_url, data=data)
        logging.info('third trust request = {}'.format(third_url))
        # 断言响应结果
        self.assertEqual(200, response.status_code)
        self.assertEqual('UserRegister OK', response.text)

    # 充值成功
    def recharge(self):
        # 1.登录成功
        response = self.login_api.login(self.session)
        logging.info('login response = {}'.format(response.json()))
        assert_utils(self, response, 200, 200, '登录成功')
        # 2.获取充值验证码
        r = random.random()
        logging.info(r)
        response = self.trust_api.get_recharge_verify_code_url(self.session, str(r))
        logging.info('get recharge verify code response = {}'.format(response.text))
        self.assertEqual(200, response.status_code)

        # 3.发送充值请求
        response = self.trust_api.recharge(self.session, '10000')
        logging.info('recharge response = {}'.format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get('status'))
        # 4.发送第三方充值请求
        # 获取响应中form表单中的数据，并提取为后续第三方请求的参数
        from_data = response.json().get('description').get("form")
        logging.info('form response = {}'.format(from_data))
        # 调用第三方请求的接口
        response = request_third_api(from_data)
        logging.info('third recharge response = {}'.format(from_data))
        # 断言response是否正确
        self.assertEqual('NetSave OK', response.text)
