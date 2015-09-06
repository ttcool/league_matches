import urllib2
from bs4 import BeautifulSoup
import json
import  pandas   as pd
from pandas import DataFrame 

match = []
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
for id in [86,193,150,649,823,967,2573,3270,4030,4794,5428,6118,6832,7471,8658]:
    for i in range(1,39):
        url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid='+str(id)+'&round='+str(i)
        print url
        req = urllib2.Request(url,headers=headers)
        content = urllib2.urlopen(req).read()
        c = json.loads(content)
        for i in c:
            match.append(i)
for i in match:
    print i
json.dump(match,open('match.json','w'))

#pd1 = pd.DataFrame(c)
#pd2 = pd.DataFrame(c,columns=['hname','hid','gname','gid','hsxname','gsxname','pan','round','stime'])
#pd2.to_excel('foo.xlsx',sheet_name='Sheet1')
#pd1.to_csv('pre.csv')
