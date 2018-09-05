#uu = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback24946&productId=600000&reportType2=DQGG&reportType=YEARLY&beginDate=2017-01-01&endDate=2017-12-31&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1514460531026'
#hh = {'Referer':'http://www.sse.com.cn/disclosure/listedinfo/regular/','Host':'query.sse.com.cn'}

#class QueryType(Enum):
#    QUATER1 = 1
#    QUATER2 = 2
#    QUATER3 = 3
#    YEARLY = 4

import requests, re, json ,os

def GenerateUrl(code, year, quater):
    starttime = ''
    endtime = ''
    if(quater == 'YEARLY') :
        starttime = str(int(year) + 1) + '-01-01'
        endtime = str(int(year) + 1) + '-12-31'
    else:
        starttime = str(year) + '-01-01'
        endtime = str(year) + '-12-31'
    callbackurl = 'jsonpCallback12345'
    preUrl = 'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=' + callbackurl + '&productId=' + code +  '&reportType2=DQGG&reportType=' + quater + '&beginDate=' + starttime + '&endDate=' + endtime + '&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1514460531026'
    return  preUrl

def CreatePath(path):
    if not os.path.exists(path) :
        os.makedirs(path)

def GetFilesAndDownload(url, path):
    headersfordownload = {'Host': 'query.sse.com.cn','Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'}
    preurl = 'http://www.sse.com.cn/'
    rr = requests.get(url,headers = headersfordownload)
    if len(rr.text) > 0:
        matchstring = '{"[\s\S]*?"}'
        rc =  re.compile(matchstring)
        jsonreturn = rc.findall(rr.text)[0]
        returndata = json.loads(jsonreturn)
        ResultNode = returndata['result']
        if ResultNode != []:
            length = len(ResultNode)
            for index in range(0,length):
                CreatePath(path)
                title = ResultNode[index]['title'] + '.PDF'
                filepath = path.strip().rstrip('\\') + '\\' + title
                url = ResultNode[index]['URL']
                downloadurl = preurl + url.strip().lstrip('/')
                drr = requests.get(downloadurl)
                if not os.path.exists(filepath):
                    with open(filepath, 'wb') as f:
                        f.write(drr.content)

def GetFiles(code, year ,strorepath):
    QueryType = ['QUATER1','QUATER2','QUATER3','YEARLY']
    downloadpath = strorepath.strip().rstrip('\\') + '\\' + code + '\\' + str(year)
    for eachtype in QueryType:
        eachurl = GenerateUrl(code,year,eachtype)
        GetFilesAndDownload(eachurl,downloadpath)

stockcodepre = '60'
currentyear = 2015
FileDownloadPath = r"F:\StockReport"
for y in range(516, 517):
    stockid = ''
    if (y < 10):
        stockid = stockcodepre + '000' + str(y)
    elif (y < 100):
        stockid = stockcodepre + '00' + str(y)
    elif (y < 1000):
        stockid = stockcodepre + '0' + str(y)
    else:
        stockid = stockcodepre + str(y)
    GetFiles(stockid,currentyear,FileDownloadPath)






