# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de rdmcast
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



def rdmcast0(params):
    plugintools.log("[beta.1-0.3.0].rdmcast "+repr(params))

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
    body = gethttp_referer_headers(url_user)
    print body

    token = plugintools.find_single_match(body, "token', '(.*?)'")
    playpath = plugintools.find_single_match(body, "file', '(.*?)'")
    plugintools.log("token= "+token)
    plugintools.log("playpath= "+playpath)

    streamer = plugintools.find_single_match(body, "streamer', '(.*?)'")

    url = streamer+' playpath='+playpath+' swfUrl='+url_user.get("swfurl")+' token='+token+' pageUrl=http://rdmcast.com/player.swf live=true timeout=15'

    plugintools.log("url= "+url)
    plugintools.play_resolved_url(url)    
    
 
# Vamos a hacer una llamada a la página que nos dará el token
def gethttp_referer_headers(url_user):

    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    print 'referer',referer
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)             
    return body
    
