# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 EPG miguiatv.com
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

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
FANART = "fanart"
OTHER = "other"
MUSIC = "music"

def epg_now(title):
    plugintools.log('[%s %s].epg_now %s' % (addonName, addonVersion, title))
    channel = title.lower()
    plugintools.log("Canal: "+channel)
   
    if channel == "la 1" or channel == "la 1 hd":
        channel = "tve1"
        epg_channel = get_epg(channel)
        return epg_channel
    elif channel == "la 2":
        channel = "la2"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "antena 3" or channel == "antena 3 hd":
        channel = "antena3"
        epg_channel = get_epg(channel)
        return epg_channel
    elif channel == "cuatro" or channel == "cuatro hd":
        channel = "cuatro"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "telecinco" or channel == "telecinco hd":
        channel == "telecinco"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "la sexta" or channel == "la sexta hd":
        channel = "la-sexta"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+" or channel == "canal+ 1" or channel == "canal plus" or channel == "canal+ hd":
        channel = "canal+1"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "goltv" or channel == "golt":
        channel = "goltv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "40 TV":
        channel = "los40"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "andalucía tv" or channel == "andalucia tv":
        channel = "andalucia-tv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "bio":
        channel = "bio"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "calle 13" or channel == "calle 13 hd":
        channel = "calle-13"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal barça" or channel == "canal barca":
        channel = "canal-barca"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "40 TV":
        channel = "los40"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "andalucía tv" or channel == "andalucia tv":
        channel = "andalucia-tv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "aragón tv" or channel == "aragon tv":
        channel = "aragon-television"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "axn" or channel == "axn hd":
        channel = "axn"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "bio":
        channel = "bio"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal barça" or channel == "canal barca":
        channel = "canal-barca"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ 30" or channel == "canal+ ...30" or channel == "canal plus 30":
        channel = "canal-plus-30"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ 2" or channel == "canal+ 2 hd" or channel == "canal plus 2 hd":
        channel = "canal-plus-2"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ accion" or channel == "canal+ acción" or channel=="canal plus accion":
        channel = "canal-plus-accion"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ comedia" or channel == "canal plus comedia":
        channel = "canal-plus-comedia"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ decine" or channel == "canal plus decine":
        channel = "canal-plus-decine"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ deporte" or channel == "canal plus deporte":
        channel = "canal-plus-deporte"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ futbol" or channel == "canal+ fútbol" or channel == "canal plus fútbol" or channel == "canal plus futbol":
        channel = "canal-plus-futbol"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ golf" or channel == "canal plus golf":
        channel = "golf-plus"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ toros" or channel == "canal plus toros":
        channel = "canalplus-toros"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ extra" or channel=="canal plus extra":
        channel = "canalplus-xtra"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal 33" or channel == "canal33":
        channel = "canal33"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal cocina":
        channel = "canal-cocina"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "cartoon network" or channel == "cartoon network hd":
        channel = "cartoon-network"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "castilla-la mancha televisión" or channel == "castilla-la mancha tv":
        channel = "castilla-la-mancha"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "caza y pesca":
        channel = "caza-y-pesca"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "clan tve" or channel == "clan tve 50":
        channel = "clan-tve-50"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "cnbc":
        channel = "cnbc"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "cnn-international" or channel == "cnn int":
        channel = "cnn-international"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv":
        channel = "cosmopolitan"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "canal+ dcine" or channel == "canal plus dcine":
        channel = "dcine-espanol"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "decasa":
        channel = "decasa"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "discovery channel":
        channel = "discovery-channel"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "discovery max":
        channel = "discovery-max"
        epg_channel = get_epg(channel)
        return epg_channel
    elif channel == "disney channel":
        channel = "disney-channel"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "disney-cinemagic":
        channel = "disney-cinemagic"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "disney xd":
        channel = "disney-xd"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "divinity":
        channel = "divinity"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "energy":
        channel = "energy"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "etb1" or channel == "etb 1":
        channel = "etb1"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "etb 2" or channel == "etb2":
        channel = "etb2"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "factoría de ficción" or channel == "factoria de ficcion" or channel == "fdf":
        channel = "factoria-de-ficcion"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "fox" or channel == "fox hd":
        channel = "fox"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "fox crime" or channel == "fox life" or channel == "fox crime hd":
        channel = "fox-crime"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "fox news":
        channel = "fox-news"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "historia" or channel == "historia hd":
        channel = "historia"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "cosmopolitan" or channel == "cosmopolitan tv":
        channel = "cosmopolitan"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "hollywood" or channel == "hollywood channel":
        channel = "hollywood"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "ib3 televisio" or channel == "ib3 televisió":
        channel = "ib3-televisio"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "intereconomia" or channel == "intereconomía" or channel == "intereconomía tv":
        channel = "intereconomia"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "mtv" or channel == "mtv españa" or channel == "mtv espana":
        channel = "mtv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "national geographic" or channel == "nat geographic" or channel == "nat geo":
        channel = "national-geographic"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "neox":
        channel = "neox"
        epg_channel = get_epg(channel)
        return epg_channel             
    elif channel == "nick jr":
        channel = "nick-jr"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "odisea" or channel == "odisea hd":
        channel = "odisea"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "nova":
        channel = "nova"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "panda":
        channel = "panda"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "paramount comedy":
        channel = "paramount"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "playboy tv":
        channel = "playboy-tv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "playhouse disney":
        channel = "playhouse-disney"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "radiotelevision de murcia" or channel == "radiotelevisión de murcia" or channel == "rtv murcia":
        channel = "radiotelevision-de-murcia"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "real madrid tv":
        channel = "real-madrid-tv"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "syfy" or channel == "syfy hd" or channel == "scifi":
        channel = "sci-fi"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "sony entertainment":
        channel = "sony-entertainment"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "sportmania" or channel == "sportmania hd":
        channel = "sportmania"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "tcm":
        channel = "tcm"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "teledeporte" or channel == "intereconomía" or channel == "intereconomía tv":
        channel = "teledeporte"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "telemadrid" or channel == "telemadrid hd":
        channel = "telemadrid"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "televisión canaria" or channel == "televisión canaria":
        channel = "television-canaria"
        epg_channel = get_epg(channel)
        return epg_channel         
    elif channel == "televisión de galicia" or channel == "television de galicia" or channel == "tvg":
        channel = "tvg"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "tnt" or channel == "tnt hd":
        channel = "tnt"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "tv3" or channel == "tv3 hd":
        channel = "tv3"
        epg_channel = get_epg(channel)
        return epg_channel        
    elif channel == "vh1":
        channel = "vh1"
    elif channel == "viajar":
        channel = "viajar"
        epg_channel = get_epg(channel)
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

def get_epg(channel):
    plugintools.log('[%s %s].get_epg %s' % (addonName, addonVersion, channel))	

    horas = []
    eventos = []
    horas_next = []  # Lista extendida (hoy-mañana)
    eventos_next = []  # Lista extendida (hoy-mañana)
    horas_prev = []  # Lista extendida (ayer-hoy)
    eventos_prev = []  # Lista extendida (ayer-hoy)      
    
    # Obtenemos programación del día en una lista
    epg_channel = []
    
    # Programación de AYER: Calculamos fecha actual para construir URL
    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    ayer = int(ahora.day) - 1

    # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
    if ayer <= 9:
        dia_actual = "0" + str(ayer)

    if mes_actual <= 9:
        mes_actual = "0" + str(mes_actual)
        
    fecha = str(ahora.year) + str(mes_actual) + str(ayer)

    # Construimos la URL...
    url = 'http://www.miguiatv.com/'+fecha+'/'+channel
    plugintools.log("URL Ayer= "+url)
    
    # Obtenemos datos de la programación...
    data = gethttp_withref(url)
    title = plugintools.find_single_match(data, '<title>([^<]+)</title>')
    body = plugintools.find_single_match(data, 'table-condensed table-striped(.*?)</table>')
    event = plugintools.find_multiple_matches(data, '<tr>(.*?)</tr>')
    control = 0  # Interruptor que evalúa evento anterior y posterior a la hora actual
    for entry in event:
        time_event = plugintools.find_single_match(entry, '\"top\">([^<]+)</td>')
        #plugintools.log("time_event= "+time_event)
        hora_event = (int(time_event[0:2]) * 60 + int(time_event[3:5]))
        #plugintools.log("hora_event= "+str(hora_event))
        time_now = (ahora.hour * 60) + ahora.minute
        event_name = plugintools.find_single_match(entry, '<a href[^>]+>([^<]+)</a>')
        #plugintools.log("event_name= "+event_name)
        horas.append(time_event)
        eventos.append(event_name)
        horas_prev.append(time_event)
        eventos_prev.append(event_name)        
    
    # Programación de HOY: Calculamos fecha actual para construir URL
    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    hoy = ahora.day

    # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
    if hoy <= 9:
        hoy = "0" + str(hoy)

    if mes_actual <= 9:
        mes_actual = "0" + str(ahora.month)
        
    fecha = str(ahora.year) + str(mes_actual) + str(hoy)

    # Construimos la URL...
    url = 'http://www.miguiatv.com/'+fecha+'/'+channel
    plugintools.log("URL Hoy= "+url)    
    
    # Obtenemos datos de la programación...
    data = gethttp_withref(url)
    title = plugintools.find_single_match(data, '<title>([^<]+)</title>')
    body = plugintools.find_single_match(data, 'table-condensed table-striped(.*?)</table>')
    event = plugintools.find_multiple_matches(data, '<tr>(.*?)</tr>')
    control = 0  # Interruptor que evalúa evento anterior y posterior a la hora actual
    for entry in event:
        time_event = plugintools.find_single_match(entry, '\"top\">([^<]+)</td>')
        #plugintools.log("time_event= "+time_event)        
        hora_event = (int(time_event[0:2]) * 60 + int(time_event[3:5]))
        time_now = (ahora.hour * 60) + ahora.minute
        event_name = plugintools.find_single_match(entry, '<a href[^>]+>([^<]+)</a>')
        #plugintools.log("event_name= "+event_name)        
        horas.append(time_event)
        eventos.append(event_name)
        horas_prev.append(time_event)
        eventos_prev.append(event_name)        
        horas_next.append(time_event)
        eventos_next.append(event_name)        
        
    # Programación de MAÑANA: Calculamos fecha actual para construir URL
    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    manana = int(ahora.day) + 1

    # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
    if manana <= 9:
        dia_actual = "0" + str(manana)

    if mes_actual <= 9:
        mes_actual = "0" + str(ahora.month)
        
    fecha = str(ahora.year) + str(mes_actual) + str(manana)

    # Construimos la URL...
    url = 'http://www.miguiatv.com/'+fecha+'/'+channel
    plugintools.log("URL Mañana= "+url)      
    
    # Obtenemos datos de la programación...
    data = gethttp_withref(url)
    title = plugintools.find_single_match(data, '<title>([^<]+)</title>')
    body = plugintools.find_single_match(data, 'table-condensed table-striped(.*?)</table>')
    event = plugintools.find_multiple_matches(data, '<tr>(.*?)</tr>')
    control = 0  # Interruptor que evalúa evento anterior y posterior a la hora actual
    for entry in event:
        time_event = plugintools.find_single_match(entry, '\"top\">([^<]+)</td>')
        plugintools.log("time_event= "+time_event)
        hora_event = (int(time_event[0:2]) * 60 + int(time_event[3:5]))
        plugintools.log("hora_event= "+str(hora_event))
        time_now = (ahora.hour * 60) + ahora.minute
        event_name = plugintools.find_single_match(entry, '<a href[^>]+>([^<]+)</a>')
        plugintools.log("event_name= "+event_name)
        horas.append(time_event)
        eventos.append(event_name)
        horas_next.append(time_event)
        eventos_next.append(event_name)         
    
    # Control de medianoche: ESTO NO FUNCIONA PORQUE A VECES EN ESTA WEB MUESTRAN HASTA LAS 06:00 HORAS DEL DÍA SIGUIENTE
    # Si el último evento de hoy empezó antes que la hora actual, mostrar en titulo y además mostrar los tres primeros eventos de MAÑANA
    # Si el primer evento de hoy es posterior a la hora actual, mostramos ese evento y los tres siguientes en la sinopsis

    try:
        cont = len(horas)
        cont = cont - 1
        if horas[cont] != "":
            plugintools.log("Último evento: "+horas[cont])
            plugintools.log("Hora de emisión: "+horas[cont])
            hora_ult_evento = (int(time_event[0:2]) * 60 + int(time_event[3:5]))
            plugintools.log("Hora último evento: "+str(hora_ult_evento))

        # Comparación de horas para determinar evento en emisión
        if int(ahora.hour) >= 22:   # Control de medianoche (cuando la hora es posterior al inicio del último evento debe leer eventos de mañana)
            plugintools.log("Control medianoche")
            horas = horas_next
            eventos = eventos_next
        elif int(ahora.hour) < 6:   # Control salto de día para que muestre primeros eventos de mañana
            plugintools.log("Control vespertino")
            horas = horas_next
            eventos = eventos_next
        else:
            horas = horas_next
            eventos = eventos_next
    except:
        pass
        
    #Iniciamos comparación de horas
    time_now = (ahora.hour * 60) + ahora.minute
    plugintools.log("hora en minutos: "+str(time_now))    
    i = 0
    try:
        while i < len(horas):
            time_event = horas[i]
            time_event = ( int(time_event[0:2]) * 60 ) + int(time_event[3:5])
            diff = time_event - time_now
            plugintools.log("diff= "+str(diff))
            if diff >= 0:
                hora_ahora = horas[i-1]
                evento_ahora = eventos[i-1]
                hora_luego = horas[i]
                evento_luego = eventos[i]
                hora_despues = horas[i+1]
                evento_despues = eventos[i+1]
                hora_4 = horas[i+2]
                evento_4 = eventos[i+2]
                hora_5 = horas[i+3]
                evento_5 = eventos[i+3]                 
                epg_channel =  hora_ahora,evento_ahora,hora_luego,evento_luego,hora_despues,evento_despues,hora_4,evento_4,hora_5,evento_5
                return epg_channel
                break
            i = i + 1
    except:
        pass        

    # Si la hora actual es anterior a la del primer evento, leer programación del día anterior
    # Si la hora actual es posterior al último evento, leer programación del día siguiente
    # Bug!: A las 22:12 horas salta un error en Telecinco porque la siguiente emisión es a las 6 de la madrugada (¿?)



def gethttp_withref(url):   
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer","http://www.miguiatv.com/"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body



def modo_vista(show):
    if show == "":
        show = plugintools.get_setting("video_id")
        
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

    plugintools.log("Modo de vista fijado en EPG: "+show) 
    


      
        
    
   


            
   
