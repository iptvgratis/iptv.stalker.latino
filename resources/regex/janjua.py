# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de castalba
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


'''
<item>
<title>DMAX Italia</title>
<link>rtmp://$doregex[ip]/live playpath=dsdfsdff?id=39204$doregex[pk] conn=S:OK swfUrl=http://www.janjuaplayer.com/resources/scripts/eplayer.swf pageUrl=http://www.janjuaplayer.com/embedplayer/dsdfsdff/1/500/380 swfVfy=true buffer=5000 live=true</link>
<regex>
<name>ip</name>
<expres>redirect=(.*)<expres>
<page>http://www.janjua.tv:1935/loadbalancer</page>
</regex>
<regex>
<name>pk</name>
<expres>ea=(.*)'</expres>
<page>http://www.janjuaplayer.com/embedplayer/dsdfsdff/1/500/380</page>
<referer>http://www.janjuaplayer.com/</referer>
</regex>
</item>
'''


# En construcción!
def janjua0(params):
    plugintools.log("[%s %s] Castalba regex: %s " % (addonName, addonVersion, repr(params)))

    url = params.get("url")
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
    body = gethttp_referer_headers(pageurl,referer)
    plugintools.log("body= "+body)

    playpath = plugintools.find_single_match(body, "var v_part = '([^']+)")
    playpath = playpath.replace("/privatestream/", "")
    plugintools.log("playpath= "+playpath)
    url_redirect = 'http://www.janjua.tv:1935/loadbalancer'
    bodi = gethttp_referer_headers(url_redirect,referer)
    plugintools.log("bodi= "+bodi)
    ip = plugintools.find_single_match(bodi, 'redirect=([^ ]+)')
    plugintools.log("ip= "+ip)          
            
    # Construimos la URL original            
    url = url_user.get("rtmp")+' playpath='+playpath+' swfUrl='+url_user.get("swfurl")+' pageUrl='+pageurl+' swfVfy=true buffer=5000 live=true'
    plugintools.log("url= "+url)
    plugintools.play_resolved_url(url)
        
 

def gethttp_referer_headers(url,ref):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body
    
