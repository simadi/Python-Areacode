
from db.sqlite_helper import SqliteHelper
from utils.log    import Logger

h=SqliteHelper()
log =Logger('[MyDB]').get_logger();

class MyDB():

    def CreateTable(self):
        sql='''CREATE TABLE IF NOT EXISTS "area" (
        "AreaCode" VARCHAR NOT NULL DEFAULT NULL,
        "FatherAreaCode" VARCHAR NOT NULL DEFAULT NULL,
        "UrbanRuralCode" VARCHAR NOT NULL DEFAULT 0,
        "Name" VARCHAR NOT NULL DEFAULT NULL,
        "Url" VARCHAR NOT NULL DEFAULT NULL,
        "Level" tinyint NOT NULL DEFAULT 0,
        "ChildNum" tinyint NOT NULL DEFAULT 0,
        "IsLeaf" tinyint NOT NULL DEFAULT 0,
        "GetCode" tinyint NOT NULL DEFAULT 0,
        "AddTime" DATE DEFAULT (datetime('now', 'localtime')),
        "UpdateAt" DATE,
        PRIMARY KEY ("AreaCode")); '''
        ok=h.exe_sql_bool(sql)
        print('建表{}'.format(ok))

    def AddBatch(self,data_list):
        sql = """INSERT OR IGNORE INTO area(AreaCode,FatherAreaCode,'UrbanRuralCode',name,url,level,IsLeaf) VALUES (?,?,?,?,?,?,?) """
        #value = [(2, 1004, "赵六", 1004), (4, 1005, "吴七", 1005)]
        return h.exe_sql_int(sql,data_list)

    def GetAreaNeedGrabe(self):
        sql="SELECT * FROM area WHERE getCode=0 AND IsLeaf=0";# LIMIT 100 13,130100000000,130102000000,130102001000 and AreaCode='130102001000'
        return h.fetch_table(sql)

    def UpdateArea(self,AreaCode,childNum,getCode):
        sql="UPDATE area SET getCode={},childNum={},UpdateAt=datetime(CURRENT_TIMESTAMP,'localtime') WHERE AreaCode='{}'".format(getCode,childNum,AreaCode)
        return h.exe_sql_int(sql)
    
    def GetAreaStringByKey(self,key):
        AreaCodes=self.GetAreaByKey(key)
        sql="SELECT * FROM area WHERE AreaCode in('{}') Order By AreaCode".format("','".join(AreaCodes))
        allRows= h.fetch_table(sql)
        for r in allRows:
            name=r[3]
            Level=r[5]
            log.info(name.rjust((Level-1)*3+len(name),' '))
            '''
            ├ ─  ┴
            └
            '''
            #IsLeaf=r[7]
            #if IsLeaf==0:

    def GetAreaByKey(self,key):
        sql="SELECT * FROM area WHERE  Name LIKE '%{}%'".format(key)#
        allRows= h.fetch_table(sql)
        AreaCodes=[]
        for r in allRows:
            AreaCode=r[0]
            AreaCodes.append(AreaCode)
            AreaCodes.extend(self.GetAreaByAreaCodeRecurve(AreaCode))
        return AreaCodes

    def GetAreaByAreaCodeRecurve(self,AreaCode):
        '''
        递归查询上级区域
        返回所有区域代码
        '''
        AreaCodes=[]
        while True: 
            sql="SELECT * FROM area WHERE AreaCode='{}'".format(AreaCode)#
            r= h.fetch_table(sql,1)
            if  r==None:
                break
            AreaCode=r[1]
            if AreaCode=='':
                break
            AreaCodes.append(AreaCode)
        return AreaCodes


    def getSub(self,c):
        sql="SELECT shortAreaCode FROM area WHERE  shortFatherAreaCode='{}'".format(c)#
        allRows= h.fetch_table(sql)
        AreaCodes=[]
        for r in allRows:
            AreaCodes.append(int(r[0]))
        return '{}:{}'.format(c,AreaCodes)
    
    def GetAllArea(self):
        d=[]
        sql="SELECT '0','全国' UNION SELECT shortAreaCode,shortName FROM area WHERE  IsLeaf=0  Order By shortAreaCode";# limit 10
        allRows= h.fetch_table(sql)
        for r in allRows:
            c=r[0]
            sql1="SELECT shortAreaCode FROM area WHERE  shortFatherAreaCode='{}'".format(c)
            allRows1= h.fetch_table(sql1)
            AreaCodes=[]
            for r1 in allRows1:
                AreaCodes.append(int(r1[0]))
            d.append('{}:{}'.format(c,AreaCodes))
        return 'var dicID={{{}}};'.format(",".join(d))

    def GetAllArea2(self):
        sql="SELECT shortAreaCode,shortName FROM area  Order By shortAreaCode";# limit 10
        d=[]
        allRows= h.fetch_table(sql)
        for r1 in allRows:
            d.append("{}:'{}'".format(r1[0],r1[1]))
        return 'var dicName={{{}}};'.format(",".join(d))

    def GetProvince(self):
        sql="SELECT shortAreaCode,Name FROM area  WHERE level=1";# limit 10
        d={}
        allRows= h.fetch_table(sql)
        for r in allRows:
            d[r[1]]=r[0]
        return d

    def AddBatchAreaPostageLevel(self,data_list):
        sql = """INSERT OR IGNORE INTO AreaPostageLevel(FromAreaCode,ToAreaCode,PostageLevel) VALUES (?,?,?) """
        return h.exe_sql_int(sql,data_list)
    
    def GetProvince2(self):
        sql="SELECT AreaCode,shortName FROM area  WHERE level=1";# limit 10
        d=[]
        allRows= h.fetch_table(sql)
        for r in allRows:
            d.append("{}:'{}'".format(r[0],r[1]))
        return d
    def GetAreaPostageLevel(self):
        sql="SELECT FromAreaCode||ToAreaCode,PostageLevel FROM AreaPostageLevel";
        d=[]
        allRows= h.fetch_table(sql)
        for r in allRows:
            d.append("{}:{}".format(r[0],r[1]))
        return d

    def GetPostageLevel(self):
        sql="SELECT Level,postage1,postagen FROM PostageLevel";
        d=[]
        allRows= h.fetch_table(sql)
        for r in allRows:
            d.append("{}:{}".format(r[1],r[2]))
        return d