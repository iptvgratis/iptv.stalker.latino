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

from __main__ import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


temp = xbmc.translatePath(os.path.join('special://home/userdata/playlists/tmp', ''))


def getposter(title):
    plugintools.log("GetPoster "+title)

    try:
        datamovie = {}
        title = title.lower().strip().replace(" ", "+")
        url = 'http://m.imdb.com/find?q='+title
        referer= 'http://m.imdb.com/'
        data = gethttp_referer_headers(url, referer)
        match_movie = plugintools.find_single_match(data, '<div class="title">(.*?)</div>')
        movie_url = plugintools.find_single_match(match_movie, '<a href="([^"]+)')
        movie_url = 'http://m.imdb.com/'+movie_url
        body = gethttp_referer_headers(movie_url,referer)
        poster_url = plugintools.find_single_match(body, '<link rel=\'image_src\' href="([^"]+)')
        datamovie["Poster"] = poster_url.strip()
    except:
        datamovie["Poster"] = ""

    try:
        duration = plugintools.find_single_match(body, '<time itemprop="duration"(.*?)</time>')
        duration = duration.split(">")
        if len(duration) >= 2:
            duration = duration[1].strip()
        datamovie["Duration"] = duration
    except:
        datamovie["Duration"] = "N/D"

    try:
        # Año
        if len(movie_title) >= 2:
            #title = movie_title[0].strip()
            datamovie["Year"] = movie_title[1].replace(")", "").strip()
    except:
        datamovie["Year"] = "N/D"

    try:
        movie_title = plugintools.find_single_match(body, '<meta property=\'og:title\' content="([^"]+)')
        movie_title = movie_title.split("(")
    except:
        movie_title = title
        datamovie["Title"] = ""
    try:
        datamovie["Rating"] = plugintools.find_single_match(body, '<span class="inline-block text-left vertically-middle">(.*?)<')
        datamovie["Rating"] = datamovie["Rating"].strip()
    except:
        datamovie["Rating"] = ""

    themoviedb(title, datamovie)
    return datamovie

'''
    try:
        # Géneros de la película
        genres = plugintools.find_multiple_matches(body, '<span class="itemprop" itemprop="genre">(.*?)</span>')
        str_generos = ""
        for entry in genres:
            plugintools.log("entry= "+entry)
            # TODO: Pasar el género por una función de traducción inglés -> español
            str_generos = str_generos + ' ' + entry
        str_generos = str_generos.strip()
        datamovie["Genre"] = str_generos.replace(" ", ", ")
    except:
        datamovie["Genre"] = ""

    try:
        # Director y escritor(es)
        datamovie["Director"] = plugintools.find_multiple_matches(body, '<h3 class="inline-block"><span itemprop="name">Director:</h3>(.*?)</span>')
        datamovie["Director"] = datamovie["Director"][0].replace('<span itemprop="name">', "").replace("</span>", "").replace("</span>", "").replace("\\n", "").strip()
        datamovie["Writer"] = plugintools.find_multiple_matches(body, '<h3 class="inline-block"><span itemprop="name">Writers:</h3>(.*?)</span>')
        datamovie["Writer"] = datamovie["Writer"][0].replace('<span itemprop="name">', "").replace("</span>", "").replace("</span>", "").replace("\\n", "").strip()
    except:
        datamovie["Director"] = "N/D"
        datamovie["Writer"] = "N/D"


    return datamovie

'''



def save_title(title, datamovie, filename):
    plugintools.log("Arena+ Saving data... "+repr(datamovie))

    # Comprobamos si no existe el archivo para crearlo
    if not os.path.isfile(temp + filename):
        plugintools.log("Creando archivo... temp/"+filename)
        imdb_file = open(temp + filename, "a")
        imdb_file.seek(0)
        imdb_file.write('#EXTM3U,movies\n\n')  # Fijamos modo de vista para la lista de películas
        imdb_file.close()
        print "Archivo creado correctamente!"
    else:
        pass    

    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    title = title.strip()
    #poster_url = datamovie["Poster"]
    #print 'Rating',datamovie["Rating"]
    #print 'Duration',datamovie["Duration"]
    #print 'Year',datamovie["Year"]
    #print 'Director',datamovie["Director"]
    #print 'Writer',datamovie["Writer"]
    imdb_file.write('#EXTINF:-1,'+title+',tvg-logo="'+datamovie["Poster"]+'",tvg-wall="'+datamovie["Fanart"]+'",imdb="'+datamovie["Rating"]+'",genre="'+datamovie["Genre"]+'",votes="'+datamovie["Votes"]+'",time="'+str(datamovie["Duration"])+'",year="'+datamovie["Year"]+'",dir="'+datamovie["Director"]+'",wri="'+datamovie["Writer"]+'",plot="'+datamovie["Plot"]+'"\n')
    imdb_file.close()


def save_url(url, filename):
    plugintools.log("Arena+ Saving URL...")
    
    # Abrimos archivo para guardar datos de película
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n\n')
    imdb_file.close()


def save_multilink(url, filename):
    plugintools.log("Arena+ Saving URL...")

    # Abrimos archivo para guardar datos de pelÃ­cula
    plugintools.log("Abriendo archivo... temp/"+filename)
    imdb_file = open(temp + filename, "a")
    imdb_file.write(url+'\n')
    imdb_file.close()


def themoviedb(title, datamovie):
    plugintools.log("The Movie Database: "+title)

    try:
        url = 'https://www.themoviedb.org/search?query='+title
        plugintools.log("URL= "+url)
        referer = 'https://www.themoviedb.org/'
        data = gethttp_referer_headers(url,referer)
        #plugintools.log("data= "+data)
        matches = plugintools.find_single_match(data, '<ul class="search_results movie">(.*?)</ul>')
        title_film = plugintools.find_single_match(matches, 'title="([^"]+)')
        plugintools.log("title_film= "+title_film)
        url_film = plugintools.find_single_match(matches, '<a href="([^"]+)')
        url_film = 'https://www.themoviedb.org'+url_film+'?language=es'
        url_film = url_film.strip()
        plugintools.log("url_film= "+url_film)
        year_film = plugintools.find_single_match(matches, '<span>(.*?)</span>')
        year_film = year_film.replace("(", "").replace(")", "").strip()
        datamovie["Year"] = year_film
        plugintools.log("year_film= "+year_film)
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
        request_headers.append(["Referer", referer])
        body,response_headers = plugintools.read_body_and_headers(url_film, headers=request_headers)
        #plugintools.log("body= "+body)
        sinopsis = plugintools.find_single_match(body, 'itemprop="description">(.*?)</p>')
        sinopsis = sinopsis.replace('"', "")
        datamovie["Plot"]=sinopsis
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
        rating = plugintools.find_single_match(body, '<span itemprop="ratingValue" id="rating_hint">(.*?)</span>')
        datamovie["Rating"]=rating
        votes = plugintools.find_single_match(body, '<span itemprop="ratingCount">(.*?)</span>')
        datamovie["Votes"]=votes

    except:
        pass

def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    #plugintools.log("body= "+body)
    return body
