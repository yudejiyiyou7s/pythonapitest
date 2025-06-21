import shutil

import pytest
import os
if __name__ == "__main__":
    pytest.main()
    shutil.copy(r'D:\pycharm\code\python-test\pytestdemo\environment.xml',
                r'D:\pycharm\code\python-test\pytestdemo\testcase\Login\allure-results')
    os.system(f'allure serve D:/pycharm/code/python-test/pytestdemo/testcase/Login/allure-results')