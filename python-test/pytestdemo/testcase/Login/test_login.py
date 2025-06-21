import shutil
import time
import allure
import os
import pytest
import subprocess
from common.readyaml import  get_testcase_yaml
from common.sendrequests import SendRequests
from base.apiutil import BaseRequests

# @allure.feature('登录接口')
class TestLogin:

    # @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize('params',get_testcase_yaml('login.yaml'))
    def test_case01(self,params):
        BaseRequests().specification(params)




if __name__ == '__main__':
    # 使用subprocess运行pytest，这样不会影响当前进程
    subprocess.run(["pytest"], shell=True)
    # 后续代码一定会执行
    shutil.copy(r'D:\pycharm\code\python-test\pytestdemo\environment.xml',r'D:\pycharm\code\python-test\pytestdemo\testcase\Login\allure-results')
    print('ok')



