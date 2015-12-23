# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de freetvcast
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


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



def freetvcast(params):
    plugintools.log("[beta.1-0.3.0].resolve_freetvcast " + repr(params) )

    freetvcast_user = {"rtmp": "" , "playpath":'', "swfurl": "http://freetvcast.pw/player.swf" , "pageurl": "http://freetvcast.pw/", "token":'#ed%h0#w@12Fuck', "live":'True', "timeout":'15', "referer":''}

    # Construimos diccionario 'freetvcast_user'
    url = params.get("url")
    url = url.strip()
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            freetvcast_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            freetvcast_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            freetvcast_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            freetvcast_user["pageurl"]=entry
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            freetvcast_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            freetvcast_user["referer"]=entry             
            

    # Vamos a obtener el playpath y el rtmp (streamer)
    pageurl = freetvcast_user.get("pageurl")
    referer = freetvcast_user.get("referer")
    body = gethttp_headers(pageurl, referer)
    plugintools.log("body= "+body)

    rtmp = re.compile("'streamer', '([^']*)").findall(body)
    print 'rtmp',rtmp
    freetvcast_user["rtmp"]=rtmp[0]
    app = rtmp[0]
    app = app.split("token=")
    app = app[1]
    freetvcast_user["app"]=app

    playpath = re.compile("'file', '([^']*)").findall(body)
    print 'playpath',playpath
    freetvcast_user["playpath"]=playpath[0]

    play_freetvcast(freetvcast_user)
    
    
# Vamos a hacer una llamada al pageUrl
def gethttp_headers(pageurl, referer):
    plugintools.log("pageUrl= "+pageurl)
    plugintools.log("referer= "+referer)
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    return body


    rtmp_server = matches[0]        
    vaughnlive_user["rtmp"] = 'rtmp://' + rtmp_server + '/live?'
    body = body.replace(rtmp_server, "")
    body = body.replace("0m0", "")
    body = body.replace(";", "")
    
    decrypted = decrypt_vaughnlive(body)
    plugintools.log("decrypted= "+decrypted)
    
    rtmp_fixed = vaughnlive_user.get("rtmp") + decrypted
    vaughnlive_user["rtmp"]=rtmp_fixed
    play_vaughnlive(vaughnlive_user, params)
    

def play_freetvcast(freetvcast_user):
    plugintools.log("[beta.1-0.3.0].freetvcast User= " + repr(freetvcast_user) )
    
    # Construimos la URL decodificada...
    url = freetvcast_user.get("rtmp") + " playpath=" + freetvcast_user.get("playpath") + " token=" + freetvcast_user.get("token") + " swfUrl=http://freetvcast.pw/player.swf pageUrl=" + freetvcast_user.get("pageurl") + " live=true timeout=15"
    url = url.strip()
    plugintools.play_resolved_url(url)       


  
