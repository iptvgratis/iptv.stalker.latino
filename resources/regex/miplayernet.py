# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de miplayer.net
# Version 0.1 (02.11.2014)
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

import re,urllib,urllib2,sys
import plugintools,ioncube


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



# Función que guía el proceso de elaboración de la URL original
def miplayernet0(params):
    plugintools.log("[%s %s].miplayer.net %s " % (addonName, addonVersion, repr(params)))
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("pageUrl"):
            pageurl = entry.replace("pageUrl=", "")
            pageurl = pageurl.replace("&amp;", "&")
            url_user["pageurl"]=pageurl          
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            url_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user)) 
    url = url_user.get("pageurl")
    ref = url_user.get("referer")
    if ref == "":
        ref = 'http://miplayer.net'
        
    body = gethttp_referer_headers(url, ref)

    tok_page = plugintools.find_single_match(body, 'getJSON."(.*?)"')
    #rtmp = plugintools.find_single_match(body, "file: '([^']+)")
    tok_rtmp = plugintools.find_single_match(body, "wmsAuthSign=([^']+)")
    plugintools.log("tok_page= "+tok_page)
    body = gethttp_referer_headers(tok_page, 'http://miplayer.net/')
    tok = plugintools.find_single_match(body, 'token":"(.*?)"')
    
    plugintools.log("tok= "+tok)
    plugintools.log("tok_rtmp= "+tok_rtmp)

    media_url='rtmp://rtmp.miplayer.net/redirect?wmsAuthSign='+tok_rtmp+' token='+tok+' swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://miplayer.net live=1 timeout=15'
    plugintools.log("url= "+media_url)
    plugintools.play_resolved_url(media_url)



def gethttp_referer_headers(pageurl, referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

