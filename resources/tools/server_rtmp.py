# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Analizador de RTMPs by Juarrox (juarrox@gmail.com)
# Version 0.3.4 (28.04.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info
#------------------------------------------------------------


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools

from __main__ import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

# Regex de canales
#from resources.regex.shidurlive import *
from resources.regex.vaughnlive import *
from resources.regex.ninestream import *
from resources.regex.vercosas import *
from resources.regex.castalba import *
from resources.regex.castdos import *
from resources.regex.directwatch import *
from resources.regex.freetvcast import *
from resources.regex.freebroadcast import *
from resources.regex.sawlive import *
from resources.regex.broadcastlive import *
from resources.regex.businessapp import *
from resources.regex.rdmcast import *
from resources.regex.dinozap import *
from resources.regex.streamingfreetv import *
from resources.regex.byetv import *
from resources.regex.ezcast import *
from resources.regex.ucaster import *
from resources.regex.iguide import *


def server_rtmp(params):
    plugintools.log('[%s %s].server_rtmp %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")

    if url.find("iguide.to") >= 0:
        server = 'iguide'

    elif url.find("freetvcast.pw") >= 0:
        server = 'freetvcast'        

    elif url.find("9stream") >= 0:
        server = '9stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        
    
    elif url.find("businessapp1") >= 0:
        server = 'businessapp1'

    elif url.find("miplayer.net") >= 0:
        server = 'miplayernet'        

    elif url.find("janjua") >= 0:
        server = 'janjua'
        
    elif url.find("rdmcast") >= 0:
        server = 'rdmcast'        

    elif url.find("freebroadcast") >= 0:
        server = 'freebroadcast'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'        

    elif url.find("goodgame.ru") >= 0:
        server = 'goodgame.ru'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("hdcast") >= 0:
        server = 'hdcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("sharecast") >= 0:
        server = 'sharecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("cast247") >= 0:
        server = 'cast247'

    elif url.find("castalba") >= 0:
        server = 'castalba'

    elif url.find("direct2watch") >= 0:
        server = 'direct2watch'        

    elif url.find("vaughnlive") >= 0:
        server = 'vaughnlive'        

    elif url.find("sawlive") >= 0:
        server = 'sawlive'        

    elif url.find("streamingfreetv") >= 0:
        server = 'streamingfreetv'        

    elif url.find("totalplay") >= 0:
        server = 'totalplay'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("shidurlive") >= 0:
        server = 'shidurlive'        

    elif url.find("everyon") >= 0:
        server = 'everyon'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("iviplanet") >= 0:
        server = 'iviplanet'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("cxnlive") >= 0:
        server = 'cxnlive'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("ucaster") >= 0:
        server = 'ucaster'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("mediapro") >= 0:
        server = 'mediapro'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'        

    elif url.find("veemi") >= 0:
        server = 'veemi'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("yukons.net") >= 0:
        server = 'yukons.net'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("janjua") >= 0:
        server = 'janjua'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'
        

    elif url.find("mips") >= 0:
        server = 'mips'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'
        

    elif url.find("zecast") >= 0:
        server = 'zecast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'
        

    elif url.find("vertvdirecto") >= 0:
        server = 'vertvdirecto'      

    elif url.find("filotv") >= 0:
        server = 'filotv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'

    elif url.find("dinozap") >= 0:
        server = 'dinozap'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("ezcast") >= 0:
        server = 'ezcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'
        

    elif url.find("flashstreaming") >= 0:
        server = 'flashstreaming'
        if url.find("timeout") < 0:
            url = url + ' timeout=15'
        

    elif url.find("shidurlive") >= 0:
        server = 'shidurlive'       

    elif url.find("multistream") >= 0:
        server = 'multistream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("playfooty") >= 0:
        server = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'
                params["url"]=url        

    elif url.find("flashtv") >= 0:
        server = 'flashtv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
                params["url"]=url
            else:
                url = url + ' timeout=15'        

    elif url.find("04stream") >= 0:
        server = '04stream'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("vercosas") >= 0:
        server = 'vercosasgratis'       

    elif url.find("broadcastlive") >= 0:
        server = 'broadcastlive'
        
    elif url.find("dcast") >= 0:
        server = 'dcast'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("playfooty") >= 0:
        server = 'playfooty'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    elif url.find("pvtserverz") >= 0:
        server = 'pvtserverz'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'

    elif url.find("byetv") >= 0:
        server = 'byetv'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'                

    else:
        server = 'rtmp'
        if url.find("timeout") < 0:
            if url.endswith("conn=S:OK") == True:  # Control para aquellos servidores que requieran al final de la URL la expresión: conn=S:OK
                url = url.replace("conn=S:OK", "").strip()
                url = url + ' timeout=15 conn=S:OK'
            else:
                url = url + ' timeout=15'        

    params["url"] = url
    params["server"] = server
    
    



def launch_rtmp(params):
    plugintools.log('[%s %s].launch_rtmp %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    title = params.get("title")
    title = title.replace("[/COLOR]", "")
    title = title.strip()
    plugintools.log("Vamos a buscar en el título: "+title)

    if title.endswith("[9stream]") == True:        
        server = '9stream'
        ninestreams(params)

    elif title.endswith("[iguide]") == True:
        server = 'iguide'
        iguide0(params)

    elif title.endswith("[streamingfreetv]") == True:
        server = 'streamingfreetv'
        streamingfreetv0(params)

    elif title.endswith("[vercosasgratis]") == True:
        server = 'vercosasgratis'
        vercosas(params)

    elif title.endswith("[freebroadcast]") == True:
        server = 'freebroadcast'
        freebroadcast(params)

    elif title.endswith("[ucaster]") == True:
        server = 'ucaster'
        ucaster0(params)

    elif title.endswith("[direct2watch]") == True:
        server = 'direct2watch'
        directwatch(params)

    elif title.endswith("[shidurlive]") == True:
        server = 'shidurlive'
        plugintools.play_resolved_url(url)

    elif title.endswith("[vaughnlive]") == True:
        server = 'vaughnlive'
        resolve_vaughnlive(params)        

    elif title.endswith("[cast247]") == True:
        server = 'cast247'
        castdos(params)

    elif title.endswith("[ezcast]") == True:
        server = 'ezcast'
        ezcast0(params)        

    elif title.endswith("[businessapp1]") == True:
        server = 'businessapp'
        businessapp0(params)

    elif title.endswith("[miplayer.net]") == True:
        server = 'miplayernet'
        miplayernet0(params)        

    elif title.endswith("[janjua]") == True:
        server = 'janjua'
        janjua0(params)        

    elif title.endswith("[rdmcast]") == True:
        server = 'rdmcast'
        rdmcast0(params)        

    elif title.endswith("[byetv]") == True:
        server = 'byetv'        
        byetv0(params)       

    elif url.find("hdcast") >= 0:
        server = 'hdcast'
        plugintools.play_resolved_url(url)

    elif url.find("janjua") >= 0:
        server = 'janjua'
        janjua0(params)

    elif url.find("mips") >= 0:
        server = 'mips'
        plugintools.play_resolved_url(url)

    elif url.find("zecast") >= 0:
        server = 'zecast'
        plugintools.play_resolved_url(url)

    elif url.find("filotv") >= 0:
        server = 'filotv'
        print "filotv"
        plugintools.play_resolved_url(url)

    elif url.find("flashstreaming") >= 0:
        server = 'flashstreaming'
        plugintools.play_resolved_url(url)

    elif url.find("multistream") >= 0:
        server = 'multistream'
        print "multistream"
        plugintools.play_resolved_url(url)

    elif url.find("playfooty") >= 0:
        server = 'playfooty'
        plugintools.play_resolved_url(url)

    elif url.find("flashtv") >= 0:
        server = 'flashtv'
        print "flashtv"
        plugintools.play_resolved_url(url)

    elif url.find("freetvcast") >= 0:
        server = 'freetvcast'
        print "freetvcast"
        freetvcast(params)

    elif url.find("04stream") >= 0:
        server = '04stream'
        plugintools.play_resolved_url(url)

    elif url.find("sharecast") >= 0:
        server = 'sharecast'
        plugintools.play_resolved_url(url)

    elif url.find("sawlive") >= 0:
        server = 'sawlive'
        sawlive(params)

    elif url.find("goodcast") >= 0:
        server = 'goodcast'
        plugintools.play_resolved_url(url)

    elif url.find("broadcastlive") >= 0:
        server = 'broadcastlive'        
        broadcastlive1(params)

    elif url.find("dinozap") >= 0:
        server = 'dinozap'        
        dinozap0(params)        

    elif url.find("dcast.tv") >= 0:
        server = 'dcast.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castalba") >= 0:
        server = 'castalba'
        castalba(params)

    elif url.find("tutelehd.com") >= 0:
        server = 'tutelehd.com'
        plugintools.play_resolved_url(url)

    elif url.find("flexstream") >= 0:
        server = 'flexstream'
        plugintools.play_resolved_url(url)

    elif url.find("xxcast") >= 0:
        server = 'xxcast'
        plugintools.play_resolved_url(url)

    elif url.find("vipi.tv") >= 0:
        server = 'vipi.tv'
        plugintools.play_resolved_url(url)

    elif url.find("watchjsc") >= 0:
        server = 'watchjsc'
        plugintools.play_resolved_url(url)

    elif url.find("zenex.tv") >= 0:
        server = 'zenex.tv'
        plugintools.play_resolved_url(url)

    elif url.find("castto") >= 0:
        server = 'castto'
        plugintools.play_resolved_url(url)

    elif url.find("tvzune") >= 0:
        server = 'tvzune'
        plugintools.play_resolved_url(url)

    elif url.find("flashcast") >= 0:
        server = 'flashcast'
        plugintools.play_resolved_url(url)

    elif url.find("ilive.to") >= 0:
        server = 'ilive.to'
        plugintools.play_resolved_url(url)

    elif url.find("janjua") >= 0:
        server = 'janjua'        
        janjua0(params)          

    else:
        print "No ha encontrado launcher"
        server = 'rtmp'        
        plugintools.play_resolved_url(url)

