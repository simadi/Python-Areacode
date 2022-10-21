import utils.log    as logger
import utils.tools as tools
from bs4 import BeautifulSoup
import re

class Graber():

    def __init__(self):
        self.log = logger.Logger('[Graber]').get_logger()
        self.levelDic = {1: 'province',2: 'city',3: 'county',4: 'town',5: 'village'}
        self.specialCode=['441900000000','442000000000','460400000000']#东莞,中山,儋州市 :不设区的市

    def grabeArea1(self,url0):
        html =tools.getHtml(url0)
        soup = BeautifulSoup(html, 'lxml')    
        listA=soup.find_all('a')[0:-1]  # 所有 a 元素
        areas=[]
        for a in listA:
            AreaCode=a.attrs['href'].replace('.html','')
            url=url0.replace('index',AreaCode)
            UrbanRuralCode=''
            name=a.contents[0]
            IsLeaf=0
            area=(AreaCode,'0',UrbanRuralCode,name,url,1,IsLeaf)
            areas.append(area)
        self.log.info('获取到1级地区{}个'.format(len(areas)))
        return areas

    '''
    http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html 
    http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/13.html 省
    http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/13/1301.html 市
    http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/13/01/130102.html 县
    http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/13/01/02/130102001.html 镇
    '''
    
    def grabeArea(self,fatherCode,fatherUrl,fatherLevel):
        html =tools.getHtml(fatherUrl)#http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/13.html
        html = re.sub(r">\s+?<", "><", html)#去掉空行
        soup = BeautifulSoup(html, 'lxml')
        if fatherCode in self.specialCode:
            fatherLevel=fatherLevel+1
        level=fatherLevel+1
        listTr=soup.find_all('tr', class_=self.levelDic[level]+'tr')#countytr,towntr,villagetr,省市县镇村
        areas=[]
        for tr in listTr:
            #<tr class="citytr"><td><a href="13/1301.html">130100000000</a></td><td><a href="13/1301.html">石家庄市</a></td></tr>
            #<tr class="countytr"><td>130101000000</td><td>市辖区</td></tr>
            #<tr class="countytr"><td><a href="01/130104.html">130104000000</a></td><td><a href="01/130104.html">桥西区</a></td></tr>
            #<tr class="towntr"><td><a href="02/130102005.html">130102005000</a></td><td><a href="02/130102005.html">跃进街道</a></td></tr>
            if level<5:#市县镇
                if len(tr.next())==0:#无连接
                    IsLeaf=1
                    AreaCode=tr.next.next
                    url=''
                else:
                    IsLeaf=0
                    a=tr.next()[0]
                    AreaCode=a.contents[0]
                    url0=self.getUrlFatherPath(fatherCode,fatherLevel,fatherUrl)
                    url=url0+a.attrs['href']
                UrbanRuralCode=''            
                name=tr.text.replace(AreaCode,'')
            else:#村
            #<tr class="villagetr"><td>130102001003</td><td>111</td><td>八家庄社区居民委员会</td></tr>
                AreaCode=tr.contents[0].text
                UrbanRuralCode=tr.contents[1].text
                name=tr.contents[2].text
                url=''
                IsLeaf=1
            area=(AreaCode,fatherCode,UrbanRuralCode,name,url,level,IsLeaf)
            areas.append(area)
        return areas

    def getUrlFatherPath(self,AreaCode,level,url):
        if AreaCode in self.specialCode:
            str1=AreaCode[0:(level-1)*2]
        else:
            str1=AreaCode[0:level*2]
        return url.replace(str1+'.html','')
