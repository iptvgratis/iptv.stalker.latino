# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de Sawlive por Quequino
# Version 0.2 (7.12.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import json
import math


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



# Función que guía el proceso de elaboración de la URL original
def sawlive(params):
    plugintools.log("[beta.1-0.3.0].ninestreams "+repr(params))
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            url_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            url_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            url_user["pageurl"]=entry          
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            url_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user)) 
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    if referer == "":
        referer = 'http://www.wiz1.net/lag10_home.php'
    url = wizz1(pageurl, referer)
       



# Vamos a hacer una llamada al pageUrl
def gethttp_headers(url, referer):      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


                
def wizz1(pageurl, referer):
 plugintools.log("empieza...")
 data=gethttp_headers(pageurl,referer)
 data=unpack(data);
 r='src="([^"]+)';w=plugintools.find_single_match(urllib.unquote_plus(tamzar(data)),r);
 data=gethttp_headers(w,referer);url=w;
 r='SWFObject\(\'([^\']+).*?file\',\s?\'([^\']+).*?streamer\',\s?\'([^\']+)';w=plugintools.find_multiple_matches(data,r);
 url=w[0][2]+' playpath='+w[0][1]+' swfUrl='+w[0][0]+' token=‪#‎yw‬%tt#w@kku conn=S:OK live=1 pageUrl='+url;print url
 plugintools.play_resolved_url(url)
 

def tamzar(data):
 r='Tamrzar\.push\(\'([^\']+)';w=plugintools.find_multiple_matches(data,r);data=''.join(w);
 return data

def unpack(sJavascript,iteration=1, totaliterations=1  ):
 aSplit = sJavascript.split("rn p}('")
 p1,a1,c1,k1=('','0','0','')
 ss="p1,a1,c1,k1=(\'"+aSplit[1].split(".spli")[0]+')';exec(ss)
 k1=k1.split('|')
 aSplit = aSplit[1].split("))'")
 e = '';d = ''
 sUnpacked1 = str(__unpack(p1, a1, c1, k1, e, d,iteration))
 if iteration>=totaliterations: return sUnpacked1
 else: return unpack(sUnpacked1,iteration+1)
def __unpack(p, a, c, k, e, d, iteration,v=1):
 while (c >= 1):
  c = c -1
  if (k[c]):
   aa=str(__itoaNew(c, a))
   p=re.sub('\\b' + aa +'\\b', k[c], p)
 return p
def __itoa(num, radix):
 result = ""
 if num==0: return '0'
 while num > 0: result = "0123456789abcdefghijklmnopqrstuvwxyz"[num % radix] + result;num /= radix
 return result
def __itoaNew(cc, a):
 aa="" if cc < a else __itoaNew(int(cc / a),a)
 cc = (cc % a)
 bb=chr(cc + 29) if cc> 35 else str(__itoa(cc,36))
 return aa+bb
