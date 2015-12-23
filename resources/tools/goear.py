# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Arena+ Parser de Goear
# Version 0.1 (27.01.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools


thumbnail = 'http://cdn5.applesencia.com/wp-content/blogs.dir/17/files/2012/02/Goear-Logo.png'
fanart = 'http://www.bestfreejpg.com/wp-content/uploads/2014/07/best-music-wallpaper-c.jpg'
referer = 'http://www.seriesflv.com/'

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
FANART = "fanart"
OTHER = "other"
MUSIC = "music"


def goear(params):
    plugintools.log("Arena+ Goear: ")
    
    url = params.get("url")
    show = params.get("extra")
    
    if show == "":
        show = params.get("show")
        if show == "":
            show = params.get_setting("music_id")
            modo_vista(show)
            plugintools.log("show= "+show)            
    elif show == "LIST":
        show = plugintools.get_setting("music_id")

    modo_vista(show)
    plugintools.log("show= "+show)

    goear_def(params.get("url"))



def goear_def(url):
    plugintools.log("[Arena+ 0.3.0].goear")

    params = plugintools.get_params()
    show = params.get("extra")    
    
    if show == "":
        show = params.get("show")
        if show == "":
            show = params.get_setting("music_id")
            modo_vista(show)
            plugintools.log("show= "+show)            
    elif show == "LIST":
        show = plugintools.get_setting("music_id")

    modo_vista(show)
    plugintools.log("show= "+show)
        
    thumbnail = params.get("thumbnail")
    title = params.get("title")
    plugintools.add_item(action="", title='[COLOR royalblue][B]'+title+'[/B][/COLOR]', url=url, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)

    if url.startswith("goear_sg") == True:
        id_playlist = url.replace("goear_sg:", "").replace('"',"").strip()
        url = 'http://www.goear.com/action/sound/get/'+id_playlist
        plugintools.log("url= "+url)
        plugintools.play_resolved_url(url)
    elif url.startswith("goear_pl") == True:
        id_playlist = url.replace("goear_pl:", "").replace('"',"").strip()
        url = 'http://www.goear.com/apps/android/playlist_songs_json.php?v='+id_playlist
        plugintools.log("url= "+url)
        referer = 'http://www.goear.com/'
        data = gethttp_referer_headers(url,referer,show)
        #plugintools.log("data= "+data)
        modo_vista(show)

        songs = plugintools.find_multiple_matches(data, '{(.*?)}')
        i = 1
        for entry in songs:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play", title='[COLOR lightyellow]'+str(i)+' '+title_song+'[/COLOR][COLOR orange] ('+songtime+')[/COLOR]', url=url, thumbnail = thumbnail , extra = show , fanart = fanart , folder = False, isPlayable = True)
            i = i + 1
       

def gethttp_referer_headers(url,referer,show):
    plugintools.log("beta.1-0.3.0.gethttp_referer_headers ")
    modo_vista(show)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body


def modo_vista(show):
    if show == "":
        plugintools.get_setting("music_id")
        
    if show == "0":
        show = "movies"
    elif show == "1":
        show = "thumbnail"
    elif show == "2":
        show = "list"
    elif show == "3":
        show = "fanart"
    elif show == "4":
        show = "seasons"
    elif show == "5":
        show = "episodes"
    elif show == "6":
        show = "tvshows"

    if show == "music":
        plugintools.set_view(TV_SHOWS)
    if show == "series":
        plugintools.set_view(EPISODES)
    if show == "tvshows":
        plugintools.set_view(TV_SHOWS)
    if show == "thumbnail":
        plugintools.set_view(THUMBNAIL)
    elif show == "movies":
        plugintools.set_view(MOVIES)
    elif show == "list":
        plugintools.set_view(LIST)
    elif show == "seasons":
        plugintools.set_view(SEASONS)
    elif show == "episodes":
        plugintools.set_view(EPISODES)
    elif show == "tvshows":
        plugintools.set_view(TV_SHOWS)
    else:
        plugintools.set_view(LIST)

    plugintools.log("Modo de vista fijado en Música: "+show)

