
# -*- ecoding: utf-8 -*-
# @ModuleName: StudentSystem
# @Author: Sail
# @Time: 2021/10/11 22:08
# Python骚操作之海量性感妹子图爬虫实战精讲
# 爬虫技术 : 获取数据的程序
# 确定网站 相互了解  筛选功能 保存数据
# BS4 xpath json  re pyquery
from calendar import isleap
from lxml import etree
from urllib import request,parse
import re,time
from db.mydb import MyDB
from utils.graber import Graber
from utils.log    import Logger

def GetMeizi():
    #1.到网站里面确定一个网址
    url = 'https://www.huya.com/g/4079'
    #2.用Python跟这个网址先做一个了解
    result = requests.get(url=url).text
    #3.在网站源码内筛选我们需要的数据  json xpath re bs4 pyquery
    data = etree.HTML(result)
    demo = data.xpath('//img[@class="pic"]')
    #4.保存数据
    for  i  in demo:
        newUrl = i.xpath('./@data-original')[0]
        newName = i.xpath('./@alt')[0]
        request.urlretrieve(newUrl, r'G:\妹子\\' + newName + '.jpg')
        print("<%s>下载完毕!" % newName)

log =Logger('[Main]').get_logger();
grab=Graber()

if __name__ == "__main__":
    mydb=MyDB()
    fileName='areaData.js'
    #a=mydb.GetAllArea()
    b=mydb.GetAllArea2()
    with open(fileName,'w',encoding='utf-8')as file:
        #file.write(a+"\r")
        file.write(b+"\r")
    #print(a)
    os.system("pause")
    '''
    a=mydb.GetAreaStringByKey('一连')
    #log.info(a)
    os.system("pause")
    MyDB.CreateTable()
    urlIndex='http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html'
    provinces=grab.grabeArea1(urlIndex)
    num=MyDB.AddBatch(provinces);
    log.info('批量插入{}个省市'.format(num))
    '''
    i=0
    while True:
        i=i+1
        rows=mydb.GetAreaNeedGrabe()
        log.info('第{}次采集{}个========================'.format(i,len(rows)))
        if len(rows)==0:
            log.info('全部采完了========================')
            break
        for r in rows:
            AreaCode=r[0]
            #FatherAreaCode=r[1]
            #UrbanRuralCode=r[2]
            name=r[3]
            url=r[4]
            level=r[5]
            #IsLeaf=r[5]
            #getCode=r[6]
            #AddTime=r[7]
            #UpdateAt=r[8]
            getCode=0
            log.info('获取[{}]的下级地区---------------------------------'.format(name))
            areas=grab.grabeArea(AreaCode,url,level)
            childNum=len(areas)
            log.info('采集到{}个 {}'.format(childNum,[x[3] for x in areas]))
            if len(areas)==0:
                log.info('采集有问题 {}'.format(url))
                getCode=-1
            else:
                num=mydb.AddBatch(areas);
                log.info('批量插入{}'.format(num))
                getCode= -2 if num<0 else 1
            n=mydb.UpdateArea(AreaCode,childNum,getCode)
            log.info('更新采集状态为{}'.format(n))
            time.sleep(1) # 暂停 1 秒



