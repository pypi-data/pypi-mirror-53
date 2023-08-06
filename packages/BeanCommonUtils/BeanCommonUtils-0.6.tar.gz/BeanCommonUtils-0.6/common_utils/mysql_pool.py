import pymysql
from DBUtils.PooledDB import PooledDB


class MysqlPool(object):

    __pool = None

    def __init__(self, mysql_info):
        # 构造函数，创建数据库连接、游标
        self.mysql_conn = MysqlPool.get_mysql_conn(mysql_info)
        self.cur = self.mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @classmethod
    def get_mysql_conn(cls, mysql_info):
        if cls.__pool is None:
            cls.__pool = PooledDB(creator=pymysql, mincached=5, maxcached=20,
                                  host=mysql_info['host'], user=mysql_info['user'], passwd=mysql_info['passwd'],
                                  db=mysql_info['db'], port=mysql_info['port'],
                                  charset=mysql_info.get('charset', 'utf8'))

        return cls.__pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql, sql_type):
        try:
            insert_num = self.cur.execute(sql)
            self.mysql_conn.commit()
        except Exception as e:
            raise Exception("%s sql execute error, err_msg: %s" % (sql_type, e))

        return insert_num, True

    # 查询
    def op_select(self, sql):
        self.cur.execute(sql)
        try:
            select_res = self.cur.fetchall()
        except Exception as e:
            return e, False

        return select_res, True

    def sql_operate(self, sql, sql_type):
        sql_operate_list = ["insert", "update", "delete", "select"]
        if not isinstance(sql_type, str) and sql_type not in sql_operate_list:
            raise ValueError("input sql_type error, sql_type may be: %s" % sql_operate_list)

        if sql_type == "select":
            return self.op_select(sql)
        else:
            return self.op_insert(sql, sql_type)

    # 释放资源
    def dispose(self):
        self.mysql_conn.close()
        self.cur.close()
