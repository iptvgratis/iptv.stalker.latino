# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de vaughnlive
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
import time


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


def resolve_vaughnlive(params):
    plugintools.log("[beta.1-0.3.0].resolve_vaughnlive " + repr(params) )

    vaughnlive_user = {"rtmp": "" , "swfurl": "http://vaughnlive.tv/800021294/swf/VaughnSoftPlayer.swf" , "pageurl": "http://www.vaughnlive.tv/", "token":'#ed%h0#w18623jsda6523l'}

    # Construimos diccionario 'vaughn_user'
    url = params.get("url")
    url = url.strip()
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            vaughnlive_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            vaughnlive_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            vaughnlive_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            vaughnlive_user["pageurl"]=entry
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            vaughnlive_user["token"]=entry           
    
    # rtmp://198.255.0.10:443/live?9LdRvrakvwT0SarNUJY6gaNMTm7xtHfY playpath=live_lmshows_at live=1 timeout=20

    # rtmp://192.240.125.26:443/live?YNRqBuQERAV2O2kvNzETwzaQyIdAZrqj playpath=live_lmshows_at live=1 timeout=20

    # LSP:     rtmp://198.255.5.66:443/live?0n0qMt6OtXhOLwQKIwSoxVdmXHiYW8nVZSY playpath=live_dibujos_animados live=1 timeout=20
    # beta.1: rtmp://198.255.5.66:443/live?0n0qMt6OtXhOLwQKIwSoxVdmXHiYW8nVZSY playpath=live_dibujos_animados live=1 timeout=20

    ret_val = ""
    ret_val=str(int(round(time.time() * 1000)))
    pageurl = 'http://mvn.vaughnsoft.net/video/edge/live_dibujos_animados-'+ret_val+'.33434'    
    body = gethttp_noref(pageurl)
    body = body.strip()
    plugintools.log("body= "+body)
    body = body.split(";")
    token = body[1].replace(":mvnkey-", "").strip()

    pageurl = vaughnlive_user.get("pageurl")
    body=gethttp_noref(pageurl)
    getedge = plugintools.find_single_match(body, '{ return \"(.*?)\"')
    getedge = getedge.split(",")
    getedge = getedge[0]
    plugintools.log("getedge= "+getedge)    
    url = 'rtmp://'+getedge+'/live?'+token+ ' playpath='+vaughnlive_user.get("playpath")+' live=1 timeout=20'
    print 'url',url
    plugintools.play_resolved_url(url)


def gethttp_noref(url):
    plugintools.log("[beta.1-0.3.0.Vaughn_Regex] ")    

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
    
