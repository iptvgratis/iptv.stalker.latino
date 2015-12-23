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




def seriesblanco0(params):
    plugintools.log("[beta.1-0.3.0].seriesblanco "+repr(params))

    show = params.get("page")
    if show == "tvshows":
        plugintools.modo_vista(show)
    else:
        show = plugintools.get_setting("series_id")
        plugintools.modo_vista(show)

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    thumbnail = params.get("thumbnail")
    if thumbnail == "":
        thumbnail = "http://seriesblanco.com/imags_estilos/logoblanconavidad2.png"
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    
    url = params.get("url")    
    referer = url
    data = gethttp_referer_headers(url,referer,show)
    #plugintools.log("data= "+data)

    seasons = plugintools.find_multiple_matches(data, "<h2 style='cursor: hand; cursor: pointer;'><u>(.*?)</table>")
    for entry in seasons:
        #plugintools.log("entry= "+entry)
        title_temp = plugintools.find_single_match(entry, "(.*?)</u></h2>")
        chapter = plugintools.find_multiple_matches(entry, '<tr><td>(.*?)</td>')
        for entri in chapter:
            #plugintools.log("entri= "+entri)
            url_chapter = plugintools.find_single_match(entri, "<a href='([^']+)")
            url_chapter = 'http://www.seriesblanco.com'+url_chapter
            title_chapter = plugintools.find_single_match(entri, "'>(.*?)</a>")
            plugintools.log("title_chapter="+title_chapter)
            plugintools.log("url_chapter="+url_chapter)
            if title_chapter.find("x00") < 0:
                plugintools.add_item(action="seriesblanco1", title=title_chapter, url=url_chapter, thumbnail = thumbnail , info_labels = datamovie , extra = show , page = show , plot = sinopsis , fanart = fanart, folder = True, isPlayable = False)

    plugintools.modo_vista(show)    

    

def seriesblanco1(params):
    plugintools.log("[beta.1-0.3.0] SeriesBlanco1 "+repr(params))

    show = params.get("page").strip()       
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    thumbnail = params.get("thumbnail")
    if thumbnail == "":
        thumbnail = "http://seriesblanco.com/imags_estilos/logoblanconavidad2.png"
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"        
    
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer,show)
    plugintools.modo_vista(show)
    #plugintools.log("data= "+data)
    match_listacapis = plugintools.find_single_match(data, "<form method='post' name=validacion action=''><table class='zebra'><caption class='tam16'>Visionados online</caption>(.*?)<div id='backlinks-container'>")
    #plugintools.log("match_listacapis= "+match_listacapis)
    match_capi = plugintools.find_multiple_matches(match_listacapis, "<td class='tam12'(.*?)</td></tr>")
    for entry in match_capi:
        #plugintools.log("entry= "+entry)
        url_capi = plugintools.find_single_match(entry, "<a href='([^']+)")
        url_capi = 'http://www.seriesblanco.com'+url_capi
        #plugintools.log("url_capi= "+url_capi)
        lang_audio = plugintools.find_single_match(entry, "<img src='/banderas/([^']+)")
        if lang_audio.find("es.png") >= 0:
            lang_audio = "ESP"
        elif lang_audio.find("la.png") >= 0:
            lang_audio = "LAT"
        elif lang_audio.find("vos.png") >= 0:
            lang_audio = "V.O.S."
        elif lang_audio.find("vo.png") >= 0:
            lang_audio = "V.O."            
        #plugintools.log("lang_audio= "+lang_audio)
        url_server = plugintools.find_single_match(entry, "<img src='/servidores/([^']+)")
        url_server = url_server.replace(".png", "").replace(".jpg", "")
        quality_url = plugintools.find_single_match(entry, "<td class='tam12'>(.*?)</td></tr>")
        if quality_url == "":
            quality_url = "undefined"
        #plugintools.log("quality_url= "+quality_url)
        if url_server.find("allmyvideos") >=0:
            url_server = "allmyvideos"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("vidspot") >= 0:
            url_server = "vidspot"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("played.to") >= 0:
            url_server = "played.to"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("streamin.to") >= 0:
            url_server = "streamin.to"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("streamcloud") >= 0:
            url_server = "streamcloud"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("nowvideo") >= 0:
            url_server = "nowvideo"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("veehd") >= 0:
            url_server = "veehd"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("vk") >= 0:
            url_server = "vk"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("tumi") >= 0:
            url_server = "tumi"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("novamov") >= 0:
            url_server = "novamov"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("moevideos") >= 0:
            url_server = "moevideos"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("gamovideo") >= 0:
            url_server = "gamovideo"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("movshare") >= 0:
            url_server = "movshare"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("powvideo") >= 0:
            url_server = "powvideo"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("mail.ru") >= 0:
            url_server = "mailru"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("netu") >= 0:
            url_server = "netu"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        elif url_server.find("movshare") >= 0:
            url_server = "movshare"
            plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR lightgreen][I] ['+lang_audio+'] [/I][/COLOR]'+'[COLOR lightyellow][I] ['+url_server+'][/I][/COLOR]', url = url_capi, plot = sinopsis, info_labels = datamovie , page = show , thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        
        plugintools.modo_vista(show)

            

def seriesblanco2(params):
    plugintools.log("[beta.1-0.3.0].seriesblanco "+repr(params))

    show = params.get("page")
    plugintools.modo_vista(show)    
    plugintools.log("show= "+show)
    
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer,show)
    plugintools.modo_vista(show)
    #plugintools.log("data= "+data)    
    # onclick='window.open("http://allmyvideos.net/lh18cer7ut8r")
    url_final = plugintools.find_single_match(data, "onclick='window.open(.*?);'/>")
    url_final = url_final.replace('("', "").replace('")', "")
    #plugintools.log("url_final= "+url_final)
    params = plugintools.get_params()
    params["url"]=url_final
    getlink_seriesblanco(params)



def getlink_seriesblanco(params):
    plugintools.log("GetLink for SeriesBlanco.com "+repr(params))

    show = params.get("page")
    plugintools.modo_vista(show)   
    
    url_final = params.get("url")
    
    if url_final.find("allmyvideos") >= 0:
        params["url"]=url_final
        allmyvideos(params)
    elif url_final.find("vidspot") >= 0:
        params["url"]=url_final
        vidspot(params)
    elif url_final.find("played.to") >= 0:
        params["url"]=url_final
        playedto(params)        
    elif url_final.find("streamin.to") >= 0:
        params["url"]=url_final
        streaminto(params)
    elif url_final.find("streamcloud") >= 0:
        params["url"]=url_final
        streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0:
        params["url"]=url_final
        nowvideo(params)
    elif url_final.find("vk") >= 0:
        params["url"]=url_final
        vk(params)        
    elif url_final.find("veehd") >= 0:
        params["url"]=url_final
        veehd(params)
    if url_final.find("videobam") >= 0:
        params["url"]=url_final
        videobam(params)
    elif url_final.find("novamov") >= 0:
        params["url"]=url_final
        novamov(params)
    elif url_final.find("moevideos") >= 0:
        params["url"]=url_final
        moevideos(params)
    elif url_final.find("gamovideo") >= 0:
        params["url"]=url_final
        gamovideo(params)
    elif url_final.find("powvideo") >= 0:
        params["url"]=url_final
        powvideo(params)
    elif url_final.find("mail.ru") >= 0:
        params["url"]=url_final
        mailru(params)
    elif url_final.find("netu") >= 0:
        params["url"]=url_final
        netu(params)
    elif url_final.find("tumi.tv") >= 0:
        params["url"]=url_final
        tumi(params)         
        

    plugintools.modo_vista(show)        
       

def gethttp_referer_headers(url,referer,show):
    plugintools.log("beta.1-0.3.0.gethttp_referer_headers ")

    plugintools.log("show= "+show)
    plugintools.modo_vista(show) 
        
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.modo_vista(show)
    return body
