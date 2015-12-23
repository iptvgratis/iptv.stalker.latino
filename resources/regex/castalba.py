# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de castalba
# Version 0.1 (01.12.2014)
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


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.t-killa/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.t-killa/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.t-killa/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.t-killa/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.t-killa/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'



# En construcción!
def castalba(params):
    plugintools.log("[beta.1-0.3.0].castalba "+repr(params))

    url = params.get("url")
    plugintools.play_resolved_url(url)


# Función que guía el proceso de elaboración de la URL original
def castalba(params):
    plugintools.log("[beta.1-0.3.0].castalba "+repr(params))
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


    # Controlamos el caso de canal privado (requiere referer, por implementar)
    if body.find("THIS CHANNEL IS CURRENTLY OFFLINE") > 0 :
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Canal offline", 3 , art+'icon.png'))
        return 0
    else:
    
        # Iniciamos captura de parámetros
        file = re.compile('file\': \'(.*?)\',').findall(body)
        if file[0].endswith("m3u8"):
            plugintools.play_resolved_url(file[0])
        else:
            streamer = re.compile('streamer\': \'(.*?)\',').findall(body)
            print 'file',file
            print 'streamer',streamer
            url_user["playpath"] = file[0]
            url_user["rtmp"] = streamer[0]            
            # Construimos la URL original
            url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' swfUrl=http://static.castalba.tv/player5.9.swf pageUrl=' + url_user.get("pageurl") + ' live=true timeout=15'
            url = url.strip()
            plugintools.log("url= "+url)
            plugintools.play_resolved_url(url)
        
 
# Vamos a hacer una llamada a la página que nos dará el token
def gethttp_headers(pageurl):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", pageurl])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

	
def gethttp_referer_headers(url_user):

    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    print 'referer',referer
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body
    
