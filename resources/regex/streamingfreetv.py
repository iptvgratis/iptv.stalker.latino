# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de streamingfreetv
# Version 0.1 (17.10.2014)
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


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



def streamingfreetv0(params):
    plugintools.log("[beta.1-0.3.0].streamingfreetv "+repr(params))

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
    body = gethttp_headers(pageurl)
    plugintools.log("body= "+body)
    
    #<script type='text/javascript'> width=650, height=400, channel='sysf', e='1';</script><script type='text/javascript' src='http://privado.streamingfreetv.net/embedPlayer.js'></script>
    pattern = plugintools.find_single_match(body, 'width=(.*?)</script>')
    width= plugintools.find_single_match(pattern, '\'(.*?)\' ')
    print width
    height= plugintools.find_single_match(pattern, 'height=\'(.*?)\' ')
    print height
    playpath = url_user.get("playpath")
    src=plugintools.find_single_match(pattern, 'src=(.*?) ')
    
    #http://privado.streamingfreetv.net/embed/embed.php?channel=sysf&w=650&h=400
    pageurl = 'http://privado.streamingfreetv.net/embed/embed.php?channel='+playpath+'&w='+width+'&h='+height
    plugintools.log("pageurl= "+pageurl)
    url_user["pageurl"]=pageurl

    #<param name='flashvars' value='file=sysf&streamer=rtmp://94.23.247.151/redirect?token=0ngYvHGwJks-BswfZHOwTwExpired=1417266581&autostart=false&skin=http://privado.streamingfreetv.net/jw/classic.zip'>

    rtmp=plugintools.find_single_match(body, 'streamer=(.*?)&autostart')
    swfurl=plugintools.find_single_match(body, '<param name=\'movie\' value=\'(.*?)\'')
    print 'swfurl',swfurl
    print 'rtmp',rtmp
    url = rtmp+' playpath='+playpath+' swfUrl='+swfurl+' pageUrl='+pageurl
    #plugintools.log("url= "+url)
    plugintools.play_resolved_url(url)
    
    
 
# Vamos a hacer una llamada a la página que nos dará el token
def gethttp_headers(pageurl):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", pageurl])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    #plugintools.log("body= "+body)
    return body

	
def gethttp_referer_headers(url_user):

    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    print 'referer',referer
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    #plugintools.log("body= "+body)    
    return body
    
