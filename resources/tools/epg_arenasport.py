# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 EPG Arenasport
# Version 0.1 (11.11.2014)
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
import time
import epg_miguiatv

from __main__ import *



def epg_arena(url):
    plugintools.log("[beta.1-0.3.0].EPG EHF.com loading... "+url)

    #url = 'http://tv.aladin.info/tv-program-arena-sport-1'
    
    horas = []
    eventos = []
    epg_channel = []
    
    # Obtenemos programación del día
    epg_channel = get_program(horas, eventos, url)
    print epg_channel
    return epg_channel



def get_program(horas, eventos, url):
    plugintools.log("[beta.1-0.3.1].get_program "+url)

    epg_channel = []

    body = gethttp_noref(url)
    arena1 = plugintools.find_multiple_matches(body, '<td class=\'text-center strong \'>(.*?)</td>')
    event = plugintools.find_multiple_matches(body, '<td class=\'\'>(.*?)</td></tr>')
    evento_ahora = plugintools.find_single_match(body, '<td class=\'bg-warning\'>(.*?)</td></tr>')
    next_matches = plugintools.find_single_match(body, evento_ahora+'(.*?)</div>')
    evento_luego = plugintools.find_single_match(next_matches, '<td class=\'\'>(.*?)</td></tr>')
    hora_luego = plugintools.find_single_match(next_matches, '<td class=\'text-center strong \'>(.*?)</td>')
    hora_ahora = plugintools.find_single_match(body, 'class=\'text-center strong bg-warning\'>(.*?)</td><td class=\'bg-warning\'>'+evento_ahora)

    epg_channel = hora_ahora,evento_ahora,hora_luego,evento_luego
    return epg_channel    



def encode_string(txt):
    plugintools.log("[beta.1-0.3.0].encode_string: "+txt)
    
    txt = txt.replace("&#231;", "ç")
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#233;', 'é')
    txt = txt.replace('&#225;', 'á')
    txt = txt.replace('&#241;', 'ñ')
    txt = txt.replace('&#250;', 'ú')
    txt = txt.replace('&#237;', 'í')
    txt = txt.replace('&#243;', 'ó')    
    txt = txt.replace('&#39;', "'")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace("&nbsp;", "")
    txt = txt.replace('&#39;', "'")
    txt = txt.replace('&#246;',"ö")
    txt = txt.replace('&#228;', "ä")
    
    return txt


def gethttp_noref(url):
    plugintools.log("[beta.1-0.3.0.gethttp_noref] "+url)    

    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body

# Esta función devuelve el evento en emisión ahora
def compara_times(horas, eventos):
    plugintools.log("[beta.1-0.3.1].compara_times")
    print horas, eventos

    from datetime import datetime  

    # Determinamos fecha actual para construir URL
    ahora = datetime.now()
    if int(ahora.minute) < 10:
        minutos = "0" + str(ahora.minute)
    else:
        minutos = str(ahora.minute)
    time_now = str(ahora.hour) + ":" + minutos  # Lo pasamos a minutos para comparar
    #plugintools.add_item(action="", title="Son las "+time_now, url="", folder=False, isPlayable=False)
    
    #Iniciamos comparación de horas
    if int(ahora.hour) <= 12:
        time_now = ((ahora.hour + 12) * 60) + ahora.minute
        plugintools.log("Antes de mediodía= "+str(time_now))
    else:
        time_now = (ahora.hour * 60) + ahora.minute
        plugintools.log("Después de mediodía= "+str(time_now))
    
    plugintools.log("time_now= "+str(time_now))
    i = 0
    try:
        while i < len(horas):
            time_event = horas[i]
            time_event = ( int(time_event[0:2]) * 60 ) + int(time_event[3:5])
            plugintools.log("time_event= "+str(time_event))
            if int(ahora.hour) <= 12:
                time_now = ((ahora.hour + 12) * 60) + ahora.minute
                plugintools.log("Antes de mediodía= "+str(time_now))
                diff = time_event - time_now
                print diff
                if diff <= 0:
                    hora_ahora = horas[i-1]
                    evento_ahora = eventos[i-1]
                    plugintools.log("evento_ahora= "+evento_ahora)
                    hora_luego = horas[i]
                    evento_luego = eventos[i]
                    plugintools.log("evento_luego= "+evento_luego)
                    return hora_ahora,evento_ahora,hora_luego,evento_luego
                    break
                else:                    
                    i = i + 1
            if int(ahora.hour) >= 12:
                time_now = ((ahora.hour + 12) * 60) + ahora.minute
                plugintools.log("Antes de mediodía= "+str(time_now))
                diff = time_now - time_event
                print diff
                if diff >= 0:
                    hora_ahora = horas[i-1]
                    evento_ahora = eventos[i-1]
                    plugintools.log("evento_ahora= "+evento_ahora)
                    hora_luego = horas[i]
                    evento_luego = eventos[i]
                    plugintools.log("evento_luego= "+evento_luego)
                    return hora_ahora,evento_ahora,hora_luego,evento_luego
                    break
                else:                    
                    i = i + 1                    
            
    except:
        pass
    

