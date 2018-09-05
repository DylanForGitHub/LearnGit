import requests
import re
import os

#data ={ 'leftid': '1', 'lmid': 'drgg', 'pageNo': '1', 'stockCode': '000504', 'keyword': '',
#        'noticeType': '010301', 'startTime': '2016-12-13', 'endTime': '2017-12-15', 'imageField.x': '26', 'imageField.y': '8', 'tzy': ''}

noticetypeList = ['010305','010303','010307','010301']

#查询深圳数据结果类
class DownloadInfo(object):
    def __init__(self, Result, Link, Name):
        self.Result = Result
        self.Link = Link
        self.Name = Name

def GenerateData(stockid, noticetype, year):
    startdate = '-01-01'
    enddate = '-12-31'
    fromdate = ''
    todate = ''
    if(noticetype == '010301'):
        fromdate = str(int(year) + 1) + startdate
        todate = str(int(year) + 1) + enddate
    else:
        fromdate = str(year) + startdate
        todate = str(year) + enddate
    data = {'leftid': '1', 'lmid': 'drgg', 'pageNo': '1', 'stockCode': stockid, 'keyword': '',  'noticeType': noticetype, 'startTime': fromdate, 'endTime': todate, 'imageField.x': '26', 'imageField.y': '8', 'tzy': ''}
    return data

def SearchData(SearchData):
    DownloadInfoList = []
    url = 'http://disclosure.szse.cn/m/search0425.jsp'
    mainurl = 'http://disclosure.szse.cn/m/'
    html = requests.post(url, data=SearchData)
    patternstring = '<a href[\s\S]*?target[\s\S]*?</a>'
    pattern = re.compile(patternstring)
    downloadlinkArray = pattern.findall(html.text)
    if len(downloadlinkArray) > 0:
        for eachlink in downloadlinkArray:
            ##正则表达式获取下载链接地址
            dlpattern = '\'(.*)\''
            downloadlink = re.compile(dlpattern).findall(eachlink)[0]
            fnpattern = '>(.*)<'
            filenamelink = re.compile(fnpattern).findall(eachlink)[0].split('：')[1]
            NewDownloadInfo = DownloadInfo(True, mainurl + downloadlink, filenamelink + '.PDF')
            DownloadInfoList.append(NewDownloadInfo)
    else:
        NewDownloadInfo = DownloadInfo(False, '' ,'')
        DownloadInfoList.append(NewDownloadInfo)
    return DownloadInfoList


def Createdir(path, stockid, year):
    path = path.strip().rstrip('\\')
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + '\\' + stockid + '\\' + str(year)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def downloadfile(link, filename, path, stockid, year):
    newfilepath =  Createdir(path, stockid, year)
    rr = requests.get(link)
    filepath = newfilepath + '\\' + filename
    if not os.path.exists(filepath):
        with open(filepath, 'wb') as f:
            f.write(rr.content)


stockprelist= ['00','30']
currentyear = 2015
FileDownloadPath = r"F:\StockReport"
for x in stockprelist:
    for y in range(2460, 2461):
        stockid = ''
        if (y < 10):
            stockid = x + '000' + str(y)
        elif(y < 100):
            stockid = x + '00' + str(y)
        elif(y < 1000):
            stockid = x + '0' + str(y)
        else :
            stockid = x + str(y)
        for eachtype in noticetypeList:
            eachdata = GenerateData(stockid, eachtype, currentyear)
            LinkList = SearchData(eachdata)
            if len(LinkList) > 0:
                for eachLink in LinkList :
                    if eachLink.Result:
                        downloadfile(eachLink.Link, eachLink.Name, FileDownloadPath,stockid,currentyear)

