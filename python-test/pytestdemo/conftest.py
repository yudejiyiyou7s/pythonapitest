import pytest
from common.recordlog import logs
from common.readyaml import ReadYamlData


read=ReadYamlData()
@pytest.fixture(scope="session",autouse=True)
def  clear_extract_data():
    """
    清除extract.yaml文件中的数据
    :return:
    """

    read.clear_extract_data()

@pytest.fixture(scope="session",autouse=True)
def fixture_test(request):
    """
    前后置处理
    :return:
    """
    logs.info('----------------------开始执行用例--------------------------')
    yield
    logs.info('----------------------用例执行结束--------------------------')

