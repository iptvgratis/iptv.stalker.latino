# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de direct2watch
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
def iguide0(params):
    plugintools.log("[beta.1-0.3.0].directwatch "+repr(params))
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
    plugintools.log("url= "+url);plugintools.log("ref= "+ref)

    body = gethttp_referer_headers(url,ref)
    print body

    rtmp = plugintools.find_single_match(body, "'streamer': '(.*?)'")
    playpath = plugintools.find_single_match(body, "'file': '(.*?).flv'")
    plugintools.log("rtmp= "+rtmp)
    plugintools.log("playpath= "+playpath)
    media_url = rtmp + ' playpath='+playpath+' swfUrl=http://cdn.iguide.to/player/secure_player_iguide_embed_token.swf pageUrl='+url+' token=#ed%h0#w18623jsda6523lDGD'
    plugintools.log("U R L = "+media_url)
    plugintools.play_resolved_url(media_url)

    
                                            

def gethttp_referer_headers(url,ref):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body



