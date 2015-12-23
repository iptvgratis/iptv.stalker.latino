# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 EPG de Mundoplus.tv
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


def epg_mundoplus(title):
    plugintools.log('[%s %s].epg_ftv %s' % (addonName, addonVersion, title))
    channel = title.lower()
    channel = channel.replace("Opción 1", "").replace("HD", "").replace("720p", "").replace("1080p", "").replace("SD", "").replace("HQ", "").replace("LQ", "").strip()
    channel = channel.replace("Opción 2", "")
    channel = channel.replace("Opción 3", "")
    channel = channel.replace("Op. 1", "")
    channel = channel.replace("Op. 2", "")
    channel = channel.replace("Op. 3", "")
    plugintools.log("Canal: "+channel)
    params = plugintools.get_params()
    
    if channel == "la 1" or channel == "la 1 hd":
        channel = "tve1"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "la 2":
        channel = "tve2"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "24 horas" or channel == "24h":
        channel = "24h"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "clan tve" or channel == "clan":
        channel = "clantve"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "antena 3":
        channel = "a3"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "la sexta" or channel == "la sexta hd":
        channel = "sexta"
        epg_channel = epg_formulatv(params, channel)    
    elif channel == "telecinco hd" or channel == "telecinco":
        channel == "telecinco"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "nova":
        channel = "nova"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "neox":
        channel = "neox"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "mega":
        channel = "mega"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "golt" or channel == "gol television":
        channel = "gol"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "cuatro" or channel == "cuatro hd":
        channel = "cuatro"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "telecinco":
        channel = "t5"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "fdf":
        channel = "fdft5"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "divinity":
        channel = "divinity"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "energy":
        channel = "energy"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "boing":
        channel = "boing"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "discovery max":
        channel = "dmax"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "13tv":
        channel = "13tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "paramount channel":
        channel = "paramount"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "discovery max":
        channel = "dmax"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel      
    

        return epg_channel        
    elif channel == "canal+1" or channel == "canal+ 1" or channel == "canal plus" or channel == "canal+ hd":
        channel = "canal+1"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "canal+2" or channel == "canal+ 2" or channel == "canal plus 2" or channel == "canal+ 2 hd":
        channel = "canal+ 2"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel
    elif channel == "canal+ 1 ...30" or channel == "canal+ 1... 30":
        channel = "canal+ 1 ...30"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel    
    elif channel == "canal+ series":
        channel = "canal+ series"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel      
    elif channel == "goltv" or channel == "golt":
        channel = "gol televisión"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "40 TV":
        channel = "40 tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal sur" or channel == "andalucia tv":
        channel = "canal sur"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "axn white":
        channel = "axn white"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel
    elif channel == "xtrm":
        channel = "xtrm"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel     
    elif channel == "bio":
        channel = "bio"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "calle 13" or channel == "calle 13 hd":
        channel = "calle 13"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "amc" or channel == "amc españa":
        channel = "amc (españa)"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel     
    elif channel == "canal barça" or channel == "canal barca":
        channel = "barça tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "andalucía tv" or channel == "andalucia tv":
        channel = "andalucia-tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "bio":
        channel = "bio"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal barça" or channel == "canal barca":
        channel = "canal barca"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ 30" or channel == "canal+ ...30" or channel == "canal plus 30":
        channel = "canal+ 1... 30"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ accion" or channel == "canal+ acción" or channel=="canal plus accion":
        channel = "canal+ acción"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ comedia" or channel == "canal plus comedia":
        channel = "canal+ comedia"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ decine" or channel == "canal plus decine":
        channel = "canal+ dcine"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ deporte" or channel == "canal plus deporte":
        channel = "canal+ deporte"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ futbol" or channel == "canal+ fútbol" or channel == "canal plus fútbol" or channel == "canal plus futbol":
        channel = "canal+ fútbol"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "canal+ liga":
        channel = "canal+ liga"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel    
    elif channel == "canal+ golf" or channel == "canal plus golf":
        channel = "golf+"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ toros" or channel == "canal plus toros":
        channel = "canal+ toros"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal+ extra" or channel=="canal+ xtra":
        channel = "canal+ xtra"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal 33" or channel == "canal33":
        channel = "canal33"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "canal cocina":
        channel = "canal cocina"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "cartoon network" or channel == "cartoon network hd":
        channel = "cartoon network"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "castilla-la mancha televisión" or channel == "castilla-la mancha tv":
        channel = "castilla-la-mancha"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "caza y pesca":
        channel = "caza-y-pesca"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "clan" or channel == "clan tve 50" or channel == "clan tve":
        channel = "clan tve"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "nickelodeon":
        channel = "nickelodeon"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel    
    elif channel == "boing":
        channel = "boing"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel     
    elif channel == "cnbc":
        channel = "cnbc"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "cnn-international" or channel == "cnn int":
        channel = "cnn international"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv":
        channel = "cosmopolitan"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "a&e" or channel == "a&e españa":
        channel = "a&e españa"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel      
    elif channel == "canal+ dcine" or channel == "canal plus dcine":
        channel = "dcine espanol"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "decasa":
        channel = "decasa"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "discovery channel":
        channel = "discovery channel"
        epg_channel = epg_formulatv(params, channel)
    elif channel == "national geographic":
        channel = "national geographic"
        epg_channel = epg_formulatv(params, channel)        
        return epg_channel        
    elif channel == "discovery max":
        channel = "discovery max"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "disney channel":
        channel = "disney channel"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "disney-cinemagic":
        channel = "disney cinemagic"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "disney xd":
        channel = "disney xd"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "disney junior" or channel == "disney jr":
        channel = "disney junior"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel     
    elif channel == "divinity":
        channel = "divinity"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "energy":
        channel = "energy"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "etb1" or channel == "etb 1":
        channel = "euskal telebista 1"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "etb 2" or channel == "etb2":
        channel = "euskal telebista 1"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "factoría de ficción" or channel == "factoria de ficcion" or channel == "fdf":
        channel = "fdf"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "buzz":
        channel = "buzz"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel    
    elif channel == "fox" or channel == "fox hd":
        channel = "fox españa"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "fox life":
        channel = "fox life"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "fox news":
        channel = "fox news"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "historia" or channel == "historia hd":
        channel = "canal de historia"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "natura" or channel == "canal natura":
        channel = "canal natura"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel     
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv":
        channel = "cosmopolitan"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "hollywood" or channel == "hollywood channel":
        channel = "canal hollywood"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "ib3 televisio" or channel == "ib3 televisió":
        channel = "ib3 televisio"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "intereconomia" or channel == "intereconomía" or channel == "intereconomía tv":
        channel = "intereconomia"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "mtv" or channel == "mtv españa" or channel == "mtv espana":
        channel = "mtv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "nat geo wild":
        channel = "nat geo wild"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
           
    elif channel == "nick jr." or channel == "nick jr":
        channel = "nick jr."
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "odisea" or channel == "odisea hd":
        channel = "odisea"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    
    elif channel == "panda":
        channel = "panda"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "paramount channel":
        channel = "paramount channel"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "playboy tv":
        channel = "playboy tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "playhouse disney":
        channel = "playhouse disney"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "rtv murcia 7" or channel == "radiotelevisión de murcia" or channel == "rtv murcia":
        channel = "7 región de murcia"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "real madrid tv":
        channel = "real madrid tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "syfy" or channel== "syfy españa":
        channel = "syfy españa"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "sony entertainment":
        channel = "sony entertainment"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "sportmania" or channel == "sportmania hd":
        channel = "sportmania"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "tcm":
        channel = "tcm"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "teledeporte" or channel == "intereconomía" or channel == "intereconomía tv":
        channel = "teledeporte"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "telemadrid" or channel == "telemadrid hd":
        channel = "telemadrid"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "televisión canaria" or channel == "televisión canaria":
        channel = "television canaria"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel         
    elif channel == "televisión de galicia" or channel == "television de galicia" or channel == "tvg":
        channel = "tvg"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "tnt" or channel == "tnt hd":
        channel = "tnt españa"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "tv3" or channel == "tv3 hd":
        channel = "tv3"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel        
    elif channel == "vh1":
        channel = "vh1"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "viajar":
        channel = "canal viajar"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "baby tv":
        channel = "baby tv"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel
    elif channel == "canal panda":
        channel = "canal panda"
        epg_channel = epg_formulatv(params, channel)
        return epg_channel     
    elif channel == "arenasports 1":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-1')
        return epg_channel
    elif channel == "arenasports 2":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-2')
        return epg_channel
    elif channel == "arenasports 3":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-3')
        return epg_channel
    elif channel == "arenasports 4":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-4')
        return epg_channel
    elif channel == "arenasports 5":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-arena-sport-5')
        return epg_channel
    elif channel == "sportklub 1" or channel == "sport klub 1":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-sport-klub-1')
        return epg_channel
    elif channel == "sportklub 2" or channel == "sport klub 2":
        from resources.tools.epg_arenasport import *
        epg_channel = epg_arena('http://tv.aladin.info/tv-program-sport-klub-2')
        return epg_channel      
    else:
        return False


def epg_mundoplus(params, channel):
    plugintools.log('[%s %s].epg_formulatv %s' % (addonName, addonVersion, repr(params)))
    url='http://www.mundoplus.tv/zonatdt/parrillatdt/index.php?amb=NAC&secc='+ch+'&fecha='+hoy+'&perso=0'
    thumbnail = params.get("thumbnail")
    fanart = params.get("extra")
    canal_buscado = channel
    canal_buscado= canal_buscado.replace(" hd", "")
    epg_channel = []
    params["plot"]=""

    backup_ftv = tmp + 'backup_ftv.txt'    
    if os.path.exists(backup_ftv):
        pass
    else:
        backup_epg = open(backup_ftv, "a")
        data = plugintools.read(params.get("url"))
        backup_epg.write(data)        
        backup_epg.close()

    # Abrimos backup
    backup_epg = open(backup_ftv, "r")
    data = backup_epg.read()
    #plugintools.log("data= "+data)

    # Calculando hora actual
    ahora = datetime.now()
    minutejo = str(ahora.minute)
    
    if ahora.minute < 10:  # Añadimos un cero delante del minuto actual por si es inferior a la decena
        minuto_ahora = '0'+str(ahora.minute)
    else:
        minuto_ahora = str(ahora.minute)
       
    hora_ahora = str(ahora.hour)+":"+minuto_ahora
    epg_channel.append(hora_ahora)   # index 0              
            
    # Vamos a leer la fuente de datos
    body = plugintools.find_multiple_matches(data, '<td class="prga-i">(.*?)</tr>')    
    for entry in body:
        channel = plugintools.find_single_match(entry, 'alt=\"([^"]+)')
        channel = channel.lower()
        plugintools.log("Buscando canal: "+canal_buscado)
        plugintools.log("Channel: "+channel)
        if channel == canal_buscado:
            print 'channel',channel
            evento_ahora = plugintools.find_single_match(entry, '<p>(.*?)</p>')
            epg_channel.append(evento_ahora)   # index 1            
            hora_luego = plugintools.find_single_match(entry, 'class="fec1">(.*)</span>')
            hora_luego = hora_luego.split("</span>")
            hora_luego = hora_luego[0]
            #print 'hora_luego',hora_luego
            epg_channel.append(hora_luego)   # index 2
            diff_luego = plugintools.find_single_match(entry, 'class="fdiff">([^<]+)').strip()
            #print 'diff_luego',diff_luego
            epg_channel.append(diff_luego)   # index 3 
            evento_luego = plugintools.find_single_match(entry, '<span class="tprg1">(.*?)</span>')
            #print 'evento_luego',evento_luego
            epg_channel.append(evento_luego)   # index 4 
            hora_mastarde = plugintools.find_single_match(entry, 'class="fec2">(.*)</span>')
            hora_mastarde = hora_mastarde.split("</span>")
            hora_mastarde = hora_mastarde[0]
            epg_channel.append(hora_mastarde)   # index 5 
            evento_mastarde = plugintools.find_single_match(entry, '<span class="tprg2">(.*?)</span>')
            #print 'evento_mastarde',evento_mastarde
            epg_channel.append(evento_mastarde)    # index 6            
            sinopsis = '[COLOR lightgreen][I]('+diff_luego+') [/I][/COLOR][COLOR white][B]'+hora_luego+' [/COLOR][/B]'+evento_luego+'[CR][COLOR white][B][CR]'+hora_mastarde+' [/COLOR][/B] '+evento_mastarde
            plugintools.log("Sinopsis: "+sinopsis)
            datamovie = {}
            datamovie["Plot"]=sinopsis
            #plugintools.add_item(action="", title= '[COLOR orange][B]'+channel+' [/B][COLOR lightyellow]'+ahora+'[/COLOR] [COLOR lightgreen][I]('+diff_luego+') [/I][/COLOR][COLOR white][B]'+hora_luego+' [/COLOR][/B] '+evento_luego, info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
            #plugintools.log("entry= "+entry)
            return epg_channel            
        



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

    
        
        
    
    
