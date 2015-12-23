# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de vercosasgratis.com
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


# Función que guía el proceso de elaboración de la URL original
def vercosas(params):
    plugintools.log('[%s %s] Initializing vercosasgratis regex... %s' % (addonName, addonVersion, repr(params)))
    url_user = {}
    url_user["token"]='#ed%h0#w@12Fuck'
    
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
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user)) 
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    
    body = gethttp_headers(pageurl, referer)

    match = plugintools.find_single_match(body, 'Player By http://vercosasgratis.com(.*?)</script>')
    print match
    swf = 'http://vercosasgratis.com/player.swftoken=#ed%h0#w@12Fuck'
    playpath = plugintools.find_single_match(match, "file', '(.*?)'")
    app = plugintools.find_single_match(match, 'id=\'(.*?)\'')
    url_user["swf"] = swf.lower()    
    rtmp = plugintools.find_single_match(match, "'streamer','(.*?)'")
    #url_user["rtmp"] = rtmp.replace("&autostart=", "")
    plugintools.log("swf= "+swf)    
    plugintools.log("rtmp= "+rtmp)
    plugintools.log("playpath= "+playpath)

    url_final = rtmp + ' playpath='+playpath + ' swfUrl='+swf + ' pageUrl='+pageurl + ' live=1 timeout=10'
    plugintools.play_resolved_url(url_final)

    


# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

