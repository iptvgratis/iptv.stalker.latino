# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de SeriesYonkis para beta.1
# Version 0.1 (22.04.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a las librerías de pelisalacarta de Jesús (www.mimediacenter.info)


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
from resources.tools.resolvers import *
from resources.tools.bers_sy import *

thumbnail = 'http://oi58.tinypic.com/1jwwo6.jpg'
fanart = 'http://st-listas.20minutos.es/images/2012-06/335200/list_640px.jpg?1368294762'
referer = 'http://www.seriesflv.com/'



def seriesyonkis(params):
    plugintools.log('[%s %s] SeriesYonkis %s' % (addonName, addonVersion, repr(params)))
    
    url = 'http://www.seriesyonkis.sx/lista-de-series'
    referer = 'http://www.seriesyonkis.sx/'
    
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
        
    data = gethttp_referer_headers(url, referer, show)
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)      
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)</ul>')
    #plugintools.log("listado= "+match_series)
    plugintools.add_item(action="", title = "[COLOR orange][B]Lista de series[/B][/COLOR]", url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    letra_activa = plugintools.find_single_match(match_series, '<li class="active">(.*?)</li>')
    url = plugintools.find_single_match(letra_activa, '<a href="([^"]+)')
    plugintools.log("url= "+url)
    title = url.replace("/lista-de-series/", "")
    plugintools.add_item(action="", title = title, url = url, thumbnail = thumbnail , fanart = fanart , page = show, folder = True, isPlayable = False)

    letras = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in letras:
        url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        plugintools.log("url= "+url)
        title = url.replace("/lista-de-series/", "")
        plugintools.log("title= "+title)
        plugintools.add_item(action="lista_letra", title = title, url = url, thumbnail = thumbnail , fanart = fanart , page = show , folder = True, isPlayable = False)



def lista_letra(params):    
    plugintools.log('[%s %s] lista_letra %s' % (addonName, addonVersion, repr(params)))    

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show == "":
        show = params.get("page")
        if show == "":
            show = "tvshows"
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)    

    url = params.get("url")
    url = 'http://www.seriesyonkis.sx/'+url
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url, referer, show)
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)      
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)<div id="sidebar-section">')
    plugintools.log("listado= "+match_series)

    # Paginador de series por letra (botón "siguiente")
    paginador_next(data)

    # Listado de series
    lista_series(match_series)



# Listado de series
def lista_series(match_series):

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show == "":
        show = params.get("page")
        if show == "":
            show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
    
    serie = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in serie:
        url = plugintools.find_single_match(entry, 'href="([^"]+)')
        url = 'http://www.seriesyonkis.sx'+url
        plugintools.log("url= "+url)
        title_serie = plugintools.find_single_match(entry, 'title="([^"]+)').strip()
        plugintools.log("title_serie= "+title_serie)
        if title_serie != "":
            plugintools.log("url_serie= "+url)
            plugintools.add_item(action="serie_capis", title = title_serie, url = url, thumbnail = thumbnail , fanart = fanart , page = show , folder = True, isPlayable = False)    
        

# Paginador de series por letra
def paginador_next(data):
    
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show == "":
        show = params.get("page")
        if show == "":
            show = "tvshows"
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)
    
    match_paginas = plugintools.find_single_match(data, 'class="paginator">(.*?)<div id="sidebar-section">')
    plugintools.log("match_paginas= "+match_paginas)
    pag_actual = plugintools.find_single_match(match_paginas, '<strong>(.*?)</strong>')
    plugintools.log("pag_actual = "+str(pag_actual))
    num_pags = plugintools.find_multiple_matches(match_paginas, '<a(.*?)</a>')
    i = 0
    for entry in num_pags:
        i = i + 1
    plugintools.log("Núm. páginas= "+str(i))
    next = int(pag_actual) + 1
    plugintools.add_item(action="", title= '[COLOR lightyellow][I]Siguiente (Pág. '+str(next)+')[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , page = show , folder = True , isPlayable = False)    




def serie_capis(params):
    plugintools.log('[%s %s] serie_capis %s' % (addonName, addonVersion, repr(params)))

    show = params.get("page")
    plugintools.modo_vista(show)

    bers_sy_on = plugintools.get_setting("bers_sy_on")
    bers_sy_level = plugintools.get_setting("bers_sy_level")
    plugintools.log("bers_sy_on= "+bers_sy_on)
    plugintools.log("bers_sy_level= "+bers_sy_level)
	
    if bers_sy_on == "true" and bers_sy_level == "1":  # Control para ejecutar el BERS para toda la serie
        bers_sy0(params)
    else:    
        datamovie={}
        if params.get("plot") != "":
                datamovie["Plot"]=params.get("plot")  # Cargamos sinopsis de la serie... (si existe)
        else:
                datamovie["Plot"]="."
                
        show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
        if show is None:
                show = params.get("page")        
                if show is None:
                        show = "tvshows"            
        print show
        plugintools.modo_vista(show)
        
        url = params.get("url")
        referer = 'http://www.seriesyonkis.sx/'
        data = gethttp_referer_headers(url,referer,show)
        show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
        if show is None:
                show = params.get("page")
                if show is None:
                        show = "tvshows"
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)      
        #plugintools.log("data= "+data)
        
        #Carátula
        cover = plugintools.find_single_match(data, '<img src="([^"]+)')
        match_temporadas = plugintools.find_single_match(data, '<div id="section-content">(.*?)</ul>')
        temps = plugintools.find_multiple_matches(match_temporadas, '<h3 class="season"(.*?)</li>')
        
        for entry in temps:
            capis = plugintools.find_multiple_matches(entry, '<td class="episode-title">(.*?)</td>')
            for entri in capis:
                #plugintools.log("entri= "+entri)
                url_cap = plugintools.find_single_match(entri, '<a href="([^"]+)')
                url_cap = 'http://www.seriesyonkis.sx'+url_cap
                plugintools.log("url_cap= "+url_cap)
                num_cap = plugintools.find_single_match(entri, '<strong>(.*?)</strong>')
                num_cap = num_cap.strip()
                plugintools.log("num_cap= "+num_cap)
                title_cap = plugintools.find_single_match(entri, '</strong>(.*?)</a>')
                title_cap = title_cap.strip()
                plugintools.log("title_cap= "+title_cap)
                title_capi = '[COLOR orange][B]'+num_cap+'[/B][COLOR white]'+title_cap+'[/COLOR]'.strip()
                title_fixed = num_cap + title_cap
                title_fixed = title_fixed.strip()
                plugintools.add_item(action="enlaces_capi", title=title_capi, url = url_cap, thumbnail = cover , plot = datamovie["Plot"], info_labels = datamovie , fanart = fanart, folder = True, page = show, extra = title_fixed , isPlayable = False)

    plugintools.modo_vista(show)                




def enlaces_capi(params):
    plugintools.log('[%s %s] enlaces_capi %s' % (addonName, addonVersion, repr(params)))

    show = params.get("page")
    plugintools.modo_vista(show)    

    datamovie = {}
    datamovie["Plot"] = params.get("plot")

    url = params.get("url")
    title_fixed = params.get("extra")
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url,referer,show)  
    plugintools.modo_vista(show)      
    #plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, '<h2 class="header-subtitle veronline">(.*?)</table>')
    match_veronline = plugintools.find_single_match(matches, '<tbody>(.*?)</tbody>')
    match_links = plugintools.find_multiple_matches(match_veronline, '<tr>(.*?)</tr>')
    for entry in match_links:
        plugintools.log("entry= "+entry)
        title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        server = plugintools.find_single_match(entry, 'watch via([^"]+)')
        plugintools.log("server= "+server)
        idioma_capi = plugintools.find_single_match(entry, '<span class="flags(.*?)</span></td>')
        idioma_capi_fixed = idioma_capi.split(">")
        if len(idioma_capi_fixed) >= 2:
            idioma_capi = idioma_capi_fixed[1]
        plugintools.log("idioma_capi= "+idioma_capi)
        if idioma_capi == "English":
            idioma_capi = ' [ENG]'
        elif idioma_capi == "english":
            idioma_capi = ' [ENG]'            
        elif idioma_capi == "Español":
            idioma_capi = ' [ESP]'
        elif idioma_capi == "Latino":
            idioma_capi = ' [LAT]'
        elif idioma_capi.find("English-Spanish SUBS") >= 0:
            idioma_capi = ' [VOSE]'
        elif idioma_capi.find("Japanese-Spanish SUBS") >= 0:
            idioma_capi = ' [VOSE]'
        else:
            idioma_capi = " [N/D]"
        plugintools.log("idioma_capi= "+idioma_capi)        
        page_url = 'http://www.seriesyonkis.sx/'+page_url
        plot = datamovie["Plot"]
        source_web="seriesyonkis"
        bers_sy_on = plugintools.get_setting("bers_sy_on")  # Control para activar BERS para el capítulo
        
        if server.find("tumi.tv") >= 0:
            desc = '[Tumi]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                        
        elif server.find("streamin.to") >= 0:
            desc = '[Streamin.to]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                           
        elif server.find("vidspot") >= 0:
            desc = '[Vidspot]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                         
        elif server.find("allmyvideos") >= 0:
            desc = '[allmyvideos]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                      
        elif server.find("streamcloud") >= 0:
            desc = '[Streamcloud]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
             
        elif server.find("nowvideo.sx") >= 0:
            desc = '[Nowvideo]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                           
        elif server.find("veehd") >= 0:
            desc = '[VeeHD]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title =title, url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
            
        if server.find("allmyvideos") >= 0:
            desc = '[Allmyvideos]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'            
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie , thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
            
        elif server.find("novamov.com") >= 0:
            desc = '[Novamov]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'            
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                           
        elif server.find("Moevideos") >= 0:
            desc = '[Vidspot]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                         
        elif server.find("Gamovideo") >= 0:
            desc = '[allmyvideos]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                      
        elif server.find("movshare.net") >= 0:
            desc = '[Movshare]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
                         
        elif server.find("played.to") >= 0:
            desc = '[Played.to]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
               
        elif server.find("mail.ru") >= 0:
            desc = '[Mail.ru]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)

        elif server.find("vk") >= 0:
            desc = '[Vk]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
            
        elif server.find("videobam") >= 0:
            desc = '[Videobam]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)

        elif server.find("powvideo.net") >= 0:
            desc = '[Powvideo]'
            title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR] [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
            plugintools.add_item(action="getlink", title = title , url = page_url , info_labels = datamovie, thumbnail = thumbnail , fanart = fanart, page = show , folder = False, isPlayable = True)
            if bers_sy_on == 1:  # Control para ejecutar BERS a nivel de capítulo
                bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)

    plugintools.modo_vista(show)                 
                  
    

def getlink(params):
    plugintools.log('[%s %s] getlink %s' % (addonName, addonVersion, repr(params)))  

    show = plugintools.get_setting("series_id")
    plugintools.modo_vista(show) 
    
    page_url = params.get("url")
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(page_url,referer,show)
    plugintools.modo_vista(show)
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = params.get("page")
        if show is None:
            show = "tvshows"
    plugintools.log("show= "+show)
    plugintools.modo_vista(show)      
    match = plugintools.find_single_match(data, '<table class="episodes full-width">(.*?)</table>')
    url_final = plugintools.find_single_match(match, '<a href="([^"]+)')
    plugintools.modo_vista(show) 
    if url_final.find("allmyvideos") >= 0:
        params["url"]=url_final
        allmyvideos(params)
    elif url_final.find("vidspot") >= 0:
        params["url"]=url_final
        vidspot(params)
    if url_final.find("played.to") >= 0:
        params["url"]=url_final
        playedto(params)        
    elif url_final.find("streamcloud") >= 0:
        params["url"]=url_final
        streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0:
        params["url"]=url_final
        nowvideo(params)
    elif url_final.find("streamin.to") >= 0:
        params["url"]=url_final
        streaminto(params)        
    elif url_final.find("veehd") >= 0:
        params["url"]=url_final
        veehd(params)
    elif url_final.find("novamov") >= 0:
        params["url"]=url_final
        novamov(params)
    elif url_final.find("gamovideo") >= 0:
        params["url"]=url_final
        gamovideo(params)
    elif url_final.find("moevideos") >= 0:
        params["url"]=url_final
        moevideos(params)
    elif url_final.find("movshare") >= 0:
        params["url"]=url_final
        movshare(params)
    elif url_final.find("vk") >= 0:
        params["url"]=url_final
        vk(params)
    elif url_final.find("tumi") >= 0:
        params["url"]=url_final
        tumi(params)
    elif url_final.find("vk") >= 0:
        params["url"]=url_final
        vk(params)
    elif url_final.find("videobam") >= 0:
        params["url"]=url_final
        videobam(params)        
    elif url_final.find("mail.ru") >= 0:
        params["url"]=url_final
        mailru(params)        

    plugintools.modo_vista(show)        
       

def gethttp_referer_headers(url,referer,show):
    params = plugintools.get_params()
    show_default = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV    
    if show_default is None:
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    else:
        show = show_default
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.modo_vista(show)
    return body

