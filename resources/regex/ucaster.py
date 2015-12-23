# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Regex de Businessapp1
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

from __main__ import *
from resources.tools.nstream import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


def ucaster0(params):
    plugintools.log('[%s %s] Initializing Ucaster regex... %s' % (addonName, addonVersion, repr(params)))
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
    ref = url_user.get("referer")
    plugintools.log("url= "+url)
    plugintools.log("ref= "+ref)

    bodi=gethttp_referer(url,ref,body='')
    p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ucaster.eu'+plugintools.find_single_match(bodi,p);
    p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);print flashvars;
    p = re.compile(ur'\&?.*?=([^\&]+)');flashvars=re.findall(p,flashvars);print flashvars;id=flashvars[0];c=flashvars[1];
    lb='http://www.ucaster.eu:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');print lb
    media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+'&pk='+flashvars[4]+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl=http://www.embeducaster.com/ live=true timeout=15'
    # 
    plugintools.play_resolved_url(media_url)
    print "MEDIA URL="+media_url

	

def jscalpe(bodyy,url,ref):
    print "jscalpe(bodyy,url,ref)";p=('m3u8','freelivetv','freetvcast','goo\.gl','vercosasgratis','verdirectotv','byetv','9stream','castalba','direct2watch','kbps','flashstreaming','cast247','ilive','freebroadcast','flexstream','mips','veemi','yocast','yukons','ilive','iguide','ucaster','ezcast','plusligaonline','tvonlinegratis','dinozap','businessapp1');z=len(p);
    for i in range(0,z):
        regex='<script.*?('+str(p[i])+').*?<\/script>';caster=[];enctrd=plugintools.find_single_match(bodyy,regex);
        #!!!Quita el "if" de abajo para ver todo los "enctrd" encontrados de cada "p" caster !!!
        if len(enctrd)>0:
            caster=''.join(map(str,enctrd));print caster;
            r = re.compile('(<script.*?(?=>)>(.*?)(?=<))?.*?src=\'?"?(.*?'+caster+'[^\'",;]+)', re.VERBOSE);res = re.findall(r,bodyy);
        if caster.find('m3u8') >=0:
            r = 'file=(.*?m3u8)'
            res = plugintools.find_single_match(bodyy,r);
            res=filter(None,res);res=str(res);script='';
            nstream2(url,ref,caster,res,script)
        else: res=filter(None,res);print res
        res=list(set(res));
        script=''.join(map(str,res));
        #print cipqq,url,ref,caster,res,script;sys.exit();        
        if caster == 'ucaster': ucaster(url,ref,res)
        else: print "\nNSCRIPT = "+str(script);print "\nURL = "+url;print "\nREFERER = "+str(ref);print "\nCASTER = "+str(caster);




def curl_frame(url,ref,body,bodyi,bodyy,urli):
 request_headers=[];request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"]);request_headers.append(["Referer",ref])
 try: body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);#print "HEADERS:\n";print response_headers
 except: pass
 try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
 except: pass
 try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
 except: pass
 if loc:
  request_headers.append(["Referer",url]);
  if jar: request_headers.append(["Cookie",jar]);#print jar
  body,response_headers=plugintools.read_body_and_headers(loc,headers=request_headers);
  try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
  except: pass
 if body: bodyi+=([body]);
 return body


def gethttp_referer(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	#print "HEADERS:N";print response_headers
	return body
    


def find_multiple_matches_multi(text,pattern):
    matches = re.findall(pattern,text, re.MULTILINE)
    return matches
