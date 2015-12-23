# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Dailymotion
# Version 0.1 (10.12.2014)
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
import json
import math


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arena+/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arena+/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arena+/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arena+/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arena+/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'



def dailym_getplaylist(url):
    plugintools.log("beta.1.dailymotion_playlists "+url)
        
    # Fetch video list from Dailymotion playlist user
    data = plugintools.read(url)
    #plugintools.log("data= "+data)

    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,'{"(.*?)}')
        
    pattern = '{"(.*?)},{'
    for entry in matches:
        plugintools.log("entry="+entry)
        title = plugintools.find_single_match(entry,'name":"(.*?)"')
        title = title.replace("\u00e9" , "é")
        title = title.replace("\u00e8" , "è")
        title = title.replace("\u00ea" , "ê")
        title = title.replace("\u00e0" , "à")
        plugintools.log("title= "+title)
        id_playlist = plugintools.find_single_match(entry,'id":"(.*?)",')
        if id_playlist:
            plugintools.log("id_playlist= "+id_playlist)
            return id_playlist

        

def dailym_getvideo(url):
    plugintools.log("beta.1.dailymotion_videos "+url)

    # Fetch video list from Dailymotion feed
    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,'{"(.*?)}')

    pattern = '{"(.*?)},{'
    for entry in matches:
        plugintools.log("entry= "+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,'title":"(.*?)"')
        title = title.replace("\u00e9" , "é")
        title = title.replace("\u00e8" , "è")
        title = title.replace("\u00ea" , "ê")
        title = title.replace("\u00e0" , "à")
        video_id = plugintools.find_single_match(entry,'id":"(.*?)",')
        if video_id:
            plugintools.log("video_id= "+video_id)
            return video_id

def dailym_pl(params):
    plugintools.log("dailym_pl "+repr(params))

    pl = params.get("url")
    data = plugintools.read(pl)
    plugintools.log("playlist= "+data)

    dailym_vid = plugintools.find_multiple_matches(data, '{(.*?)}')
    
    for entry in dailym_vid:
        plugintools.log("entry= "+entry)
        title = plugintools.find_single_match(entry, '"title":"(.*?)",')
        title = title.replace('"', "")
        title = title.replace('\*', "")        
        video_id = plugintools.find_single_match(entry, '"id":"(.*?)",')
        thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
        if thumbnail == "":
            thumbnail = 'http://image-parcours.copainsdavant.com/image/750/1925508253/4094834.jpg'        
        url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
        print 'url',url
        plugintools.add_item(action="play", title=title, url=url, folder = False, fanart='http://image-parcours.copainsdavant.com/image/750/1925508253/4094834.jpg',thumbnail=thumbnail,isPlayable = True)
            
