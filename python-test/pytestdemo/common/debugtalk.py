from common.readyaml import ReadYamlData
import random


class DebugTalk:
    def __init__(self):
        self.read = ReadYamlData()

    def get_extract_order_data(self, data, randoms):
        """
        顺序读取extract.yaml中的数据
        :param data: extract.yaml中的数据
        :param randoms: randoms代表第几个数据
        :return: 第randoms个数据
        """
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, sec_node_name=None):
        """
        获取extract.yaml中的数据
        :param node_name: extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        """
        data = self.read.get_extract_yaml(node_name,sec_node_name)

        return data

    def get_extract_data_list(self,node_name,randoms=None):
        """
        获取extract.yaml中的列表数据
        :param node_name: extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        """
        data = self.read.get_extract_yaml(node_name)

        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(',')
            }
            data = data_value[randoms]
        return data

    def md5_params(self, params):
        """
        实现md5加密
        :param params: 需要加密的字符串参数
        :return: 返回32位小写MD5加密字符串
        """
        import hashlib
        md5 = hashlib.md5()
        md5.update(params.encode('utf-8'))
        return md5.hexdigest()


if __name__ == '__main__':
    debugtalk = DebugTalk()
    print(type(debugtalk.get_extract_data('product_id', 3)))
