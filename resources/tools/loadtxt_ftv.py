# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 EPG FórmulaTV.com
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#------------------------------------------------------------

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
from datetime import datetime

from resources.tools.txt_reader import TextBoxes

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

tmp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
FANART = "fanart"
OTHER = "other"
MUSIC = "music"


def epg_txt0(params):
    plugintools.log('[%s %s].epg_ftv %s' % (addonName, addonVersion, repr(params)))
    channel = title.lower()
    channel = channel.replace("Opción 1", "").replace("HD", "").replace("720p", "").replace("1080p", "").replace("SD", "").replace("HQ", "").replace("LQ", "").strip()
    channel = channel.replace("Opción 2", "")
    channel = channel.replace("Opción 3", "")
    channel = channel.replace("Op. 1", "")
    channel = channel.replace("Op. 2", "")
    channel = channel.replace("Op. 3", "")
    #plugintools.log("Canal: "+channel)
    params = plugintools.get_params()
    
    if channel == "la 1" or channel == "la 1 hd":
        channel = "la 1"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params)        
    elif channel == "la 2":
        channel = "la2"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params)          
    elif channel == "antena 3" or channel == "antena 3 hd":
        channel = "antena3"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params) 
    elif channel == "cuatro" or channel == "cuatro hd":
        channel = "cuatro"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params)       
    elif channel == "telecinco hd" or channel == "telecinco":
        channel == "telecinco"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params)      
    elif channel == "la sexta" or channel == "la sexta hd":
        channel = "lasexta"
        params["url"]='http://www.formulatv.com/programacion/'+channel+'/'
        epg_txt1(params)        


def epg_txt1(params):
    plugintools.log('[%s %s].epg_formulatv %s' % (addonName, addonVersion, repr(params)))
    
    # Calculamos la fecha de hoy
    ahora = datetime.now()
    hoy = ahora.day + ahora.month + ahora.year
    print hoy

    url = 'http://www.formulatv.com/programacion/la1/'
    channel = 'la1'
    epg_txt = tmp + channel+'-'+str(hoy)+'.txt'

    if os.path.exists(epg_txt):
        file_epg = open(epg_txt, "r")
    else:
        file_epg = open(epg_txt, "a")
        data = plugintools.read(url)        
        
        # Abrimos epg_txt
        #plugintools.log("data= "+data)

        # Cabecera del txt...
        cabecera = plugintools.find_single_match(data, '<h2 class="nt">(.*?)</h2>')
        #print cabecera
        file_epg.write('[COLOR gold]'+cabecera+'[/COLOR]\n')
        subcabecera = plugintools.find_single_match(data, '<h3 class="nt">(.*?)</h3>')
        #print subcabecera
        file_epg.write('[COLOR orange]'+subcabecera+'[/COLOR]\n\n')

        # Bloque de programación
        schedule = plugintools.find_single_match(data, '<div class="prg-item"(.*?)</style>')
        evento = plugintools.find_multiple_matches(schedule, '<div class="prg-item"(.*?)<p class="subtit">')
        for entry in evento:
            #plugintools.log("entry= "+entry)
            event_time = plugintools.find_single_match(entry, '<div class="prg-hour"><p>(.*?)</p>')
            if event_time != "":
                event_title = plugintools.find_single_match(entry, '<p class="tit">[^>]+>(.*?)</p>')
                if event_title == "":
                    event_title = plugintools.find_single_match(entry, '<p class="tit">(.*?)</p>')
                event_title = event_title.replace("</a>", "")
                file_epg.write('[B]'+event_time+'[/B] '+event_title+'\n')

    txt_file = channel+'-'+str(hoy)+'.txt'
    file_epg.close()
    #xbmc.sleep(500)
    TextBoxes("[B][COLOR lightyellow][I]playlists / [/B][/COLOR][/I] "+txt_file,epg_txt)            



    
        


    
