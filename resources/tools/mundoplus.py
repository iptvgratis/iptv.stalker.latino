# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Mundoplus.tv parser para Arena+
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


thumbnail = 'http://www.mundoplus.tv/tpl/v3.1/logo_mundoplus.png'
fanart = 'http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg'


def mundoplus_guide(params):
    plugintools.log("[Arena+ 0.3.3].Mundoplus.tv "+repr(params))

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    title = params.get("title")
    title = title.replace("[COLOR white]", "").replace("[COLOR lightyellow]", "").replace("[I]", "").replace("[/I]", "").replace("[/COLOR]", "").replace("[Multiparser]", "").replace(" ", "+").strip()
    title = title.lower().strip()
    url = 'http://www.mundoplus.tv/programacion/buscador.php?canal=g_todos&fecha=TODAS&buscar='+title
    params["url"]=url
    try:
        url = params.get("url")
        referer = 'http://www.mundoplus.tv'
        mundoplus1(params)
    except:
        pass

    

def mundoplus0(params):
    plugintools.log("[Arena+ 0.3.3].Mundoplus.tv "+repr(params))
    try:
        texto = "";
        texto='strain'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("mundoplus_search",texto)
        params["plot"]=texto
        texto = texto.lower()        
        if texto == "": errormsg = plugintools.message("Arena+","Por favor, introduzca serie a buscar");return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            url = 'http://www.mundoplus.tv/programacion/buscador.php?canal=g_todos&fecha=TODAS&buscar='+texto
            #url = 'http://www.alluc.com/stream/'+texto+'++lang:es'
            #url=baseurl+'stream/?q='+texto+'&stream=Streams'
            #url=baseurl+'stream/'+texto
            params["url"]=url
            url = params.get("url")
            referer = 'http://www.mundoplus.tv'
            plugintools.log("Texto a buscar: "+title)
            mundoplus1(params)

    except: pass
    



def mundoplus1(params):
    plugintools.log("[Arena+ 0.3.3].Mundoplus.tv búsqueda "+repr(params))

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis

    thumbnail = params.get("thumbnail")
    if thumbnail == "":
        thumbnail = 'http://www.mundoplus.tv/tpl/v3.1/logo_mundoplus.png'

    texto=params.get("plot");url=params.get("url");
    plugintools.add_item(action="", title= '[COLOR royalblue][B]MUNDOPLUS.TV /[/B][/COLOR] [COLOR white]Resultados de la búsqueda: [I][B]"'+texto+'"[/B][/I][/COLOR]', url = "", info_labels = datamovie , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
   
    referer = url
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)

    block_matches = plugintools.find_single_match(data, "Buscador</h1>(.*?)</body>")
    matches = plugintools.find_multiple_matches(block_matches, '<div>(.*?)</div>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        hora_match = plugintools.find_single_match(entry, '<b>(.*?)</b>')
        plugintools.log("hora_match= "+hora_match)
        title_match = entry.replace("<span>", "").replace("</span>", "").replace("<b>", "[B]").replace("</b>", "[/B]").strip()
        channel_match = plugintools.find_single_match(entry, '<span>(.*?)<span>')
        channel_match = channel_match.strip()
        if channel_match == "Cuatro":
            channel_match = channel_match.replace("Cuatro", "[COLOR red]Cuatro[/COLOR]")
        if channel_match == "Energy":
            channel_match = channel_match.replace("Energy", "[COLOR orange]Energy[/COLOR]")
        if channel_match == "Telecinco":
            channel_match = channel_match.replace("Telecinco", "[COLOR blue]Telecinco[/COLOR]")
        if channel_match == "La Sexta":
            channel_match = channel_match.replace("La Sexta", "[COLOR green]laSexta[/COLOR]")
        if channel_match == "Fox":
            channel_match = channel_match.replace("Fox", "[COLOR blue]Fox[/COLOR]")             
        day_match = plugintools.find_single_match(entry, '<span>(.*?)</span>')
        day_match = day_match.split("<span>")
        day_match = day_match[1].strip()
        event_match = entry.split("</b>")
        event_match = event_match[1]
        plugintools.log("event_match= "+event_match)
        plugintools.log("channel_match= "+channel_match)
        plugintools.log("day_match= "+day_match)        
        plugintools.log("title_match= "+title_match)
        title_fixed = '[COLOR lightyellow]'+day_match+'/[COLOR lightyellow][B]'+hora_match+' [/B][/COLOR][COLOR lightgreen]'+channel_match+'[/COLOR][COLOR white] '+event_match+'[/COLOR]'
        plugintools.add_item(action="", title= title_fixed, url="", thumbnail = thumbnail, info_labels = datamovie , fanart = fanart , folder = False, isPlayable = False)




def gethttp_referer_headers(url,referer):
    plugintools.log("Arena+ 0.3.3 Gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
