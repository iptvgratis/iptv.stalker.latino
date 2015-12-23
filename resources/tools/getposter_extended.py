# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 GetPoster (módulo de descarga de posters de películas)
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

# TODO:
# Crear botones de paginación y función de lectura de resultados por páginas: getresults(url)
# Mostrar un multilink con las páginas de resultados. El botón tendría de título: "Ir a la página..."
# Buscar alguna forma (si es posible) de mostrar los thumbnails
# Eliminar logs


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




def getposter(title):
    plugintools.log("[Arena+].GetPoster "+title)

    datamovie = []
    title = title.lower().strip().replace(" ", "+")
    url = 'http://m.imdb.com/find?q='+title
    referer= 'http://www.imdb.com/'
    data = gethttp_referer_headers(url, referer)
    
    match_movie = plugintools.find_single_match(data, '<div class="title">(.*?)</div>')
    movie_url = plugintools.find_single_match(match_movie, '<a href="([^"]+)')
    movie_url = 'http://www.imdb.com/'+movie_url
    body = gethttp_referer_headers(movie_url,referer)
    
    poster = plugintools.find_single_match(body, '<link rel=\'image_src\' href="([^"]+)')
    poster = poster.strip()
    movie_title = plugintools.find_single_match(body, '<meta property=\'og:title\' content="([^"]+)')
    movie_title = movie_title.split("(")
    print movie_title
    try:
        if len(movie_title) >= 2:
            title = movie_title[0].strip()
            datamovie.append(title)
            year = movie_title[1].replace(")", "").strip()
            datamovie.append(year)
        else:
            return -1
    except:
        pass
        
    duration = plugintools.find_single_match(body, '<time itemprop="duration"(.*?)</time>')
    duration = duration.split(">")
    if len(duration) >= 2:
        duration = duration[1].strip()
        
    genres = plugintools.find_multiple_matches(body, '<span class="itemprop" itemprop="genre">(.*?)</span>')
    str_generos = ""
    for entry in genres:
        plugintools.log("entry= "+entry)
        # Pasar el género por una función de traducción inglés -> español
        str_generos = str_generos + ' ' + entry
    str_generos = str_generos.strip()
    str_generos = str_generos.replace(" ", ", ")

    rank = plugintools.find_single_match(body, '<div class="titlePageSprite star-box-giga-star">(.*?)</div>')
    rank = rank.strip()
    
    datamovie.append(str_generos)    
    datamovie.append(duration)
    datamovie.append(rank)
    datamovie.append(poster)
    
    #plugintools.add_item(action="", title = '[COLOR lightyellow][B]'+title+' ('+year+') - [/B][I][/COLOR][COLOR grey]'+str_generos+'[/I][/COLOR] [COLOR lightgreen] '+duration+' [/COLOR][COLOR orange][IMDB: [B]'+rank+'[/B]][/COLOR]' , url="", thumbnail = poster , fanart = poster, folder=False, isPlayable=False)

    return datamovie
    

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body


