#!/usr/bin/python
#coding=utf-8
import threading,traceback,time,importlib,imp,os,logging
from core.utils import printInfo
from downloader import execDownload
from extracter import Extracter
from setting import SPIDERS,CONCURRENCY,CONCURRENCYPER1S

class SimplifiedMain():
  def __init__(self):
    for spider in SPIDERS:
      try:
        self.getSpider(spider['file'],spider["class"])
      except Exception as err:
        self.log(err,logging.ERROR)
    
    self._extracter = Extracter()

  def log(self, msg, level=logging.DEBUG):
    if (isinstance(msg,UnicodeEncodeError)):
      print msg
      return
    printInfo(msg)
    if(level==logging.ERROR):
      logger = logging.getLogger()
      logging.LoggerAdapter(logger, None).log(level, msg)

  _runflag = False
  def setRunFlag(self, flag):
    self._runflag = flag

  _spiderDic = {}
  def startThread(self):
    threadExtract = threading.Thread(target=self.extractThread)
    threadExtract.start()
    while self._runflag:
      try:
        if(os.path.exists('stop.txt')):
          self._runflag = False
          os.rename('stop.txt','stoped.txt')
          break
        for ssp in self._spiderDic.values():
          urlCount = ssp.urlCount()
          if(self.checkConcurrency(ssp.name,urlCount)):
            url = ssp.popUrl()
            if(url):
              thread = threading.Thread(target=self.downloadThread, args=(url,ssp))
              thread.start()
            else:
              self._concurrency-=1
          if(urlCount==0):
            plan = ssp.plan()
            ssp.resetUrls(plan)
            time.sleep(3)
      except Exception as err:
        self.log(err,logging.ERROR)
        time.sleep(10)
      time.sleep(0.3)
    self._runflag=False
    self.log('download app stoped......')

  _concurrency=0
  _downloadPageNum=0
  _startCountTs=time.time()
  def checkConcurrency(self,name,count):
    tmSpan = time.time()-self._startCountTs
    if(tmSpan>10):
      if(self._downloadPageNum>(CONCURRENCYPER1S*tmSpan)):
        self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}, reason={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan,'exceed the config number CONCURRENCYPER1S'))
        return False
      self._startCountTs=time.time()
      self._downloadPageNum=0
    if self._concurrency >= CONCURRENCY:
      self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}, reason={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan,'exceed the config number CONCURRENCY'))
      return False
    self._concurrency+=1
    self.log('name={}, count={}, concurrency={}, downloadPageNum={}, tmSpan={}'.format(name,count,self._concurrency,self._downloadPageNum,tmSpan))
    return True

  def getSpider(self, fileName, className):
    if(fileName in self._spiderDic):
      return self._spiderDic[fileName]
    m = importlib.import_module(fileName,'spiders')
    cls = getattr(m, className)
    ssp = cls()
    if(not ssp.login()):
      print className +': login failed'
    else:
      self._spiderDic[fileName]=ssp
    return ssp

  def extractThread(self):
    while(self._runflag):
      flag=False
      for ssp in self._spiderDic.values():
        try:
          data = ssp.popHtml()
          if(data):
            flag = True
            obj = self._extracter.extract(data["url"],data["html"],ssp)
            ssp.updateHtmlState(data["id"],1)
            if obj: ssp.saveData(obj)
            time.sleep(0.5)
        except Exception as err:
          self.log(err,logging.ERROR)
          time.sleep(10)
      if(not flag):
        time.sleep(3)
      time.sleep(1)
  def downloadThread(self,url,ssp):
    try:
      if(not url):
        return
      if(isinstance(url,str)):
        url={'url':url}
      print url['url']
      self._downloadPageNum=self._downloadPageNum+1
      html = execDownload(url,ssp)
      ssp.saveHtml(url,html)
      if(not html):
        # self._extracter.extract(url,html,ssp)
        # else:
        ssp.downloadError(url)
    except Exception as err:
      self.log(err,logging.ERROR)
    finally:
      self._concurrency-=1
