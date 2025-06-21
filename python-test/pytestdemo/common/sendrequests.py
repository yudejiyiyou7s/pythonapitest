import json
import pytest
import requests
import allure
from common.recordlog import logs
from common.readyaml import ReadYamlData
from requests import utils


class SendRequests:
    def __init__(self):
        self.read=ReadYamlData()

    def send_request(self,**kwargs):
        cookie={}
        session=requests.session()
        result=None
        try:
            result=session.request(**kwargs)
            set_cookie=requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie']=set_cookie
                self.read.write_yaml_data(set_cookie)
                logs.info(f'接口请求cookies:{cookie}')
            logs.info(f'接口实际返回信息:{result.text if result.text else result}')
        except requests.exceptions.ConnectionError:
            logs.error('接口连接服务器失败')
            pytest.fail('接口连接服务器失败')
        except requests.exceptions.HTTPError:
            logs.error('接口http异常')
            pytest.fail('接口http异常')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail(e)
        return result

    def run_main(self, name,url, case_name,header,method,cookies=None,file=None,**kwargs):
        # 收集报告日志信息
        try:
            logs.info(f'接口名称:{name}')
            logs.info(f'接口请求地址:{url}')
            logs.info(f'接口请求方法:{method}')
            logs.info(f'接口请求头:{header}')
            logs.info(f'接口测试名称:{case_name}')
            logs.info(f'接口请求cookies:{cookies}')
            # 处理请求参数
            req_params=json.dumps(kwargs, ensure_ascii=False)
            if 'data' in kwargs.keys():
                logs.info(f'接口请求参数:{kwargs}')
                # allure.attach(req_params,f'接口请求参数：{req_params}',allure.attachment_type.TEXT)
            elif 'json' in kwargs.keys():
                logs.info(f'接口请求参数:{kwargs}')
                # allure.attach(req_params,f'接口请求参数：{req_params}',allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f'接口请求参数:{kwargs}')
                # allure.attach(req_params,f'接口请求参数：{req_params}',allure.attachment_type.TEXT)
        except Exception as e:
            logs.error(e)
        response=self.send_request(url=url,method=method,headers=header,cookies=cookies,files=file,verify=False,**kwargs)
        return response



if __name__ == '__main__':
    url1 = 'http://127.0.0.1:8787/dar/user/login'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    data = {
        "user_name": "test01",
        "passwd": "admin123"
    }
    method = 'POST'
    res = SendRequests().run_main(url1, headers=None, data=data, method=method)
    print(res)

    token=res["token"]

    url2='http://127.0.0.1:8787/dar/user/addUser'
    headers={
        "Content-Type":"application/x-www-formurlencoded;charset=UTF-8"
    }
    data={
        "username":"testadduser",
        "password":"test6789890",
        "role_id":"123456789",
        "dates":"2023-12-31",
        "phone":"13800000000",
        "token":token
    }
    method="POST"
    res=SendRequests().run_main(url2,headers=headers,data=data,method=method)
    print(res)
