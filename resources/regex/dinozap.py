# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de Dinozap
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


def dinozap0(params):
    plugintools.log('[%s %s] Initializing Businessapp regex... %s' % (addonName, addonVersion, repr(params)))
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

    url = url_user.get("pageurl")
    ref = 'http://www.dinozap.info/'
    body='';body=gethttp_referer_headers(url,ref)
    reff=url;url=plugintools.find_single_match(body,'iframe\ssrc="([^"]+)');
    for i in range(1,10):
        k=url;body=gethttp_referer_headers(url,reff);
        scrpt='document\.write\(unescape\(\'([^\']+)';scrpt=plugintools.find_single_match(body,scrpt)
        tok='securetoken([^\n]+)';tok=plugintools.find_single_match(body,tok);
        try: hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
        except: i-=1;
        diov='var\s(sUrl|cod1)\s=\s\'([^\']+)';diov=plugintools.find_multiple_matches(body,diov);#print diov;
        Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));jquery = '%s?callback=jQuery17049106340911455604_%s&v_cod1=%s&v_cod2=%s&_=%s';
        jurl=jquery%(hidd[3][1].decode('base64'),Epoc_mil,urllib.quote_plus(hidd[1][1]),urllib.quote_plus(hidd[2][1]),Epoc_mil);r='"result\d{1}":"([^"]+)';p='plugintools.find_multiple_matches(body,r)';
        body=gethttp_referer_headers(jurl,k);x=eval(p)[0];print jurl
        if x=='not_found': print 'try '+str(i)+' : '+x;
        else: print 'try '+str(i)+' : OK :)';break;
    if x=='not_found': eval(nolink);sys.exit();
    swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(eval(p)[1].replace('\\',''),'1735\/([^"]+)'); q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
    w=eval(p)[1].replace('\\','')+' app='+app+' playpath='+eval(p)[0]+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
    if w: plugintools.play_resolved_url(w);sys.exit();
    else: eval(nolink);sys.exit();


   

def gethttp_referer_headers(url,ref):
    plugintools.log("url= "+url)
    plugintools.log("ref= "+ref)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


def gethttp_headers(url):
    plugintools.log("url= "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body


