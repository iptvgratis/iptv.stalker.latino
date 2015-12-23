# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de ezcast
# rev. 15.05.2015
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
def ezcast0(params):
    plugintools.log("[%s %s] Regex de ezcast: %s " % (addonName, addonVersion, repr(params)))
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

    print url_user
    url = url_user["pageurl"]
    ref = url
    body = gethttp_referer_headers(url,ref);plugintools.log("body= "+body)

# Comprobar qué es la variable "res" en la función ezcast(url,ref,res):
    p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(body,p);plugintools.log("flashvars= "+flashvars)
    p = re.compile(ur'\&?=([^\&]+)');flvs=re.findall(p,flashvars);id=flvs[0];c=flvs[1];token=flvs[4];print 'flvs',flvs
    width = plugintools.find_single_match(body, 'var width = (.*?);')
    height = plugintools.find_single_match(body, 'var height = (.*?);')
    p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ezcast.tv'+plugintools.find_single_match(body,p);print swf
    lb='http://ezcast.tv:1935/loadbalancer';lb=plugintools.read(lb);print lb;lb=plugintools.find_single_match(lb,'redirect=(.*)');plugintools.log("lb= "+lb)
    media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+'&pk='+token+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl=http://www.ezcast.tv/embedded/'+c+'/1/'+width+'/'+height+' timeout=15'
    url = media_url.strip()
    plugintools.play_resolved_url(url)

    # rtmp://46.28.50.124/live playpath=marronlc1?id=21225&pk=3e363f86ad78041bdbda8a8785f4a80f638ccc80eda8b269bd75f80bc08f25f2 swfUrl=http://www.embedezcast.com/static/scripts/fplayer.swf pageUrl=http://www.embedezcast.com/embedplayer/marronlc1/1/500/400
			
	
def gethttp_referer_headers(url,ref):

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body
