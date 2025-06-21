import pymysql
from common.recordlog import logs
from conf.operationConfig import OperationConfig
conf=OperationConfig()

class ConnectMysql:
    """
    连接读取mysql数据库
    """

    def __init__(self):
        mysql_conf = {
            'host': conf.get_section_for_data('MYSQL','host'),
            'port': int(conf.get_section_for_data('MYSQL','port')),
            'user': conf.get_section_for_data('MYSQL','user'),
            'password': conf.get_section_for_data('MYSQL','password'),
            'database': conf.get_section_for_data('MYSQL','database'),
            'charset': 'utf8'  # 将charset放入字典中
        }
        try:
            self.conn=self.connection = pymysql.connect(**mysql_conf)  # 保存连接对象
            self.cursor = self.conn.cursor()  # 保存游标对象
            self.cursor=self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接数据库
                host: {host}
                port: {port}
                user: {user}
                database: {database}
            """.format(**mysql_conf))
        except Exception as e:
            logs.error(e)

    def close(self):
        """
        关闭数据库连接
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def query(self,sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            res=self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def insert(self,sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def update(self,sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

    def delete(self,sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            logs.error(e)
        finally:
            self.close()

if __name__=="__main__":
    conn=ConnectMysql()
    sql="select * from user where id=1"
    res=conn.query(sql)
    print(res)



