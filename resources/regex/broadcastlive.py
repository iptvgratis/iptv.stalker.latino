# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de Businessapp1 y Broadcastlive
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import urllib
import urllib2
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, scrapertools
import sys,traceback,urllib2,re


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


# Función que guía el proceso de elaboración de la URL original
def broadcastlive0(params):
    plugintools.log('[%s %s] Initializing 1Broadcastlive regex... %s' % (addonName, addonVersion, repr(params)))
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url");print url
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

    url = url_user.get("pageurl")
    ref = url_user.get("referer")
    plugintools.log("url= "+url)
    plugintools.log("ref="+ref)
    
    bodi=gethttp_referer_headers(url,ref);ref=url;p='(width|height|channel)=\'?([^,\']+)';p=plugintools.find_multiple_matches(bodi,p);
    url='http://1broadcastlive.com/embed/embed.php?channel='+p[2][1]+'&w='+p[0][1]+'&h='+p[1][1];bodi=gethttp_referer_headers(url,ref);
    p='<param\sname=\'(movie|flashvars)\'\svalue=\'([^\']+)';p=plugintools.find_multiple_matches(bodi,p);
    app='redirect'+p[1][1].split('&')[1].split('=',1)[1].split('redirect')[1];w=p[1][1].split('&')[1].split('=',1)[1]+' app='+app+' playpath='+p[1][1].split('&')[0].split('=')[1]+' flashver=WIN%2016,0,0,305 swfUrl='+p[0][1].lower()+' swfVfy=1 live=1 pageUrl='+url;
    if w: plugintools.play_resolved_url(w);sys.exit();
    else: eval(nolink);sys.exit();


def broadcastlive1(params):
    plugintools.log('[%s %s] Initializing 1Broadcastlive regex... %s' % (addonName, addonVersion, repr(params)))
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
    url = url_user.get("pageurl")
    ref = url_user.get("referer")
    if ref is None:
        ref = 'http://1broadcastlive.com/'
    body = gethttp_referer_headers(url,ref)
    match = plugintools.find_single_match(body, '<param name=\'movie\'(.*?)</object>')
    print match
    swf = plugintools.find_single_match(match, 'value=\'(.*?)\'>')
    app = plugintools.find_single_match(match, 'id=\'(.*?)\'')
    url_user["swf"] = swf.lower()    
    rtmp = plugintools.find_single_match(match, 'streamer=(.*?)false')
    rtmp_fixed = rtmp.split("redirect?")
    rtmp = rtmp_fixed[1]
    rtmp = rtmp.replace("&autostart=", "")
    url_user["playpath"]= plugintools.find_single_match(match, 'file=(.*?)&')
    plugintools.log("swf= "+url_user.get("swf"))    
    plugintools.log("playpath= "+url_user.get("playpath"))

    url = 'rtmp://188.165.213.105/redirect?'+rtmp+ ' playpath=' + url_user.get("playpath") + ' swfUrl=http://1broadcastlive.com/embed/noreproductor.php?o=1&amp;kpublica=29245 pageUrl=http://1broadcastlive.com/ live=true timeout=20'
    plugintools.play_resolved_url(url)

   

def gethttp_referer_headers(url,ref):
    plugintools.log("url= "+url)
    plugintools.log("ref= "+ref)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

