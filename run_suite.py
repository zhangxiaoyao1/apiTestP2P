import time
import unittest
import app
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
from script.login import login

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))

report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S)"))
with open(report_file, "wb") as f:
    runner = HTMLTestRunner(f, title="P2P金融项目接口测试报告", description="test")
    runner.run(suite)
