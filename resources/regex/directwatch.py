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
def directwatch(params):
    plugintools.log("[beta.1-0.3.0].directwatch "+repr(params))
    url_user = {}
    url_user["token"]='KUidj872jf9867123444'
    url_user["rtmp"]='rtmp://watch.direct2watch.com/direct2watch'
    url_user["swfurl"]='http://www.direct2watch.com/player/player2.swf'    
    
    
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
        ref = 'http://www.vipracing.tv'
        
    res = gethttp_referer_headers(pageurl, referer)

    try:
        from roja import new_frame
        refi=ref
        body,jar,resp,ref=new_frame(res[0][2],ref,'','')
        url=plugintools.find_single_match(body,'src=\'([^\']+)')
        body,jar,resp,ref=new_frame(url,refi,'',jar)
        p = re.compile(ur'(\$\.getJSON\(\'?"?.*?)<\/script>', re.DOTALL)
        pars=re.findall(p,body);pars=str(pars[0]);pars=pars.replace("\n","").replace("\t","")
        tokserv=plugintools.find_single_match(str(pars),'getJSON\(\'?"?([^\'"]+)');
        strmr=plugintools.find_single_match(str(pars),'streamer\'?"?:\s?\'?"?([^\'"]+)');
        plpath=plugintools.find_single_match(str(pars),'file\'?"?:\s?\'?"?([^\.]+)');
        if plpath=="'": plpath=res;
        swf=plugintools.find_single_match(str(pars),'flash\'?"?,\s?src\'?"?:\s?\'?"?([^\'"]+)');
        body='';tok=gethttp_referer_headers(tokserv,url);tok=plugintools.find_single_match(str(tok),'token":"([^"]+)');
        media_url = str(strmr)+' playpath='+str(plpath)+' flashver='+urllib.quote_plus('WIN 14,0,0,176')+' swfUrl='+str(swf)+' timeout=15 live=1 pageUrl='+url+' token='+tok
        plugintools.play_resolved_url(media_url)

    except:
        print url,res,ref
        body='';body=gethttp_referer_headers(pageurl, referer);
        p = re.compile(ur'(\$\.getJSON\(\'?"?.*?)<\/script>', re.DOTALL)
        pars=re.findall(p,body);pars=str(pars[0]);pars=pars.replace("\n","").replace("\t","");
        tokserv=plugintools.find_single_match(str(pars),'getJSON\(\'?"?([^\'"]+)');
        strmr=plugintools.find_single_match(str(pars),'streamer\'?"?:\s?\'?"?([^\'"]+)');
        plpath=plugintools.find_single_match(str(pars),'file\'?"?:\s?\'?"?([^\.]+)');
        if plpath=="'": plpath=res;
        swf=plugintools.find_single_match(str(pars),'flash\'?"?,\s?src\'?"?:\s?\'?"?([^\'"]+)');
        body='';tok=gethttp_referer_headers(tokserv,url);tok=plugintools.find_single_match(str(tok),'token":"([^"]+)');
        media_url = str(strmr)+' playpath='+str(plpath)+' swfUrl='+str(swf)+' live=1 pageUrl='+url+' token='+tok
        print media_url
        plugintools.play_resolved_url(media_url)
    
    


    #p='(embed\/|\&width=|\&height=)(\d{1,3})';match=plugintools.find_multiple_matches(pageurl,p);print match
    #url='http://www.direct2watch.com/embedplayer.php?width='+match[1][1]+'&height='+match[2][1]+'&channel='+match[0][1]+'&autoplay=true'
    body=gethttp_referer_headers(pageurl,referer);
    
    try:
        p='window\.open\("([^"]+)';match=plugintools.find_multiple_matches(body,p)[1];m=match.split('/')[5];
        #print match.replace(m,'')+m.split('-')[2].replace(' ','_');sys.exit();
        #if match: body=gethttp_referer_headers(match.replace(m,'')+m.split('-')[2].replace(' ','_'),url);
    except: pass
    #print body;sys.exit()

    p='(\$\.getJSON\(|streamer\'?"?:?\s?|file\'?"?:?\s?|flash\'?"?,\s?src:?\s?)\'?"?([^\'"]+)'
    match=plugintools.find_multiple_matches_multi(body,p);print match
    tokserv = match[0][1];strmr = match[1][1].replace("\\","");plpath = match[2][1].replace(".flv","");swf = match[3][1];request_headers=[]
    request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"]);request_headers.append(["Referer",url])
    body,response_headers = plugintools.read_body_and_headers(tokserv, headers=request_headers);p=':\'?"?([^\'"]+)';tok=plugintools.find_single_match(body,p)
    media_url=strmr+"/"+plpath+" swfUrl="+swf+" live=1 token="+tok+" timeout=15 swfVfy=1 pageUrl="+url;
    plugintools.play_resolved_url(media_url)



def gethttp_referer_headers(pageurl, referer):
    plugintools.log("[beta.1-0.3.0].gethttp_headers "+pageurl)
      
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    body,response_headers = plugintools.read_body_and_headers(pageurl, headers=request_headers)      
    plugintools.log("body= "+body)
    return body

