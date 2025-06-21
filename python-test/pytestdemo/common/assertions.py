import operator

import allure
import jsonpath

from common.recordlog import logs
from common.connection import ConnectMysql


class Assertions:
    """
    断言封装
    1.字符串包含
    2.结果相等断言
    3.结果不相等断言
    4.断言接口返回值里面的任意一个值
    5.数据库断言
    """

    def contains_assert(self,value,response,status_code):
        """
        字符串包含断言 断言预期结果中的字符串是否包含在接口的实际返回中
        :param value: 预期结果
        :param response: 实际结果
        :status_code: 状态码
        """
        flag=0
        for assert_key,assert_value in value.items():
            if assert_key =="status_code":
                if assert_value !=status_code:
                    flag=1
                    allure.attach('预期结果',f'{assert_value}\n,实际结果{status_code}','响应代码断言失败',allure.attachment_type.TEXT)
                    logs.error(f"contains断言失败，状态码断言失败，预期结果{assert_value},实际结果{status_code}")
            else:
                resp_list=jsonpath.jsonpath(response,'$..%s' %assert_key)
                print('resp_list:',resp_list)
                print('resp_list[0]:',type(resp_list[0]))
                if isinstance(resp_list[0],str):
                    resp_list=''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        logs.info(f'响应文本断言结果：成功，预期结果{assert_value}\n,实际结果{resp_list}')

                else:
                    flag=1
                    logs.error(f'响应文本断言结果：失败，预期结果{assert_value}\n,实际结果{resp_list}')
                    allure.attach('预期结果',f'{assert_value}\n,实际结果{resp_list}','响应文本断言失败',allure.attachment_type.TEXT)
        return flag

    def equal_assert(self,value,response):
        """
        结果相等断言
        :param value: 预期结果
        :param response: 实际结果

        """
        flag=0
        res_list=[]
        print('eq中的value:',value)
        if isinstance(value,dict) and isinstance(response,dict):

            # 处理实际结果的数据结构，保持与预期结果的数据结构一致
            print('1', list(value.keys())[0])
            print('2', list(value.keys()))
            print('3', value.keys())
            for res in response:
                print('res:',res)

                if list(value.keys())[0] !=res:
                    res_list.append(res)
            print('res_list',res_list)
            for rl in res_list:
                del response[rl]
            print(f'实际结果:{response}')
            # 通过判断实际结果的字典和预期结果的字典是否相等来判断断言是否通过
            eq_asser=operator.eq(response,value)
            if eq_asser:
                logs.info(f'相等断言成功：接口的实际结果{response}与预期结果{value}相等')
            else:
                flag=1
                logs.error(f'相等断言失败：接口的实际结果{response}与预期结果{value}不相等')
        else:
            raise TypeError('类型错误')
        return flag


    def not_equal_assert(self,value,response):
        """
        结果不相等断言
        :param value: 预期结果
        :param response: 实际结果

        """
        flag = 0
        res_list = []
        if isinstance(value, dict) and isinstance(response, dict):
            # 处理实际结果的数据结构，保持与预期结果的数据结构一致
            for res in response:
                print(res)
                print(list(value.keys())[0])
                if list(value.keys()[0]) != res:
                    res_list.append(res)
            print(res_list)
            for rl in res_list:
                del response[rl]
            print(f'实际结果:{response}')
            # 通过判断实际结果的字典和预期结果的字典是否相等来判断断言是否通过
            eq_asser = operator.ne(response, value)
            if eq_asser:
                logs.info(f'不相等断言成功：接口的实际结果{response}与预期结果{value}不相等')
            else:
                flag = 1
                logs.error(f'不相等断言失败：接口的实际结果{response}与预期结果{value}相等')
        else:
            raise TypeError('类型错误')
        return flag

    def assert_mysql(self,expected_sql):
        """
        数据库断言
        :param expected_sql: yaml文件中的sql语句
        :return: 0通过，非0失败
        """
        flag=0
        conn=ConnectMysql()
        dv_value=conn.query(expected_sql)
        if dv_value:
            logs.info('数据库断言成功')
        else:
            flag=1
            logs.error('数据库断言失败,数据库检查是否存在此数据')
        return flag

    def in_assert(self,value,response):
        """
        断言接口返回值里面的任意一个值
        """
        pass


    def assert_result(self,expected,response,status_code):
        """
        断言结果
        :param value: 预期结果
        :param response: 实际结果
        :status_code: 状态码
        """
        all_flag=0
        try:
            for yq in expected:
                print('yq:',yq)
                for key,value in yq.items():
                    print('key:',key)
                    print('value:',value)
                    if key =='contains':
                        flag=self.contains_assert(value,response,status_code)
                        all_flag+=flag
                    elif key =='eq':
                        flag=self.equal_assert(value,response)
                        all_flag+=flag
                    elif key=='ne':
                        flag=self.not_equal_assert(value,response)
                        all_flag+=flag
                    elif key=='db':
                        flag=self.assert_mysql(value)
                        all_flag+=flag

            assert all_flag==0
            logs.info('断言成功')
        except Exception as e:
            logs.error('断言失败')
            logs.error(f'异常信息：{e}')
            assert all_flag==0



