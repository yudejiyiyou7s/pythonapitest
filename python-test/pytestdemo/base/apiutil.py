import re
import allure
import json
import jsonpath
from common.debugtalk import DebugTalk
from common.readyaml import ReadYamlData, get_testcase_yaml
from common.sendrequests import SendRequests
from conf.operationConfig import OperationConfig
from common.recordlog import logs
from common.assertions import Assertions
assert_res=Assertions()

class BaseRequests:

    def __init__(self):
        self.read = ReadYamlData()
        self.conf = OperationConfig()
        self.send = SendRequests()

    def replace_load(self, data):
        """
        yaml文件替换解析有${}格式的数据
        :return:
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
            print(type(str_data))
        for i in range(str_data.count("${")):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                print('索引', start_index, end_index)
                ref_all_param = str_data[start_index:end_index + 1]
                print('取出的部分', ref_all_param)
                func_name = ref_all_param.replace("${", "").replace("}", "")
                func_name = ref_all_param[2:ref_all_param.index('(')]
                print('函数名', func_name)
                func_param = ref_all_param[ref_all_param.index('(') + 1:ref_all_param.index(')')]
                print('函数参数', func_param)

                extract_data = getattr(DebugTalk(), func_name)(*func_param.split(',') if func_param else '')
                print('提取数据', extract_data)
                print(type(extract_data))
                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_param, str(extract_data))
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification(self, case_info):
        """
        规范yaml测试用例的写法
        :param case_info: list类型，调试取case_info[0]-->dict
        :return:
        """

        params_type = ['params', 'data', 'json']
        cookie = None
        try:
            base_url = self.conf.get_section_for_data('api_envi', 'host')
            # base_url=self.replace_load(case_info['baseInfo']['rul'])
            url = base_url + case_info['baseInfo']['url']
            allure.attach(url, f'接口地址：{url}')
            api_name = case_info['baseInfo']['api_name']
            allure.attach(api_name, f'接口名称：{api_name}')
            method = case_info['baseInfo']['method']
            allure.attach(method, f'接口请求方法：{method}')
            headers = case_info['baseInfo']['headers']
            allure.attach(str(headers), f'接口请求头：{headers}')
            try:
                cookie = self.replace_load(case_info['baseInfo']['cookies'])
                allure.attach(cookie, f'cookie:{cookie}', allure.attachment_type.TEXT)
            except:
                pass

            for ci in case_info['testCase']:

                case_name = ci.pop('case_name')
                allure.attach(case_name, f'测试用例名称：{case_name}')

                validation = ci.pop('validation')

                extract = ci.pop('extract', None)
                extract_list = ci.pop('extract_list', None)

                for key, value in ci.items():
                    if key in params_type:
                        ci[key] = self.replace_load(value)

                res = self.send.run_main(name=api_name, url=url, case_name=case_name, header=headers, method=method,
                                         **ci)
                res_text = res.text
                res_json=res.json()
                print("原始内容",res_text)
                allure.attach(res.text, f'接口响应信息：{case_name}', allure.attachment_type.TEXT)

                if extract is not None:
                    self.extract_data(extract, res_text)
                if extract_list is not None:
                    self.extract_data(extract_list, res_text)

                #处理断言
                assert_res.assert_result(validation,res_json,res.status_code)
        except Exception as e:
            logs.error(e)
            raise e

    def extract_data(self, testcase_extract, response):
        """
        提取接口的返回值，支持正则表达式提取以及json提取
        :param testcase_extract: yaml文件中extract的值
        :param response: 接口的实际返回值
        :return:
        """
        pattern_list = ['(.+?)', '(.*?)', r'(\d+)', r'(\d*)']
        print('提取', testcase_extract)
        try:
            for key, value in testcase_extract.items():
                print(key, value)
                for pattern in pattern_list:
                    if pattern in value:
                        print('正则表达式', pattern)
                        ext_list = re.search(value, response)
                        if pattern in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_list.group(1))}
                        else:
                            extract_data = {key: ext_list.group(1)}
                        logs.info(f'正则表达式提取的参数为：{extract_data}')
                        self.read.write_yaml_data(extract_data)
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    print('json', ext_json)
                    if ext_json:
                         extract_data = {key: ext_json}
                    else:
                        extract_data = {key: None}
                    print('json提取', extract_data)
                    logs.info(f'json提取的参数为：{extract_data}')
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常')

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式提取以及json提取, 结果以列表形式返回
        :param testcase_extract_list: yaml文件中extract_list的值
        :param response: 接口的实际返回值,str类型
        :return:
        """
        pattern_list = ['(.+?)', '(.*?)', r'(\d+)', r'(\d*)']
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_data = {key: ext_list}
                        logs.info("正则表达式提取的参数%s" % extract_data)
                        self.read.write_yaml_data(extract_data)
                if "$" in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_data = {key: ext_json}
                    else:
                        extract_data = {key: None}
                    logs.info("json提取的参数%s" % extract_data)
                    self.read.write_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常')


if __name__ == '__main__':
    # data=get_testcase_yaml('login.yaml')
    # print(type(data))
    base = BaseRequests()
    data = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    base.specification(data)
    # base.replace_load(data)
