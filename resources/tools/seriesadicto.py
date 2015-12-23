# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seriesadicto.com parser para beta.1
# Version 0.1 (20/12/2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
from resources.tools.resolvers import *


fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"

def seriecatcher(params):
    plugintools.log("[Arena+ 0.3.3].seriecatcher "+repr(params))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)    
    
    url = params.get("url")
    data = plugintools.read(url)
    temp = plugintools.find_multiple_matches(data, '<i class=\"glyphicon\"></i>(.*?)</a>')
    SelectTemp(params, temp)


def GetSerieChapters(params):
    plugintools.log("[Arena+ 0.3.3].GetSerieChapters "+repr(params))

    season = params.get("season")
    datamovie = {}
    datamovie["Plot"] = params.get("plot")
    data = plugintools.read(params.get("url"))
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)        
    
    season = plugintools.find_multiple_matches(data, season + '(.*?)</table>')
    season = season[0]
    
    for entry in season:
        url_cap = plugintools.find_multiple_matches(season, '<a href=\"/capitulo(.*?)\" class=\"color4\"')
        title = plugintools.find_multiple_matches(season, 'class=\"color4\">(.*?)</a>')

    num_items = len(url_cap)    
    i = 1
    
    while i <= num_items:
        url_cap_fixed = 'http://seriesadicto.com/capitulo/' + url_cap[i-1]
        title_fixed = title[i-1]
        fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
        plugintools.add_item(action="GetSerieLinks", title= title_fixed, url = url_cap_fixed, thumbnail = params.get("thumbnail") , extra = str(i) , info_labels = datamovie , page = show , plot = datamovie["Plot"] , fanart = fanart, folder = True, isPlayable = False)        
        i = i + 1
        
        
    
def GetSerieLinks(params):
    plugintools.log("Arena+ GetSerieLinks "+repr(params))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
    
    url_cap_fixed = params.get("url")
    title_fixed = params.get("title")
    data = plugintools.read(url_cap_fixed)
    #plugintools.log("data= "+data)
    
    # Thumbnail, sinopsis y fanart
    thumbnail = plugintools.find_single_match(data, 'src=\"/img/series/(.*?)"')
    thumbnail_fixed = 'http://seriesadicto.com/img/series/' + thumbnail
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    datamovie = {}
    datamovie["Plot"] = params.get("plot")

    matches = plugintools.find_multiple_matches(data, '<td class="enlacevideo"(.*?)/></td>')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        audio_url = plugintools.find_single_match(entry, '<img src="([^"]+)')
        if audio_url == "/img/1.png":
            audio_url = "[COLOR lightyellow][I][ESP][/I][/COLOR]"
        elif audio_url == "/img/2.png":
            audio_url = "[COLOR lightyellow][I][LAT][/I][/COLOR]"
        elif audio_url == "/img/3.png":
            audio_url = "[COLOR lightyellow][I][VOS][/I][/COLOR]"
        elif audio_url == "/img/4.png":
            audio_url = "[COLOR lightyellow][I][ENG][/I][/COLOR]"
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        #plugintools.log("page_url= "+page_url)
        if page_url.find("allmyvideos") >= 0:
            server_url = "[COLOR lightgreen][I][allmyvideos][/I][/COLOR]"
            plugintools.add_item(action="allmyvideos", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("vidspot") >= 0:
            server_url = "[COLOR lightgreen][I][vidspot][/I][/COLOR]"
            plugintools.add_item(action="vidspot", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("played.to") >= 0:
            server_url = "[COLOR lightgreen][I][played.to][/I][/COLOR]"
            plugintools.add_item(action="playedto", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("nowvideo") >= 0:
            server_url = "[COLOR lightgreen][I][nowvideo][/I][/COLOR]"
            plugintools.add_item(action="nowvideo", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)            
        elif page_url.find("streamin.to") >= 0:
            server_url = "[COLOR lightgreen][I][streamin.to][/I][/COLOR]"
            plugintools.add_item(action="streaminto", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("vk") >= 0:
            server_url = "[COLOR lightgreen][I][vk][/I][/COLOR]"
            plugintools.add_item(action="vk", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("tumi") >= 0:
            server_url = "[COLOR lightgreen][I][tumi][/I][/COLOR]"
            plugintools.add_item(action="tumi", title = title_fixed+' '+server_url+' '+audio_url ,url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)
        elif page_url.find("streamcloud") >= 0:
            server_url = "[COLOR lightgreen][I][streamcloud][/I][/COLOR]"
            plugintools.add_item(action="streamcloud", title = title_fixed+' '+server_url+' '+audio_url , url = page_url , thumbnail = thumbnail_fixed, info_labels = datamovie , fanart = fanart, folder = False, isPlayable = True)


    plugintools.modo_vista(show) 

        
        

def SelectTemp(params, temp):
    plugintools.log("[Arena+ 0.3.3].SelectTemp "+repr(params))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)    

    seasons = len(temp)
    
    dialog = xbmcgui.Dialog()
    
    if seasons == 1:
        selector = dialog.select('beta.1', [temp[0]])
                                             
    if seasons == 2:
        selector = dialog.select('beta.1', [temp[0], temp[1]])
                                             
    if seasons == 3:
        selector = dialog.select('beta.1', [temp[0],temp[1], temp[2]])
                                             
    if seasons == 4:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3]])
                                             
    if seasons == 5:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4]])
        
    if seasons == 6:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5]])
        
    if seasons == 7:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6]])
        
    if seasons == 8:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7]])
        
    if seasons == 9:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]])
        
    if seasons == 10:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9]])

    if seasons == 11:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10]])

    if seasons == 12:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11]])

    if seasons == 13:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12]])

    if seasons == 14:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13]])

    if seasons == 15:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14]])

    if seasons == 16:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]])

    if seasons == 17:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16]])

    if seasons == 18:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp[17]])

    if seasons == 19:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18]])

    if seasons == 20:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19]])

    if seasons == 21:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20]])

    if seasons == 22:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20], temp[21]])

    if seasons == 23:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20], temp[21], temp[22]])
        
    if seasons == 24:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20], temp[21], temp[22], temp[23]])
        
    if seasons == 25:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20], temp[21], temp[22], temp[23], temp[24]])

    if seasons == 26:
        selector = dialog.select('beta.1', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15], temp[16], temp [17], temp[18], temp[19], temp[20], temp[21], temp[22], temp[23], temp[24], temp[25]])
        

    i = 0
    while i<= seasons :
        if selector == i:
            params["season"] = temp[i]
            GetSerieChapters(params)

        i = i + 1
