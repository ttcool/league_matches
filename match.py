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
            req = urllib2.Request(url,headers=headers)
            content = urllib2.urlopen(req).read()
            c = json.loads(content)
            for i in c:
                match.append(i)
    json.dump(match,open(filename,'w'))

#英超数据
print '英超数据提取'
England_Primere_League = [86,193,150,649,823,967,2573,3270,4030,4794,5428,6118,6832,7471,8658]
England_Primere_League_round = 39
England_Primere_League_filename = 'England_Primere_League.json'
match(England_Primere_League,England_Primere_League_round,England_Primere_League_filename)

#西甲数据
print '西甲数据提取'
Spanish_Primere_League = [566,289,572,669,838,1023,2722,3342,4093,4865,5484,6207,6902,7572,8819]
Spanish_Primere_League_round = 39
Spanish_Primere_League_filename = 'Spanish_Primere_League.json'
match(Spanish_Primere_League,Spanish_Primere_League_round,Spanish_Primere_League_filename)

#意甲数据
print '意甲数据提取'
Italian_Serie_A = [113,419,449,690,870,1058,2771,3364,4162,4891,5542,6243,6964,7588,8828]
Italian_Serie_A_round = 35
Italian_Serie_A_filename = 'Italian_Serie_A.json'
match(Italian_Serie_A,Italian_Serie_A_round,Italian_Serie_A_filename)



#pd1 = pd.DataFrame(c)
#pd2 = pd.DataFrame(c,columns=['hname','hid','gname','gid','hsxname','gsxname','pan','round','stime'])
#pd2.to_excel('foo.xlsx',sheet_name='Sheet1')
#pd1.to_csv('pre.csv')
