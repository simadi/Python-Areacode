import utils.log    as logger
import sqlite3
 
##sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
##sys.path.append("..")
 
 
class SqliteHelper:
 
    def __init__(self, dbName="sqlite3.db"):
        """
        初始化连接--使用完记得关闭连接
        :param dbName: 连接库名字，注意，以'.db'结尾
        """
        self._conn = sqlite3.connect(dbName)
        self._cur = self._conn.cursor()
        self._time_now = "[" + sqlite3.datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]"
        self.log = logger.Logger('[SqliteHelper]').get_logger()
 
    def close_con(self):
        """
        关闭连接对象--主动调用
        :return:
        """
        self._cur.close()
        self._conn.close() 
 
    def exe_sql_bool(self, sql):
        """
        创建表,删除表
        :param sql:
        :return: True or False
        """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            self.log.info("执行出错:{}".format(sql), e)
            return False
  
    def exe_sql_int(self, sql, values=None):
        """
        增(多条),删,改
        :param sql:
        :param value: list:[(),()]
        :return:
        """
        try:
            if values==None:
                self._cur.execute(sql)
            else:
                self._cur.executemany(sql, values)
            self._conn.commit()
            return self._cur.rowcount
        except Exception as e:
            self.log.info("增删改出错:{}".format(sql), e)
            return -1

    def fetch_table(self, sql, limit=0):
        """
        查询所有数据
        :param sql:
        :param limit_flag: 查询条数选择，False 查询一条，True 全部查询
        :return:
        """
        try:
            self._cur.execute(sql)
            if limit!=1:
                r = self._cur.fetchall()
            else:
                r = self._cur.fetchone()
            return r
        except Exception as e:
            self.log.info("[SELECT TABLE ERROR{}]".format(sql), e)
  
class conTest:
    """测试类"""
 
    def __init__(self,file):
        self.con =sqlite3.connect(file)
        self.cur=self.con.cursor()
 
    def create_table_test(self,bm):
        sql = '''CREATE TABLE `mytest` (
                  `id` DATETIME DEFAULT NULL,
                  `user` VARCHAR(12) DEFAULT NULL,
                  `name` VARCHAR(12) DEFAULT NULL,
                  `number` VARCHAR(12) DEFAULT NULL
                )'''
        sql1 = f'PRAGMA table_info ({bm})'
        self.log.info(sql1)
        self.cur.execute(sql1)
        self.con.commit()
        value2 = self.cur.fetchall()
        if len(value2)==0:
            try:
                self.log.info(self.cur.execute(sql))
                self.con.commit()
            except:
                self.log.info("建立表出错")
        else:
            self.log.info("表已经存在")
 
    def drop_table_test(self):
        sql1="delete from mytest"
        self.cur.execute((sql1))
        self.con.commit()
        #print(self.con.drop_table("mytest"))
 
    def fetchall_table_test(self):
        sql = "SELECT * from mytest WHERE user='1003';"
        sql_all = "SELECT * from mytest;"
        print("全部记录", self.cur.execute(sql_all))
        print("全部记录", self.cur.fetchall())
        print("单条记录", self.cur.execute(sql))
        print("条件查询", self.cur.execute(sql))
 
    def delete_table_test(self):
        sql = "DELETE FROM mytest WHERE user='1003';"
        self.con.delete_table(sql)
        
 
    def update_table_test(self):
        sql_update = "UPDATE mytest SET id={0},user={1},name={2},number={3} WHERE number={4}".format(1, 1002, "'王五'",1002,1002)
        self.cur.execute(sql_update)
        self.con.commit()                                                                                            
                                                                                                   
        #print(self.con.insert_update_table(sql_update))
 
    def insert_table_test_one(self):
        sql = """INSERT INTO mytest VALUES (3, 1003, "王五", 1003);"""
        self.cur.execute((sql))
        self.con.commit()
                         
 
    def insert_table_test_many(self):
        sql = """INSERT INTO mytest VALUES (?,?,?,?) """
        value = [(2, 1004, "赵六", 1004), (4, 1005, "吴七", 1005)]
        for i in value:
            self.cur.execute(sql,i)
            self.con.commit()
##        self.con.insert_table_many(sql, value)
##        self.cur
 
    def close_con(self):
        self.con.close()
 
 
if __name__ == '__main__':
    file1="sqlite3.db"
    bm="mytest"
    contest = conTest(file1)
    contest.create_table_test(bm)
    contest.insert_table_test_many()
    contest.fetchall_table_test()
    contest.insert_table_test_one()
    contest.fetchall_table_test()
    contest.update_table_test()
    contest.drop_table_test()
    contest.close_con()