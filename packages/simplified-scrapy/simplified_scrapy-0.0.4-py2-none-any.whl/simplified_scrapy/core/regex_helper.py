#!/usr/bin/python
#coding=utf-8
import re
from xml_helper import XmlDictConfig,convert2Dic
def _getSection(html,start=None,end=None):
  s = 0
  e = len(html)
  if(start): s=html.find(start)
  if(end): e=html.find(end)
  return (s,e)
def listA(html,url=None,start=None,end=None):
  if(not html): return []
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return []
  patternLst = re.compile(u'<a[\s]+[^>]*>[\s\S]*?</a>')
  patternUrl = re.compile(u'href[\s=]+[\'"](?P<url>.*?)[\'"]') 
  patternTitle1 = re.compile(u'title[\s=]+[\'"](?P<title>.*?)[\'"]')
  patternTitle2 = re.compile(u'<a[^>]*>(?P<title>.*?)</a>')

  strA = patternLst.findall(html,s,e)
  lst=[]
  for i in strA:
    url = None
    title = None
    tmp = patternUrl.search(i)
    if tmp: url = tmp.group("url")
      
    tmp = patternTitle1.search(i)
    if tmp: title = tmp.group("title")
    if(not title):
      tmp = patternTitle2.search(i)
      if tmp: title = tmp.group("title")

    lst.append({'url':url,'title':title})

  return lst
def listImg(html,url=None,start=None,end=None):
  if(not html): return []
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]

  if(s < 0 or e < s): return None
  patternLst = re.compile(u'<img[\s]+[^>]*>')
  patternUrl = re.compile(u'src[\s=]+[\'"](?P<url>.*?)[\'"]') 
  patternTitle = re.compile(u'alt[\s=]+[\'"](?P<title>.*?)[\'"]')
  lstStr = patternLst.findall(html,s,e)
  lst=[]
  for i in lstStr:
    url = None
    title = None
    tmp = patternUrl.search(i)
    if tmp: 
      url = tmp.group("url")
      
    tmp = patternTitle.search(i)
    if tmp:
      title = tmp.group("title")

    lst.append({'url':url,'alt':title})
  return lst

def getElementsByTag(tag,html,start=None,end=None):
  if(not tag or not html): return None
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]

  if(s < 0 or e < s): return None
  patternLst = re.compile(u'<'+tag+'[\s]+[^>]*>[\s\S]*?</'+tag+'>')
  lstStr = patternLst.findall(html,s,e)
  lst=[]
  for line in lstStr:
    dic=convert2Dic(line)
    if(dic):
      lst.append(dic)
  return lst

def getElementByID(id,html,start=None,end=None):
  if(not id or not html): return None
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  index = html.find(id,s,e)
  if(index<0): return None

  pattern = re.compile(u'<[\s\S]+ id[=\'"\s]+'+id+'[\'"][\s\S]*?</[\w]+>') 
  tmp = pattern.search(html,s,e)
  dom = None
  if tmp: dom = tmp.group()
  return convert2Dic(dom)

def getElementsByClass(className,html,start=None,end=None):
  if(not className or not html): return None
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  pattern = re.compile(u'<[\s\S]+?[\s]class[=\'"\s]+[\s\S]*?'+className+'[\'" ]+[\s\S]*?</[\w]+?>') 
  lstStr = pattern.findall(html,s,e)
  lst=[]
  for line in lstStr:
    dic=convert2Dic(line)
    if(dic):
      lst.append(dic)
  return lst

def getElementTextByID(id,html,start=None,end=None):
  if(not id or not html): return None
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  index = html.find(id,s,e)
  if(index<0): return None

  pattern = re.compile(u'<[\s\S]+ id[=\'"\s]+'+id+'[\'"][\s\S]*?>(?P<txt>[\s\S]*?)</[\w]+>') 
  tmp = pattern.search(html,s,e)
  dom = None
  if tmp: dom = tmp.group("txt")
  return dom

def getElementAttrByID(id,attr,html,start=None,end=None):
  if(not id or not html or not attr): return None
  section = _getSection(html,start,end)
  s = section[0]
  e = section[1]
  if(s < 0 or e < s): return None

  dom = getElementByID(id,html,start,end)
  if(dom):
    pattern = re.compile(attr+u'[\s=]+[\'"](?P<attr>.*?)[\'"]')
    tmp = pattern.search(dom)
    if tmp: 
      return tmp.group("attr")
  return None

# print getElementsByClass('asd','''<div id="write-notes-ad" class='asd'>123</div>
#       <div id="youdao-fixed-ad" class='asd woer'></div>''')
# print getElementByID('write-notes-ad','''<div id="write-notes-ad" class='asd'>123</div>
#       <div id="youdao-fixed-ad" class='asd woer'></div>''')

# print getElementsByTag('div','''<div id="write-notes-ad" class='asd'>123</div>
#       <div id="youdao-fixed-ad" class='asd woer'></div>''')