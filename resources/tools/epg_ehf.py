# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 EPG EHF.com
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


def epg_ehf(params):
    plugintools.log("[beta.1-0.3.0].EPG EHF.com loading... "+repr(params))

    horas = []
    eventos = []

    from datetime import datetime  

    url = params.get("url")
    
    # Obtenemos programación del día
    get_program(horas, eventos, url)

    
   
def get_program(horas, eventos, url):
    plugintools.log("[beta.1-0.3.1].get_program "+url)

    thumbnail = 'http://kif.dk/wp-content/uploads/2013/07/ehfTV-banner_300x85px.png'
    fanart = 'http://i.ytimg.com/vi/i1HG9sCrO-0/maxresdefault.jpg'
    
    from datetime import datetime

    # Construimos fecha y hora actual para construir URL
    ahora = datetime.now()
    anno_actual = ahora.year
    mes_actual = ahora.month
    dia_actual = ahora.day
    fecha = str(ahora.year) + str(ahora.month) + str(ahora.day)
    
    # Obtenemos datos de la programación...
    data = gethttp_noref(url)

    #<div class="msgWithOpts">Sorry, there are no TV dates yet for this week.<br />
    sorry = plugintools.find_single_match(data, '<div class="msgWithOpts">(.*?)<br />')
    print 'sorry',sorry
    if data.find("Sorry, there are no TV dates yet for this week") >= 0:
        plugintools.add_item(action="", title='[COLOR lightyellow]Sorry, there are no TV dates yet for this week[/COLOR]' , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
    else:
        week = plugintools.find_single_match(data, 'week-(.*?)\"')
        plugintools.log("week= "+week)
        url = 'http://www.eurohandball.com/2015/tv-guide/week-'+week
        data = gethttp_noref(url)
        plugintools.log("data= "+data)
        plugintools.add_item(action="", title='[COLOR orange][B]Balonmano en Televisión: Semana '+week+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
        dates = plugintools.find_single_match(data, '<label>([^<]+)</label>')
        dates = dates.replace("&nbsp;from", "Del")
        dates = dates.replace("to", "al")
       
        miercoles = plugintools.find_single_match(data, 'id="tvDay_2"(.*?)</div>')
        miercoles_date = plugintools.find_single_match(miercoles, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(miercoles, '<td class="B">(.*?)</td>')
        miercoles_date = miercoles_date.replace("Wed", "Miércoles")
        plugintools.log("miercoles= "+miercoles_date)
        jueves = plugintools.find_single_match(data, 'id="tvDay_3"(.*?)</div>')
        jueves_date = plugintools.find_single_match(jueves, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(jueves, '<td class="B">(.*?)</td>')
        jueves_date = jueves_date.replace("Thu", "Jueves")
        plugintools.log("jueves= "+jueves_date)
        viernes = plugintools.find_single_match(data, 'id="tvDay_4"(.*?)</div>')
        viernes_date = plugintools.find_single_match(viernes, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(viernes, '<td class="B">(.*?)</td>')
        viernes_date = viernes_date.replace("Fri", "Viernes")
        plugintools.log("viernes= "+viernes_date)
        sabado = plugintools.find_single_match(data, 'id="tvDay_5"(.*?)</div>')
        sabado_date = plugintools.find_single_match(sabado, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(sabado, '<td class="B">(.*?)</td>')
        sabado_date = sabado_date.replace("Sat", "Sábado")
        plugintools.log("sabado= "+sabado_date)
        domingo = plugintools.find_single_match(data, 'id="tvDay_6"(.*?)</div>')
        domingo_date = plugintools.find_single_match(domingo, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(domingo, '<td class="B">(.*?)</td>')
        domingo_date = domingo_date.replace("Sun", "Domingo")
        plugintools.log("domingo= "+domingo_date)

        # LUNES
        day_matches = plugintools.find_single_match(data, 'id="tvDay_0"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:            
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)              

        # MARTES
        day_matches = plugintools.find_single_match(data, 'id="tvDay_1"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:            
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)  

        # MIÉRCOLES
        day_matches = plugintools.find_single_match(data, 'id="tvDay_2"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:            
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)

        # JUEVES
        day_matches = plugintools.find_single_match(data, 'id="tvDay_3"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:            
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)

        # VIERNES
        day_matches = plugintools.find_single_match(data, 'id="tvDay_4"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:
                plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)

        # SÁBADO
        day_matches = plugintools.find_single_match(data, 'id="tvDay_5"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:
                plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="" , thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)

        # DOMINGO
        day_matches = plugintools.find_single_match(data, 'id="tvDay_6"(.*?)</table>')
        plugintools.log("day_matches = " +day_matches)
        day_date = plugintools.find_single_match(day_matches, '<td class="A">(.*?)</td>') + ' ' + plugintools.find_single_match(day_matches, '<td class="B">(.*?)</td>')
        day_date = day_date.replace("Mon", "Lunes")
        bloque_partido = plugintools.find_multiple_matches(day_matches, '<td class="C">(.*?)</tr>')
        for partido in bloque_partido:
            if partido == "":
                plugintools.log("No hay eventos para el "+day_date)
            else:
                plugintools.add_item(action="", title='[COLOR lightyellow][B]'+day_date+'[/B][/COLOR]', url="", thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
                plugintools.log("partido= "+partido)
                event = plugintools.find_single_match(partido, '<span class="m1">(.*?)</a>')
                event_time = plugintools.find_single_match(partido, '<b>(.*?)</b>')
                event_type = plugintools.find_single_match(event, '<b>(.*?)</b>')
                event_type = event_type.replace("&nbsp;", " ")
                event_teams = plugintools.find_multiple_matches(event, '<span class="C">(.*?)</span>')
                plugintools.log("event_type= "+event_type)
                plugintools.log("event_time= "+event_time)        
            for equipos_partido in event_teams:
                #plugintools.log("equipos_partido= "+equipos_partido)
                if equipos_partido.startswith("<img alt") == True:
                    pass
                else:
                    equipos_partido = equipos_partido.split("<br />")
                    partidazo = equipos_partido[0].strip() + ' vs ' + equipos_partido[1].strip()
                    partidazo= encode_string(partidazo)
                    plugintools.log("partidazo= "+partidazo)
                    plugintools.add_item(action="", title='  [COLOR lightgreen][B]'+event_time+ '[/COLOR][/B][COLOR lightblue] ' + event_type + '[/COLOR][COLOR white] ' + partidazo+'[/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Delayed Broadcasters
            delayed_tv = plugintools.find_single_match(partido, '<div class="tv1">(.*?)</div>')
            ch_delayed = plugintools.find_multiple_matches(delayed_tv, '</big>(.*?)</span>')
            time_delayed = plugintools.find_multiple_matches(delayed_tv, '<span class="C">(.*?)</span>')
            for ch in ch_delayed:
                plugintools.log("canal= "+ch)        
            for hora in time_delayed:
                plugintools.log("hora= "+hora)
                plugintools.add_item(action="", title='     [COLOR orange]'+ch+' [/COLOR][COLOR lightgreen]('+hora+'h) [/COLOR][I][COLOR lightyellow][Delayed][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)
            # Live Broadcasters
            live_tv = plugintools.find_single_match(partido, '<div class="tv1 live">(.*?)</div>')
            ch_live = plugintools.find_multiple_matches(live_tv, '</big>(.*?)</span>')
            time_live = plugintools.find_multiple_matches(live_tv, '<span class="C">(.*?)</span>')
            for canal_live in ch_live:
                plugintools.log("canal= "+canal_live)
                for hora_live in time_live:
                    plugintools.log("hora= "+hora_live)
                plugintools.add_item(action="", title='     [COLOR orange]'+canal_live+' [/COLOR][COLOR lightgreen]('+hora_live+'h) [/COLOR][I][COLOR lightyellow][Live][/I][/COLOR]', thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=False)             
            
            
                 

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
    
