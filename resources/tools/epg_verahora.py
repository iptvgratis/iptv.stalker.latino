# -*- coding: utf-8 -*-
#------------------------------------------------------------
# EPG ¿Qué ver ahora? para beta.1
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

import re,urllib,urllib2,sys
import plugintools,ioncube

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arenapremium/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arenapremium/art', ''))
temp = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.arenapremium/tmp', ''))
playlist = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.arenapremium/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def epg_verahora(params):
    plugintools.log('[%s %s].epg_verahora %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("extra")

    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    plugintools.add_item(action="", title= '[COLOR lightyellow][B]¿Qué ver ahora?[/B][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    body = plugintools.find_multiple_matches(data, '<td class="prga-i">(.*?)</tr>')
    for entry in body:
        channel = plugintools.find_single_match(entry, 'alt=\"([^"]+)')
        print 'channel',channel
        ahora = plugintools.find_single_match(entry, '<p>(.*?)</p>')
        print 'ahora',ahora
        hora_luego = plugintools.find_single_match(entry, 'class="fec1">(.*)</span>')
        hora_luego = hora_luego.split("</span>")
        hora_luego = hora_luego[0]
        print 'hora_luego',hora_luego
        diff_luego = plugintools.find_single_match(entry, 'class="fdiff">([^<]+)').strip()
        print 'diff_luego',diff_luego
        evento_luego = plugintools.find_single_match(entry, '<span class="tprg1">(.*?)</span>')
        print 'evento_luego',evento_luego
        evento_mastarde = plugintools.find_single_match(entry, '<span class="tprg2">(.*?)</span>')
        print 'evento_mastarde',evento_mastarde
        plugintools.add_item(action="", title= '[COLOR orange][B]'+channel+' [/B][COLOR lightyellow]'+ahora+'[/COLOR] [COLOR lightgreen][I]('+diff_luego+') [/I][/COLOR][COLOR white][B]'+hora_luego+' [/COLOR][/B] '+evento_luego, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
        #plugintools.log("entry= "+entry)


def epg_verluego(params):
    plugintools.log('[%s %s].epg_verluego %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("extra")

    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    plugintools.add_item(action="", title= '[COLOR lightyellow][B]¿Qué ver después?[/B][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    body = plugintools.find_multiple_matches(data, '<td class="prga-i">(.*?)</tr>')
    for entry in body:
        channel = plugintools.find_single_match(entry, 'alt=\"([^"]+)')
        hora_luego = plugintools.find_single_match(entry, 'class="fec1">(.*)</span>')
        hora_luego = hora_luego.split("</span>")
        hora_luego = hora_luego[0]
        print 'hora_luego',hora_luego
        diff_luego = plugintools.find_single_match(entry, 'class="fdiff">([^<]+)').strip()
        evento_luego = plugintools.find_single_match(entry, '<span class="tprg1">(.*?)</span>')
        evento_mastarde = plugintools.find_single_match(entry, '<span class="tprg2">(.*?)</span>')
        hora_mastarde = plugintools.find_single_match(entry, 'class="fec2">(.*)</span>')
        hora_mastarde = hora_mastarde.split("</span>")
        hora_mastarde = hora_mastarde[0]        
        plugintools.add_item(action="", title= '[COLOR orange][B]'+channel+' [/B][COLOR lightyellow][B]'+hora_luego+'[/B] '+evento_luego+'[/COLOR][COLOR lightgreen][I] ('+diff_luego+') [/I][/COLOR][COLOR white][B]'+hora_mastarde+' [/COLOR][/B]'+evento_mastarde, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
    

def epg_vermastarde(params):
    plugintools.log('[%s %s].epg_vermastarde %s' % (addonName, addonVersion, repr(params)))
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("extra")

    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    plugintools.add_item(action="", title= '[COLOR lightyellow][B]¿Qué ver más tarde?[/B][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    body = plugintools.find_multiple_matches(data, '<td class="prga-i">(.*?)</tr>')
    for entry in body:
        channel = plugintools.find_single_match(entry, 'alt=\"([^"]+)')
        evento_mastarde = plugintools.find_single_match(entry, '<span class="tprg2">(.*?)</span>')
        hora_mastarde = plugintools.find_single_match(entry, 'class="fec2">(.*)</span>')
        hora_mastarde = hora_mastarde.split("</span>")
        hora_mastarde = hora_mastarde[0]        
        plugintools.add_item(action="", title= '[COLOR orange][B]'+channel+' [/B][COLOR lightyellow][B]'+hora_mastarde + '[/B] '+evento_mastarde+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
    

# Petición de la URL
def gethttp_headers(params):
    plugintools.log('[%s %s].gethttp_headers %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",'http://www.digitele.com/pluginfiles/canales/'])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body                    

    
        
        
    
    
