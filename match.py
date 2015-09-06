# -*- coding: utf8 -*-
import urllib2
from bs4 import BeautifulSoup
import json
import  pandas   as pd
from pandas import DataFrame 

#stid 赛季id   round 联赛轮次  filename 保存文件名
def match(stid,round,filename):
    match = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    for id in stid:
        for i in range(1,round):
            url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid='+str(id)+'&round='+str(i)
            print url
            req = urllib2.Request(url,headers=headers)
            content = urllib2.urlopen(req).read()
            c = json.loads(content)
            for i in c:
                match.append(i)
    json.dump(match,open(filename,'w'))

#英超数据
England_Primere_League =  [86,193,150,649,823,967,2573,3270,4030,4794,5428,6118,6832,7471,8658]
England_Primere_League_round = 39
England_Primere_League_filename = 'England_Primere_League'
match(England_Primere_League,England_Primere_League_round,England_Primere_League_filename)

#西甲数据


#pd1 = pd.DataFrame(c)
#pd2 = pd.DataFrame(c,columns=['hname','hid','gname','gid','hsxname','gsxname','pan','round','stime'])
#pd2.to_excel('foo.xlsx',sheet_name='Sheet1')
#pd1.to_csv('pre.csv')
