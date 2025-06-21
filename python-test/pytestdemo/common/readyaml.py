import yaml
import os

from conf.setting import FILE_PATH



def get_testcase_yaml(file):
    """
    获取yaml文件内容
    :param file: yaml文件路径
    :return:
    """
    try:
        with open(file, 'r', encoding='utf-8') as file:
            yaml_data = yaml.safe_load(file)
            return yaml_data
    except Exception as e:
        print(e)

class ReadYamlData:
    """
    读取并写入yaml文件内容
    """
    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = '../testcase/Login/login.yaml'

    def write_yaml_data(self,value):
        """
        写入yaml文件内容
        :param value: (dict)写入数据
        :return:
        """
        file_path= FILE_PATH['extract']

        try:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(value, f, allow_unicode=True, default_flow_style=False)
            with open(file_path, 'a', encoding='utf-8') as f:
                if isinstance(value, dict):
                    yaml.dump(value, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(e)

    def get_extract_yaml(self,node_name):
        """
        读取接口提取的变量值
        :param node_name: yaml文件的key值
        :return:
        """

        file_ptah= FILE_PATH['extract']

        if os.path.exists(file_ptah):
            pass
        else:
            print('extract.yaml文件不存在')
            open('file_ptah', 'w', encoding='utf-8').close()
            print('extract.yaml文件已创建')

        with open(file_ptah, 'r', encoding='utf-8') as f:
            extract_data=yaml.safe_load(f)
            return extract_data[node_name]

    def clear_extract_data(self):
        """
        清除extract.yaml文件中的数据
        :return:
        """
        file_path= FILE_PATH['extract']
        with open(file_path, 'w', encoding='utf-8') as f:
            f.truncate()

if __name__ == '__main__':
    # res = get_testcase_yaml('login.yaml')[0]
    # url = res['baseInfo']['url']
    # new_url = 'http://127.0.0.1:8787' + url
    # method = res['baseInfo']['method']
    # data = res['testCase'][0]['data']
    # result=get_testcase_yaml('login.yaml')
    # print(result)
    #
    # from sendrequests import SendRequests
    #
    # res = SendRequests().run_main(new_url, headers=None, data=data, method=method)
    # print(res)

    # token=res['token']
    # print(token)
    #
    # write_data={}
    # write_data['token']=token
    # ReadYamlData().write_yaml_data(write_data)
    # print(ReadYamlData().get_extract_yaml('product_id'))
    print(get_testcase_yaml(r'D:\pycharm\code\python-test\pytestdemo\testcase\Login\login.yaml'))
    print(get_testcase_yaml(r'D:\pycharm\code\python-test\pytestdemo\testcase\Login\login.yaml')[0]['baseInfo']['headers'])



