# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Parser de SeriesFLV.com
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
import plugintools

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'
referer = 'http://www.seriesflv.com/'


def seriesflv(params):
    plugintools.log("[beta.1 0.3.0].SeriesFLV")

    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        plugintools.log("show= "+show)
    
    url = params.get("url")           

    datamovie = {}
    datamovie["Plot"]=params.get("plot")  # Sinopsis

    # Vamos a capturar las categorías de capítulos: Sub, esp, lat y en (original, en inglés)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]Subtitulada[/COLOR]' , url = url, thumbnail = thumbnail , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]Español[/COLOR]' , url = url, thumbnail = thumbnail , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]Latino[/COLOR]' , url = url, thumbnail = thumbnail , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]V.O.[/COLOR]' , url = url, thumbnail = thumbnail , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
    #categorias_flv(data,show)    



def categorias_flv(data,show):
    plugintools.log("[Arena+ 0.3.4] SeriesFLV Categorias ")

    plugintools.modo_vista(show)
    plugintools.log("show= "+show)    

    params = plugintools.get_params()
    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis      
    
    sections = plugintools.find_single_match(data, '<div class="lang over font2 bold">(.*?)</div>')
    plugintools.log("sections= "+sections)
    tipo_selected = plugintools.find_single_match(sections, 'class="select">(.*?)</a>')
    plugintools.add_item(action="listado_seriesflv", title='[COLOR orange]Listado completo[/COLOR]' , url = "http://www.seriesflv.net/series/", extra = data , info_labels = datamovie , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    plugintools.add_item(action="lista_chapters", title='[COLOR orange]'+tipo_selected+'[/COLOR]' , url = "", extra = data , info_labels = datamovie , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    tipos = plugintools.find_multiple_matches(sections, ';">(.*?)</a>')
    for entry in tipos:
        plugintools.add_item(action="lista_chapters", title='[COLOR orange]'+entry+'[/COLOR]' , url = "", thumbnail = thumbnail , extra = data , plot = datamovie["Plot"] , info_labels = datamovie , page = show , fanart = fanart , folder = True, isPlayable = False)
        


def lista_chapters(params):
    plugintools.log("[Arena+ 0.3.4] SeriesFLV Lista_chapters "+repr(params))

    url = params.get("url")
    referer = 'http://www.seriesflv.com/'
    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        plugintools.log("show= "+show)
     
    data = gethttp_referer_headers(url, referer, show)
    #plugintools.log("data= "+data) 

    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis 

    chapters = plugintools.find_multiple_matches(data, '<a href="http://www.seriesflv.net/ver/(.*?)</a>')
    title = params.get("title")
    for entry in chapters:
        if title.find("Subtitulada") >= 0:            
            if entry.find('lang="sub"') >=0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , url = url_chapter , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Español") >= 0:        
            if entry.find('lang="es"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Latino") >= 0:
            if entry.find('lang="la"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

        if title.find("Original") >= 0:  
            if entry.find('lang="en"') >= 0:
                #plugintools.log("entry= "+entry)
                entry_fixed = entry.split('"')
                url_chapter = 'http://www.seriesflv.net/ver/'+entry_fixed[0]
                #plugintools.log("url_chapter= "+url_chapter)
                title_chapter = plugintools.find_single_match(entry, '<div class="i-title">(.*?)</div>')
                #plugintools.log("title_chapter= "+title_chapter)
                num_chapter = plugintools.find_single_match(entry, '<div class="box-tc">(.*?)</div>')
                #plugintools.log("núm. capítulo= "+num_chapter)
                i_time = plugintools.find_single_match(entry, '<div class="i-time">(.*?)</div>')
                #plugintools.log("desde hace= "+i_time)
                plugintools.add_item(action="chapter_urls", title='[COLOR orange]'+num_chapter+'[/COLOR]'+'  [COLOR lightyellow][B]'+title_chapter+'[/B][/COLOR][COLOR lightgreen][I] ('+i_time+')[/I][/COLOR]' , url = url_chapter , info_labels = datamovie , plot = datamovie["Plot"] , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)                



def chapter_urls(params):
    plugintools.log("[%s %s] Seriesflv regex... %s " % (addonName, addonVersion, repr(params)))
    
    show = params.get("page")
    plugintools.modo_vista(show)
    plugintools.log("show= "+show)    

    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    datamovie = {}
    datamovie["Plot"]=params.get("plot")
    
    url = params.get("url")
    title = params.get("title")
    title_fixed = title.split("(")
    if len(title_fixed) >= 2:
        title_fixed = title_fixed[0].strip()
    else:
        title_fixed = title_fixed[0].strip()
    data = gethttp_referer_headers(url, referer, show)
    thumbnail = plugintools.find_single_match(data, '<meta property="og:image" content="(.*?)"/>')
    if thumbnail == "":
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'

    plugintools.add_item(action="", title='[COLOR gold][B]'+title+'[/B][/COLOR]' , url = "" , info_labels = datamovie , extra = show , page = show , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
    
    match_urls = plugintools.find_single_match(data, '<div id="enlaces">(.*?)</table>')
    #plugintools.log("match_urls= "+match_urls)
    block_url = plugintools.find_multiple_matches(match_urls, '<tr>(.*?)</tr>')
    for entry in block_url:
        
        # Localizamos el idioma del audio (o subtítulos)
        if entry.find("http://www.seriesflv.net/images/lang/es.png") >= 0:
            lang = "[Castellano]"
        elif entry.find("http://www.seriesflv.net/images/lang/sub.png") >= 0:
            lang = "[Subtitulado]"
        elif entry.find("http://www.seriesflv.net/images/lang/en.png") >= 0:
            lang = "[English]"
        elif entry.find("http://www.seriesflv.net/images/lang/lat.png") >= 0:
            lang = "[Latino]"
        else:
            lang = "[Castellano]"
            
        #plugintools.log("block_url= "+entry)
        server_name = plugintools.find_single_match(entry, '<td width="134" style="text-align:left;" class="e_server"><img width="16" src="([^"]+)"')
        server_name = server_name.split("domain=")
        if len(server_name) >= 2:
            server_name = server_name[1].strip()            
            #plugintools.log("server_name= "+server_name)
            print title_fixed
            url = plugintools.find_single_match(entry, '<td width="84"><a href="([^"]+)"')
            url = getlinkflv(url,show)
            plugintools.modo_vista(show)
            plugintools.log("url= "+url)
            if url == "": pass
            else:
                if url.find("allmyvideos") >= 0:
                    server_url = "[COLOR lightgreen][I][allmyvideos][/I][/COLOR]"
                    plugintools.add_item(action="allmyvideos", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("vidspot") >= 0:
                    server_url = "[COLOR lightgreen][I][vidspot][/I][/COLOR]"
                    plugintools.add_item(action="vidspot", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("played.to") >= 0:
                    server_url = "[COLOR lightgreen][I][played.to][/I][/COLOR]"
                    plugintools.add_item(action="playedto", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("nowvideo") >= 0:
                    server_url = "[COLOR lightgreen][I][nowvideo][/I][/COLOR]"
                    plugintools.add_item(action="nowvideo", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("streamin.to") >= 0:
                    server_url = "[COLOR lightgreen][I][streamin.to][/I][/COLOR]"
                    plugintools.add_item(action="streaminto", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("vk") >= 0:
                    server_url = "[COLOR lightgreen][I][vk][/I][/COLOR]"
                    plugintools.add_item(action="vk", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("tumi") >= 0:
                    server_url = "[COLOR lightgreen][I][tumi][/I][/COLOR]"
                    plugintools.add_item(action="tumi", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("streamcloud") >= 0:
                    server_url = "[COLOR lightgreen][I][streamcloud][/I][/COLOR]"
                    plugintools.add_item(action="streamcloud", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("veehd") >= 0:
                    server_url = "[COLOR lightgreen][I][veehd][/I][/COLOR]"
                    plugintools.add_item(action="veehd", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("novamov") >= 0:
                    server_url = "[COLOR lightgreen][I][novamov][/I][/COLOR]"
                    plugintools.add_item(action="novamov", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("moevideos") >= 0:
                    server_url = "[COLOR lightgreen][I][moevideos][/I][/COLOR]"
                    plugintools.add_item(action="moevideos", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("movshare") >= 0:
                    server_url = "[COLOR lightgreen][I][movshare][/I][/COLOR]"
                    plugintools.add_item(action="movshare", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)
                elif url.find("movreel") >= 0:
                    server_url = "[COLOR lightgreen][I][movreel][/I][/COLOR]"
                    plugintools.add_item(action="movshare", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)                    
                elif url.find("videobam") >= 0:
                    server_url = "[COLOR lightgreen][I][videobam][/I][/COLOR]"
                    plugintools.add_item(action="videobam", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)             
                elif url.find("gamovideo") >= 0:
                    server_url = "[COLOR lightgreen][I][gamovideo][/I][/COLOR]"
                    plugintools.add_item(action="gamovideo", title= '[COLOR white]'+title_fixed+' [/COLOR][COLOR lightyellow][I]('+server_name+')[/I][/COLOR]  [COLOR lightgreen][I]'+lang+'[/I][/COLOR]' , url = url, info_labels = datamovie , extra = show , page = show , fanart = fanart , thumbnail = thumbnail , folder = False, isPlayable = True)             
    


def getlinkflv(url,show):
    plugintools.modo_vista(show)
    plugintools.log("show= "+show) 
    data = gethttp_referer_headers(url,referer,show)
    #plugintools.log("data= "+data)
    url = plugintools.find_single_match(data, '<a id="continue" href="([^"]+)"')
    return url



def lista_series(params):
    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        plugintools.log("show= "+show)
        
    url = params.get("url")
    plugintools.log("url= "+url)
    referer = 'http://www.seriesflv.net/'
    data = gethttp_referer_headers(url,referer,show)
    matches = plugintools.find_single_match(data, '<ul id="list_series_letras"(.*?)</ul>')
    series = plugintools.find_multiple_matches(matches, '<li class=(.*?)</li>')
    for entry in series:
        title_serie = plugintools.find_single_match(entry, 'title="([^"]+)')
        title_serie = title_serie.replace("Online HD", "")
        plugintools.log("title_serie= "+title_serie)
        url_serie = plugintools.find_single_match(entry, 'href="([^"]+)')
        plugintools.log("url_serie= "+url_serie)
        plugintools.add_item(action="lista_capis", title=title_serie, url=url_serie, thumbnail = params.get("thumbnail"), fanart = fanart, folder = True, isPlayable = False)
        

    
def lista_capis(params):
    plugintools.log("[%s %s] Lista capítulos en Seriesflv " % (addonName, addonVersion))

    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        plugintools.log("show= "+show)

    thumbnail = params.get("thumbnail")
    if thumbnail == "":  
        thumbnail = 'http://m1.paperblog.com/i/249/2490697/seriesflv-mejor-alternativa-series-yonkis-L-2whffw.jpeg'
    fanart = 'http://www.nikopik.com/wp-content/uploads/2011/10/S%C3%A9ries-TV.jpg'

    sinopsis = params.get("plot")
    datamovie = {}
    datamovie["Plot"]=sinopsis        
        
    url = params.get("url")
    referer = 'http://www.seriesflv.net/'
    data = gethttp_referer_headers(url,referer,show)

    # Carátula de la serie
    cover = plugintools.find_single_match(data, '<div class="portada">(.*?)</div>')
    thumbnail = plugintools.find_single_match(cover, 'src="([^"]+)')
    
    matches = plugintools.find_multiple_matches(data, '<th class="sape">Capitulos</th>(.*?)</table>')
    for entry in matches:
        capis= plugintools.find_multiple_matches(entry, '<td class="sape">(.*?)</td>')
        for entry in capis:
            title_capi = plugintools.find_single_match(entry, 'class="color4">(.*?)</a>')
            url_capi = plugintools.find_single_match(entry, '<a href="([^"]+)')
            plugintools.add_item(action="chapter_urls", title= title_capi, url= url_capi, info_labels = datamovie , plot = datamovie["Plot"] , page = show , extra = show , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)


def listado_seriesflv(params):
    plugintools.log("Arena+.[listado_seriesflv] "+repr(params))

    show = plugintools.get_setting("series_id")
    if show == "":
        show = "tvshows"
        plugintools.modo_vista(show)
        plugintools.log("show= "+show)
        
    letra = "a"
    url = 'http://www.seriesflv.net/ajax/lista.php?grupo_no=0&type=series&order=b'
    referer = 'hhttp://www.seriesflv.net/series/'
    body = gethttp_referer_headers(url,referer,show)
    plugintools.log("body= "+body)


            

def gethttp_referer_headers(url,referer,show):
    plugintools.log("beta.1-0.3.0.gethttp_referer_headers ")
    plugintools.modo_vista(show)
    plugintools.log("show= "+show)  
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    request_headers.append(["X-Requested-With", "XMLHttpRequest"])
    request_headers.append(["Cookie:","__utma=253162379.286456173.1418323503.1421078750.1422185754.16; __utmz=253162379.1421070671.14.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=http%3A%2F%2Fwww.seriesflv.net%2Fserie%2Fhora-de-aventuras.html; __cfduid=daeed6a2aacaffab2433869fd863162821419890996; __utmb=253162379.4.10.1422185754; __utmc=253162379; __utmt=1"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body

