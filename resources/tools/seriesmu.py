# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Arena+ Parser de SeriesMu
# Version 0.1 (02.11.2014)
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
import plugintools, scrapertools

thumbnail = 'http://oi58.tinypic.com/1jwwo6.jpg'
fanart = 'http://st-listas.20minutos.es/images/2012-06/335200/list_640px.jpg?1368294762'
referer = 'http://www.seriesflv.com/'


def seriesmu(params):
    plugintools.log("[Arena+ 0.3.0].SeriesMu")

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show == "tvshows":
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    elif show == "episodes":
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    elif show == "list":
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    elif show == "movies":
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)
    else:
        show = "tvshows"
        plugintools.log("show= "+show)
        plugintools.modo_vista(show)        
 
    
    url = 'http://www.seriesyonkis.sx/lista-de-series'
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url, referer, show)
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)</ul>')
    #plugintools.log("listado= "+match_series)
    plugintools.add_item(action="", title = "[COLOR orange][B]Lista de series[/B][/COLOR]", url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    letra_activa = plugintools.find_single_match(match_series, '<li class="active">(.*?)</li>')
    url = plugintools.find_single_match(letra_activa, '<a href="([^"]+)')
    plugintools.log("url= "+url)
    title = url.replace("/lista-de-series/", "")
    plugintools.add_item(action="", title = title, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

    letras = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in letras:
        url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        plugintools.log("url= "+url)
        title = url.replace("/lista-de-series/", "")
        plugintools.log("title= "+title)
        plugintools.add_item(action="lista_letra", title = title, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

    plugintools.modo_vista(show)        



def lista_letra(params):
    plugintools.log("[Arena+ 0.3.0].SeriesYonkis.Lista_letra")

    url = params.get("url")
    url = 'http://www.seriesyonkis.sx/'+url
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url, referer)
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)<div id="sidebar-section">')
    plugintools.log("listado= "+match_series)

    # Paginador de series por letra (botón "siguiente")
    paginador_next(data)

    # Listado de series
    lista_series(match_series)



# Listado de series
def lista_series(match_series):
    serie = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in serie:
        url = plugintools.find_single_match(entry, 'href="([^"]+)')
        url = 'http://www.seriesyonkis.sx'+url
        plugintools.log("url= "+url)
        title_serie = plugintools.find_single_match(entry, 'title="([^"]+)').strip()
        plugintools.log("title_serie= "+title_serie)
        if title_serie != "":
            plugintools.log("url_serie= "+url)
            plugintools.add_item(action="serie_capis", title = title_serie, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)    
        

# Paginador de series por letra
def paginador_next(data):    
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
    plugintools.add_item(action="", title= '[COLOR lightyellow][I]Siguiente (Pág. '+str(next)+')[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)    




def seriesmu0(params):
    plugintools.log("SeriesMu_capis "+repr(params))

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = "tvshows"
    elif show == "1":
        show = "seasons"        
    elif show == "2":
        show = "fanart"        
    elif show == "3":
        show = "list"        
    elif show == "4":
        show = "thumbnail"        
    elif show == "5":
        show = "movies"        
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"        
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)      
    
    url = params.get("url")
    referer = 'http://www.series.mu/'
    data = gethttp_referer_headers(url,referer,show)
    plugintools.modo_vista(show)      
    #plugintools.log("data= "+data)
    # ToDo: Card info summary (información de fecha de estreno, temporadas y número de capítulos)
    desc = plugintools.find_single_match(data, '<div class="card media-summary">(.*?)</div>')
    sinopsis = plugintools.find_single_match(desc, '<p>(.*?)</p>')
    datamovie = {}
    datamovie["Plot"]=sinopsis
    cover_match = plugintools.find_single_match(data, '<div class="mini-poster"(.*?)</div>')
    cover = plugintools.find_single_match(cover_match, 'url(.*?);')
    cover = cover.replace("(", "").replace(")", "").strip()
    fanart_match = plugintools.find_single_match(data, '.episode-cover{(.*?)}')    
    plugintools.log("fanart_match= "+fanart_match)    
    fanart_fixed = plugintools.find_single_match(fanart_match, 'background-image:(.*?);')
    fanart_fixed = fanart_fixed.replace("url(", "").replace(")", "").strip()
    title_fixed = plugintools.find_single_match(data, '<h4 class="mini-title">(.*?)<span class')
    genres = plugintools.find_single_match(data, '<span class="mini-genres" >(.*?)</span>')
    genres = genres.strip()
    title_fixed = title_fixed.strip()
    plugintools.log("fanart_fixed= "+fanart_fixed)
    plugintools.log("cover= "+cover)
    plugintools.log("sinopsis= "+sinopsis)
    plugintools.add_item(action="", title='[COLOR blue][B]Series.Mu / [/B][/COLOR][COLOR orange][B]'+title_fixed+'[/B][/COLOR] [COLOR lightgreen][I]['+genres+'][/COLOR][/I]', url = "", info_labels = datamovie , page = fanart_fixed , thumbnail = cover , fanart = fanart_fixed, folder = True, plot = sinopsis , isPlayable = False)

    match_temporadas = plugintools.find_single_match(data, '<div class="chapters chapters-seasons">(.*?)</ul>')
    match_episodios = plugintools.find_single_match(data, '<ul(.*?)</ul>')
    temps = plugintools.find_multiple_matches(match_temporadas, '<i class=icon-angle-down>(.*?)</li>')
    
    i = 1
    for entry in temps:
        label_temp = 'temp='+str(i)
        plugintools.log("label_temp= "+label_temp)
        match_capis = plugintools.find_multiple_matches(data, '<ul '+label_temp+'>(.*?)</ul>')
        plugintools.add_item(action="seriesmu_capis", title='[COLOR lightyellow]Temporada '+str(i)+'[/COLOR]', url = "", info_labels = datamovie , page = fanart_fixed , thumbnail = cover , fanart = fanart_fixed, folder = True, plot = sinopsis , isPlayable = False)
        j=1
        for matches in match_capis:
            plugintools.log("match_capis= "+matches)
            capis = plugintools.find_multiple_matches(matches, '<li>(.*?)</i>')
            for entri in capis:
                plugintools.log("entri= "+entri)
                title_capi = plugintools.find_single_match(entri, '</span>(.*?)</a>')
                url_capi = plugintools.find_single_match(entri, '<a href=(.*?)><span>')
                url_capi = 'http://series.mu'+url_capi+'/'
                plugintools.log("url_capi= "+url_capi)
                if j <= 9:
                    j = "0"+str(j)
                plugintools.add_item(action="enlacesmu", title=str(i)+'x'+str(j)+' '+title_capi, url = url_capi, info_labels = datamovie , page = fanart_fixed , plot = sinopsis , thumbnail = cover , fanart = fanart_fixed , folder = True, isPlayable = False)
                j = int(j) + 1
        
        i = i + 1

    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)          


def enlacesmu(params):
    plugintools.log("getlinksmu: "+repr(params))

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = "tvshows"
    elif show == "1":
        show = "seasons"        
    elif show == "2":
        show = "fanart"        
    elif show == "3":
        show = "list"        
    elif show == "4":
        show = "thumbnail"        
    elif show == "5":
        show = "movies"        
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"        
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)

    sinopsis = params.get("plot")
    datamovie={}
    datamovie["Plot"]=sinopsis

    fanart_fixed = params.get("page")

    loginmu()
    plugintools.modo_vista(show)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    referer = 'http://www.series.mu/'
    data = scrapertools.cache_page(url, referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, '<div class="sections episode-links online shown">(.*?)<div class="sections episode-links download">')
    capis = plugintools.find_multiple_matches(matches, '<div class="link-row">(.*?)</a>')
    for entry in capis:
        plugintools.log("entry= "+entry)
        lang_audio = plugintools.find_single_match(entry, '<div class="lang audio">(.*?)</div>')
        lang_sub = plugintools.find_single_match(entry, '<div class="lang sub">(.*?)</div>')
        url_link = plugintools.find_single_match(entry, '<a href=(.*?)target')
        url_link = url_link.replace('"',"").strip()
        url_link = 'http://series.mu'+url_link
        host = plugintools.find_single_match(entry, '<div class="host ([^"]+)')
        if host == "streamcloudeu":
            if lang_sub != "":
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Streamcloud][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
            else:
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Streamcloud][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'                
            plugintools.add_item(action="getlinkmu", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
        elif host == "vidspotnet":
            if lang_sub != "":
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Vidspot][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
            else:
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Vidspot][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
            plugintools.add_item(action="getlinkmu", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
        elif host == "allmyvideosnet":
            if lang_sub != "":
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Allmyvideos][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
            else:
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Allmyvideos][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'            
            plugintools.add_item(action="getlinkmu", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
        elif host == "playedto":
            if lang_sub != "":
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Played.to][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
            else:
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Played.to][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
            plugintools.add_item(action="getlinkmu", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
        if host == "nowvideosx":
            if lang_sub != "":
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Nowvideo.sx][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
            else:
                title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Nowvideo.sx][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
            plugintools.add_item(action="getlinkmu", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
        else:
            url_link = getotherhost(url_link,show)
            if url.find("veehd") >= 0:
                server = "VeeHD"
                if lang_sub != "":
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
                else:
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
                plugintools.add_item(action="veehd", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
            if url.find("streamin.to") >= 0:
                server = "streamin.to"
                if lang_sub != "":
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
                else:
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
                plugintools.add_item(action="streaminto", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
            if url.find("vk") >= 0:
                server = "Vk"
                if lang_sub != "":
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
                else:
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
                plugintools.add_item(action="vk", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
            if url.find("Tumi") >= 0:
                server = "Tumi"
                if lang_sub != "":
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'] ['+lang_sub+'][/I][/COLOR]'
                else:
                    title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I]['+server+'][/I][/COLOR] [COLOR lightgreen][I]['+lang_audio+'][/I][/COLOR]'
                plugintools.add_item(action="tumi", title = title_fixed, url = url_link , info_labels = datamovie , thumbnail = thumbnail , page = fanart_fixed , fanart = fanart_fixed , folder = False, isPlayable = True)
            
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show) 


def getotherhost(url,show):
    plugintools.log("GetlinkMu "+url)  # pendiente de crear función getotherlinkmu para servidores no conocidos (hay que extraer url)

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = "tvshows"
    elif show == "1":
        show = "seasons"        
    elif show == "2":
        show = "fanart"        
    elif show == "3":
        show = "list"        
    elif show == "4":
        show = "thumbnail"        
    elif show == "5":
        show = "movies"        
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"        
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)   

    data = scrapertools.get_header_from_response(url, header_to_get="location")
    plugintools.log("data= "+data)
    data = data.split(" ")
    url = data[0].strip()
    plugintools.log("url final a devolver= "+url)
    return url

    plugintools.log("show= "+show)            
    plugintools.modo_vista(show) 



def getlinkmu(params):
    plugintools.log("GetlinkMu "+repr(params))  # pendiente de crear función getotherlinkmu para servidores no conocidos (hay que extraer url)

    loginmu()
    url = params.get("url")

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = "tvshows"
    elif show == "1":
        show = "seasons"        
    elif show == "2":
        show = "fanart"        
    elif show == "3":
        show = "list"        
    elif show == "4":
        show = "thumbnail"        
    elif show == "5":
        show = "movies"        
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"
    params["page"]=show
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)     

    # Iniciamos petición de URL que contiene enlaces al capítulo...
    data = scrapertools.get_header_from_response(url, header_to_get="location")
    plugintools.log("data= "+data)
    data = data.split(" ")
    url = data[0].strip()
    plugintools.log("url final= "+url)
    plugintools.log("url= "+url)
    from resources.tools.resolvers import *
    if url.find("allmyvideos")  >= 0:
        plugintools.get_params()
        url = url.replace("http://allmyvideos.net", "http://www.allmyvideos.net").strip()
        params["url"]=url
        allmyvideos(params)
    elif url.find("streamcloud")  >= 0:
        plugintools.get_params()
        params["url"]=url        
        streamcloud(params)
    elif url.find("nowvideo.sx")  >= 0:
        plugintools.get_params()
        url = url.replace("http://nowvideo.sx", "http://www.nowvideo.sx").strip()
        params["url"]=url        
        nowvideo(params)
    elif url.find("vidspot") >= 0:
        plugintools.get_params()
        url = url.replace("http://vidspot.net", "http://www.vidpot.net").strip()
        params["url"]=url        
        vidspot(params)
    elif url.find("playedto") >= 0:
        plugintools.get_params()
        params["url"]=url        
        playedto(params)


    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)         
        

    
        
    
def loginmu():
    show = plugintools.get_setting("series_id")
    if show is "6":
        show = "tvshows"
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
    
    # Iniciamos login...
    url = 'http://series.mu/login/'
    post = 'user='+plugintools.get_setting("seriesmu_user")+'&pass='+plugintools.get_setting("seriesmu_pwd")
    data = scrapertools.cache_page(url, post=post)
            
       

def gethttp_referer_headers(url,referer,show):
    plugintools.log("beta.1-0.3.0.gethttp_referer_headers ")

    show = plugintools.get_setting("series_id")  # Obtenemos modo de vista del usuario para series TV
    if show is None:
        show = "tvshows"
    elif show == "1":
        show = "seasons"        
    elif show == "2":
        show = "fanart"        
    elif show == "3":
        show = "list"        
    elif show == "4":
        show = "thumbnail"        
    elif show == "5":
        show = "movies"        
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"        
    plugintools.log("show= "+show)            
    plugintools.modo_vista(show)
        
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body

