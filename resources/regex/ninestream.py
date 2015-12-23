# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de 9straem
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
def ninestreams(params):
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
    
    # Controlamos ambos casos de URL: Único link (pageUrl) o link completo rtmp://...
    if pageurl is None:
        pageurl = url_user.get("url")
        
    referer= url_user.get("referer")
    if referer is None:
        referer = 'http://www.verdirectotv.com'
    channel_id = re.compile('channel=([^&]*)').findall(pageurl)
    channel_id = channel_id[0]
    # http://www.9stream.com/embedplayer.php?width=650&height=400&channel=143&autoplay=true

    if pageurl.find("embedplayer.php") >= 0 :
        body = gethttp_headers(pageurl, referer)
        plugintools.log("body= "+body)
        url_user = getparams_ninestream(url_user, params, body)
        pageurl = url_user.get("pageurl")
        pageurl = 'http://www.9stream.com/embedplayer.php?width=650&height=400&channel=' + channel_id + '&autoplay=true'
        url_user["pageurl"]=pageurl
        print url_user
        url = 'rtmp://' + url_user.get("rtmp") + ':1935/verdirectotvedge/_definst_/ app=verdirectotvedge/_definst_/?xs=' + url_user.get("ninetok") + ' playpath=' + url_user.get("playpath") + ' token=' + url_user.get("token") + ' flashver=WIN%2011,9,900,117 swfUrl=http://www.9stream.com/player/player_orig_XXXXX.swf pageUrl=' + url_user.get("pageurl") + ' live=1 swfVfy=1 timeout=10'
        plugintools.play_resolved_url(url)          
        
    else:
        body = gethttp_headers(pageurl, referer)
        plugintools.log("body= "+body)
        body = ioncube1(body)
        url_user = getparams_ninestream(url_user, params, body)
        pageurl = url_user.get("pageurl")
        pageurl = 'http://www.9stream.com/embedplayer_2.php?width=650&height=400&channel=' + channel_id + '&autoplay=true'
        url_user["pageurl"]=pageurl
        ninetok = get_fileserver(decoded, url_user)
        print 'ninetok',ninetok
        url_user["token"]=ninetok
        print 'url_user',url_user
        url = 'rtmp://' + url_user.get("rtmp") + ':1935/verdirectotvedge/_definst_/ app=verdirectotvedge/_definst_/?xs=' + url_user.get("ninetok") + ' playpath=' + url_user.get("playpath") + ' token=' + url_user.get("token") + ' flashver=WIN%2011,9,900,117 swfUrl=http://www.9stream.com/player/player_orig_XXXXX.swf pageUrl=' + url_user.get("pageurl") + ' live=1 swfVfy=1 timeout=10'
        plugintools.play_resolved_url(url)        



# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


                
# Iniciamos protocolo de elaboración de la URL original
# Capturamos parámetros correctos
def getparams_ninestream(url_user, params, body):
    plugintools.log("[beta.1-0.3.0].getparams_ninestream " + repr(url_user) )
    
    # Construimos el diccionario de 9stream
    plugintools.log("body= "+body)
    entry = plugintools.find_single_match(body, 'setStream(token) {(.*?)}')
    ip = re.compile('rtmp:....([^:]*)').findall(body)   
    url_user["rtmp"]=str(ip[0])
    plugintools.log("IP= "+str(ip[0]))
    xs = re.compile('xs=(.*?)"').findall(body)
    ninetok = xs[0]
    url_user["xs"] = ninetok
    decoded = url_user.get("pageurl")
    playpath = getfile_ninestream(url_user, decoded, body)   
    playpath = playpath[0]
    # ninetok = xs[0] + './' + playpath
    ninetok = xs[0]
    url_user["ninetok"]=ninetok
    plugintools.log("xs= "+ninetok)
    url_user["xs"] = ninetok
    url_user["playpath"]=playpath
    decoded=re.compile('getJSON\("(.*?)"').findall(body)
    decoded=decoded[0]
    token = get_fileserver(decoded, url_user)
    token = token[0]
    url_user["token"]=token
    return url_user


 

# Vamos a capturar el playpath
def getfile_ninestream(url_user, decoded, body):
    plugintools.log("beta.1 getfile_ninestream( "+repr(url_user))
    referer = url_user.get("referer")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer', referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    file = re.compile("file': '([^.]*)").findall(data)
    print 'file',file
    return file


# Vamos a capturar el fileserver.php (token del server)
def get_fileserver(decoded, url_user):
    plugintools.log("beta.1 fileserver "+repr(url_user))
    referer=url_user.get("pageurl")
    req = urllib2.Request(decoded)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Referer',referer)
    response = urllib2.urlopen(req)
    print response
    data = response.read()
    print data
    token = re.compile('token":"(.*)"').findall(data)
    print 'token',token
    return token
