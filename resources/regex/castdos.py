# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de cast247
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
def castdos(params):
    plugintools.log("[beta.1-0.3.0].cast247 "+repr(params))
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

    if url_user.get("pageurl").find("domain=") <= 0:
        plugintools.log("URL_user dict= "+repr(url_user))
        pageurl = url_user.get("pageurl")
        body = gethttp_headers(pageurl)
        
        # Controlamos el caso de canal privado (requiere referer, por implementar)
        if body.find("Private Channel!") > 0 :
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Canal privado", 3 , art+'icon.png'))
            return 0
        else:
            pageurl = re.compile('var sURL = \"(.*?)=\"').findall(body)
            pageurl = 'http://www.cast247.tv/' + pageurl[0]
            real_token = gethttp_headers(pageurl)

        # Iniciamos captura de parámetros
        streamer = re.compile('streamer: "(.*?)"').findall(body)
        file = re.compile('file: "(.*?)"').findall(body)

        url_user["rtmp"] = streamer[0]
        url_user["playpath"] = file[0]
        url_user["pageurl"] = pageurl
                
        # Construimos la URL original
        url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' live=1 timeout=20'
        url = url.strip()
        plugintools.log("url= "+url)
        plugintools.play_resolved_url(url)
        
    else:
        plugintools.log("URL_user dict= "+repr(url_user))
        # http://www.cast247.tv/embed.php?channel=plusjdskaks?&amp;width=670&amp;height=400&amp;domain=streamingfreetv.net
        # http://www.cast247.tv/embed.php?channel=plusjdskaks&width=670&height=400&domain=streamingfreetv.net (url_user)
        pageurl = url_user.get("pageurl")
        url_user["referer"]=pageurl
        width = plugintools.find_single_match(pageurl, 'width=(.*?)\&')
        height = plugintools.find_single_match(pageurl, 'height=(.*?)&')
        playpath = plugintools.find_single_match(pageurl, 'channel=(.*?\&')
        # playpath = url_user.get("playpath").split("?")
        playpath = re.compile('channel=(.*?)&').findall(pageurl)
        print 'width',width
        print 'height',height
        print 'channel',playpath
        new_playpath = playpath[0]
        domain = pageurl.split("=")
        i = len(domain)
        domain = domain[int(i)-1]
        new_pageurl = 'http://www.cast247.tv/embed.php?channel=' + new_playpath + '&width=' + width + '&height=' + height + '&domain=' + domain
        plugintools.log("new_pageurl= "+new_pageurl)
        url_user["pageurl"]=new_pageurl
        body = gethttp_referer_headers(url_user)
        plugintools.log("body= "+body)

        pageurl = re.compile('var sURL = \"(.*?)=\"').findall(body)
        pageurl = 'http://www.cast247.tv/' + pageurl[0]
        real_token = gethttp_headers(pageurl)        

        # Iniciamos captura de parámetros
        streamer = re.compile('streamer: "(.*?)"').findall(body)
        print 'streamer',streamer
        playpath = re.compile('file: "(.*?)"').findall(body)
        print 'playpath',playpath        
        url_user["rtmp"] = streamer[0]
        url_user["playpath"] = playpath[0]        

        # Construimos la URL original
        url = url_user.get("rtmp") + ' playpath=' + url_user.get("playpath") + ' live=1 timeout=20'
        url = url.strip()
        plugintools.log("url= "+url)
        plugintools.play_resolved_url(url)        
        

                                               

# Vamos a hacer una llamada a la página que nos dará el token
def gethttp_headers(pageurl):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
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
