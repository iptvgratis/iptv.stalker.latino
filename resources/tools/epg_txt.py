# -*- coding: utf-8 -*-
#------------------------------------------------------------
# EPG-TXT para beta.1
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

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
FANART = "fanart"
OTHER = "other"
MUSIC = "music"

from __main__ import *
from resources.tools.txt_reader import *


def epg_txt0(params):
    plugintools.log('[%s %s] Cargando EPG-TXT ... %s' % (addonName, addonVersion, params.get("url")))
	
    # Creamos diccionario con las URLs de la programación TV
    channel = params.get("title").replace(" [EPG-TXT]", "").strip()
    channel = channel.replace("Opción 1", "").replace("HD", "").replace("720p", "").replace("1080p", "").replace("SD", "").replace("HQ", "").replace("LQ", "").strip()
    channel = channel.replace("Opción 2", "").replace("Opción 3", "").replace("Op. 1", "").replace("Op. 2", "").replace("Op. 3", "")
    plugintools.log("Cargando programación TV de "+channel)	
	
    # Consultamos diccionario de URLs de programación TV ...
    url = params.get("url")
                    
    # Creamos y abrimos archivo EPG-TXT ...
    fname = url.replace("http://servicios.elpais.com/m/programacion-tv/canal/", "").replace("/", "")
    fname_txt = fname+'.txt'  # Nombre de archivo	
    fname_txt = playlists + fname_txt  # Ruta del EPG-TXT
    fepg_txt = open(fname_txt, "wb")
    
    # Parseamos web con la programación TV ...
    data = plugintools.read(url)
    
    # Cabecera con la fecha de hoy, mañana y pasado
    bloque_head = plugintools.find_single_match(data, '<div id="hoy"(.*?)<div class="cont-rejilla">')
    bloque_events = plugintools.find_single_match(data, '<div id="hoy"(.*?)</tbody>')
    #plugintools.log("bloque_events= "+bloque_events)
    epg_txt2(url, fepg_txt, bloque_head, bloque_events)  # Parseo y escritura en EPG-TXT ...
    fepg_txt.write('\n\n')
            
    bloque_head = plugintools.find_single_match(data, '<div id="manana" class="ocultar_manana">(.*?)<div class="cont-rejilla">')
    bloque_events = plugintools.find_single_match(data, '<div id="manana" class="ocultar_manana">(.*?)</tbody>')
    #plugintools.log("bloque_events= "+bloque_events)
    epg_txt2(url, fepg_txt, bloque_head, bloque_events)
    fepg_txt.write('\n\n')
            
    bloque_head = plugintools.find_single_match(data, '<div id="pasado" class="ocultar_pasado">(.*?)<div class="cont-rejilla">')
    bloque_events = plugintools.find_single_match(data, '<div id="pasado" class="ocultar_pasado">(.*?)</tbody>')
    #plugintools.log("bloque_events= "+bloque_events)
    epg_txt2(url, fepg_txt, bloque_head, bloque_events)
    
    fepg_txt.close()
    url = 'txt:'+fname_txt
    plugintools.log("URL= "+url)

    params["url"] = url    
    txt_reader(params)
		
	
	

	
def epg_txt2(url, fepg_txt, bloque_head, bloque_events):  # Parseo y escritura de programación en EPG-TXT ...
    plugintools.log('[%s %s] Creando EPG-TXT ... %s' % (addonName, addonVersion, fepg_txt))

    # Parseamos web con la programación TV ...
    data = plugintools.read(url)    

    # Escribimos cabecera ...
    head = plugintools.find_single_match(bloque_head, '<h3>(.*?)</h3>');head=head.replace("<strong>", "[B]").replace("</strong>", "[/B]").strip()
    fepg_txt.write('[COLOR orange]'+head+'[/COLOR]\n\n')	

    # Parseamos eventos y escribimos en EPG-TXT ...
    events_dia = plugintools.find_multiple_matches(bloque_events, '<tr>(.*?)</tr>')
    for entry in events_dia:
        #plugintools.log("entry= "+entry)
        event_time = plugintools.find_single_match(entry, '<td class="hora"><strong>(.*?)</strong>')
        event_cat = plugintools.find_single_match(entry, '<li>(.*?)</li>')
        event_length = plugintools.find_single_match(entry, 'Duración:<strong> (.*?)</strong>')
        event_title = plugintools.find_single_match(entry, '<h4>(.*?)</h4>');event_title=event_title.strip()
        event_masinfo = plugintools.find_single_match(entry, '<p> (.*?)</p>')
        #plugintools.log("event_time= "+event_time)
        #plugintools.log("event_cat= "+event_cat)
        #plugintools.log("event_length= "+event_length)
        #plugintools.log("event_title= "+event_title)
        #plugintools.log("event_masinfo= "+event_masinfo)
        
        # Escribimos datos en EPG-TXT ...
        if event_time != "":  # Controlamos que sea un evento programado
            linea_1 = '[B][COLOR lightyellow]'+event_time+'[/COLOR][/B]' + ' [COLOR gold][B]' + event_title + '[/B][/COLOR][I] ('+event_length+')[/I]'
            fepg_txt.write(linea_1)
            if event_masinfo == "":
                pass
            else:
                linea_3 = '\n[I][COLOR lightyellow]'+event_cat+': '+event_masinfo+'[/COLOR][/I]'
                fepg_txt.write(linea_3)
            
	fepg_txt.write('\n')  # Saltos de línea para fin de programación del día
		

	
def epg_txt_dict(channel):
    plugintools.log('[%s %s] Abriendo URL para EPG-TXT: %s' % (addonName, addonVersion, channel))

    channel = parser_title(channel)
    plugintools.log("channel= "+channel)
    
    channel = channel.lower()
    if channel == "la 1" or channel == "la 1 hd" or channel == "tve-1" or channel == "tve-1 hd":  # Generalistas
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tve-1/'		
    elif channel == "la 2":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/la-2/'		
    elif channel == "antena 3" or channel == "antena 3 hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/antena-3/'
    elif channel == "cuatro" or channel == "cuatro hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cuatro/'
    elif channel == "telecinco hd" or channel == "telecinco":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/telecinco/'
    elif channel == "la sexta" or channel == "la sexta hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/la-sexta/'
    elif channel == "aragon tv" or channel == "aragon tv hd":  # Autonómicas
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/aragon-television/'
    elif channel == "canal33" or channel == "canal 33":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-33/'
    elif channel == "canal extremadura":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-extremadura/'
    elif channel == "canal sur":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-sur/'
    elif channel == "canal sur":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-sur-andalucia/'
    elif channel == "castilla la mancha tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/castilla-la-mancha-tv/'
    elif channel == "etb1":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/etb1/'
    elif channel == "etb2":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/etb2/'	
    elif channel == "ib3 televisio" or channel == "ib3 televisió":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/ib3-televisio/'	
    elif channel == "radiotelevisión de murcia":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/radiotelevision-de-murcia/'
    elif channel == "rtpa" or channel == "tvp asturias":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tv-p.-asturias/'	
    elif channel == "tv3":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tv3/'	
    elif channel == "telemadrid":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/telemadrid/'	
    elif channel == "televisión canaria":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/television-canaria/'
    elif channel == "televisión de galicia" or channel == "tvg":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/television-de-galicia/'	
    elif channel == "13 tv":  # TDT Generalistas
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/13-tv/'	
    elif channel == "24 horas" or channel == "24h":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/24-horas/'
    elif channel == "40 tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/40-tv/'	
    elif channel == "a&e":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/a&e/'
    elif channel == "axn" or channel == "axn hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/axn/'
    elif channel == "axn white" or channel == "axn white hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/axn-white/'
    elif channel == "al jazeera english":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/al-jazeera-english/'	
    elif channel == "bbc world":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/bbc-world/'
    elif channel == "baby tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/baby-tv/'	
    elif channel == "barça tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/barca-tv/'
    elif channel == "bloomberg":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/bloomberg/'	
    elif channel == "boing":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/boing/' 
    elif channel == "c+ 1" or channel == "canal+ 1" or channel == "canal+ 1 hd":  # Canal+
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-1/'
    elif channel == "c+ 1 ...30":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-1-...30/'
    elif channel == "c+ 2" or channel == "canal+ 2" or channel == "canal+ 2 hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-2/'
    elif channel == "c+ 3d" or channel == "canal+ 3d":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-3d/'
    elif channel == "c+ acción" or channel == "canal+ acción":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-accion/'	
    elif channel == "c+ comedia" or channel == "canal+ comedia":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-comedia/'
    elif channel == "c+ dcine" or channel == "canal+ dcine":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-dcine/'	
    elif channel == "c+ deportes" or channel == "canal+ deportes":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-deportes/' 
    elif channel == "c+ deportes 2" or channel == "canal+ deportes 2":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-deportes-2/'
    elif channel == "c+ fútbol" or channel == "canal+ fútbol" or channel == "canal+ futbol":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-futbol/'
    elif channel == "c+ golf" or channel == "canal+ golf":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-golf/'	
    elif channel == "c+ liga" or channel == "canal+ liga":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-liga/'	
    elif channel == "c+ liga multi" or channel == "canal+ liga multi":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-liga-multi/'
    elif channel == "c+ liga de campeones" or channel == "canal+ liga de campeones":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-liga-de-campeones/'	
    elif channel == "c+ series" or channel == "canal+ series":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-series/'	
    elif channel == "c+ toros" or channel == "canal+ toros":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-toros/'
    elif channel == "c+ xtra" or channel == "canal+ xtra":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cplus-xtra/'
    elif channel == "cnbc":  # Otros
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cnbc/'	
    elif channel == "cnn internacional" or channel == "cnn":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cnn-int/'	
    elif channel == "cosmo" or channel == "cosmo hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cosmo/'
    elif channel == "calle 13" or channel == "calle 13 hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/calle-13/'
    elif channel == "canal cocina":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-cocina/'	
    elif channel == "canal decasa":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-decasa/'	
    elif channel == "canal panda":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-panda/'
    elif channel == "canal de las estrellas":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/canal-de-las-estrellas/'
    elif channel == "caza y pesca":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/caza-y-pesca/'	
    elif channel == "clan tve":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/clan-tve/'	
    elif channel == "comedy central":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/comedy-central/'
    elif channel == "cubavision" or channel == "cubavision":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/cubavision/'
    elif channel == "dcine español":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/dcine-espanol/'	
    elif channel == "discovery max":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/discovery-max/'	
    elif channel == "disney channel":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/disney-channel/'
    elif channel == "disney junior":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/disney-junior/'
    elif channel == "disney xd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/disney-xd/'	
    elif channel == "divinity":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/divinity/'	
    elif channel == "energy":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/energy/'
    elif channel == "euronews":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/euronews/'
    elif channel == "fdf" or channel == "factoría de ficción":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/factoria-de-ficcion/'	
    elif channel == "fashiontv" or channel == "fashion tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/fashiontv/'	
    elif channel == "fox" or channel == "fox hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/fox/'
    elif channel == "fox life":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/fox-life/'
    elif channel == "fox news":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/fox-news/'	
    elif channel == "garage tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/garage-tv/'	
    elif channel == "goltv" or channel == "gol t" or channel == "gol tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/goltv/'
    elif channel == "historia":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/historia/'
    elif channel == "hollywood" or channel == "hollywood channel":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/hollywood/'	
    elif channel == "intereconomia" or channel == "intereconomia tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/intereconomia/'	
    elif channel == "la tienda en casa":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/la-tienda-en-casa/'
    elif channel == "mtv españa":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/mtv-espana/'
    elif channel == "mtv rocks":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/mtv-rocks/'	
    elif channel == "mezzo":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/mezzo/'	
    elif channel == "mezzo live hd" or channel == "mezzo live":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/mezzo-live-hd/'
    elif channel == "nick jr":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/nick-jr/'
    elif channel == "nat geo wild":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/nat-geo-wild/'	
    elif channel == "nat geographic" or channel == "national geographic":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/nat-geographic/'	
    elif channel == "neox":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/neox/'
    elif channel == "nickelodeon":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/nickelodeon/'
    elif channel == "nova":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/nova/'
    elif channel == "odisea" or channel == "odisea hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/odisea/'	
    elif channel == "paramount channel":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/paramount-channel/'	
    elif channel == "playboy tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/playboy-tv/'
    elif channel == "rt":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/rt/'
    elif channel == "real madrid tv":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/real-madrid-tv/'	
    elif channel == "syfy":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/syfy/'	
    elif channel == "Sol Música":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/sol-musica/'
    elif channel == "sportmania" or channel == "sportmania hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/sportmania/'
    elif channel == "super 3" or channel == "super3" or channel == "super 3 hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/super-3/'
    elif channel == "tcm" or channel == "tcm hd":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tcm/'	
    elif channel == "tnt":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tnt/'	
    elif channel == "tv record":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tv-record/'
    elif channel == "tv5monde":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/tv5monde/'
    elif channel == "teledeporte":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/teledeporte/'	
    elif channel == "telesur":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/telesur/'	
    elif channel == "vh1":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/vh1/'
    elif channel == "viajar":
        url = 'http://servicios.elpais.com/m/programacion-tv/canal/viajar/'     
		
    return url
	


# Petición de la URL
def gethttp_headers(params):
    plugintools.log('[%s %s].gethttp_headers %s' % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",'http://www.digitele.com/pluginfiles/canales/'])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    #plugintools.log("body= "+body)
    return body                    

    
        
        
    
    
