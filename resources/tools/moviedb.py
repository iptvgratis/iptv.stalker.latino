# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Arena+ MovieDB (módulo de descarga de datos de películas)
# Version 0.1 (02.11.2014)
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

import re,urllib,urllib2,sys
import plugintools,ioncube




def themoviedb(title, datamovie):
    plugintools.log("TMD: "+title)
    
    title_fixed = title.replace(" ", "+")
    plugintools.log("title_fixed= "+title_fixed)
    url = 'https://www.themoviedb.org/search?query='+title_fixed+'?language=es'
    plugintools.log("URL= "+url)
    referer = 'https://www.hemoviedb.org/'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, '<ul class="search_results movie">(.*?)</ul>')
    plugintools.log("matches= "+matches)
    title_film = plugintools.find_single_match(matches, 'title="([^"]+)')
    plugintools.log("title_film= "+title_film)
    url_film = plugintools.find_single_match(matches, '<a href="([^"]+)')
    url_film = 'https://www.themoviedb.org/'+url_film+'?language=es'
    plugintools.log("url_film= "+url_film)
    year_film = plugintools.find_single_match(matches, '<span>(.*?)</span>')
    plugintools.log("year_film= "+year_film)
    body = gethttp_referer_headers(url_film,referer)
    plugintools.log("body= "+body)
    sinopsis = plugintools.find_single_match(body, 'itemprop="description">(.*?)</p>')
    datamovie["Plot"]=sinopsis.replace('"',"'")
    plugintools.log("sinopsis= "+sinopsis)
    crew_match = plugintools.find_single_match(body, '<h3>Crew</h3>(.*?)</table>')
    match_director = plugintools.find_single_match(crew_match, '<td class="job">Director:</td>(.*?)</td>')
    director = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
    directores = ""
    for match in director:
        if directores == "":
            directores = match
        else:
            directores = directores+", "+match
    datamovie["Director"] = directores
    plugintools.log("director(es)= "+directores)        
    match_writers = plugintools.find_single_match(crew_match, '<td class="job">Writers:</td>(.*?)</td>')
    writers = plugintools.find_multiple_matches(match_director, 'itemprop="name">(.*?)</span>')
    guionistas = ""
    for entry in writers:
        if guionistas == "":
            guionistas = entry
        else:
            guionistas = guionistas+", "+entry
    datamovie["Writer"] = guionistas
    plugintools.log("guionista(s)= "+guionistas)        
    backdrop = plugintools.find_single_match(body, '<meta name="twitter:image" content="([^"]+)')
    datamovie["Fanart"]=backdrop
    plugintools.log("backdrop= "+backdrop)
    match_genres = plugintools.find_single_match(body, '<span id="genres">(.*?)</ul>')
    genres_match = plugintools.find_multiple_matches(match_genres, '<span itemprop="genre">(.*?)</span>')
    generos = ""
    for genero in genres_match:
        if generos == "":
            generos = genero
        else:
            generos = generos+", "+genero
    datamovie["Genre"] = generos
    plugintools.log("generos= "+generos)
    

def gethttp_referer_headers(url,referer):    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body


