# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Youtube Playlist para Arena+
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

import plugintools

home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arenapremium/', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.arenapremium/art', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'

'''
Endpoints Youtube addon by Bromix
Play a video: plugin://plugin.video.youtube/play/?video_id=[VID]
Show videos of a playlist: plugin://plugin.video.youtube/playlist/[PID]/
Play a playlist in a predetermined order: plugin://plugin.video.youtube/play/?playlist_id=[PID]&order=[default|reverse|shuffle]
Navigate to a channel via ID: plugin://plugin.video.youtube/channel/[CID]/
Navigate to a channel via username: plugin://plugin.video.youtube/user/[NAME]/
Search: plugin://plugin.video.youtube/search/?q=[URL_ENCODED_TEXT]
'''


def yt_playlist(params):
    
    url = params.get("url")
    i = 1

    data = gethttp_headers(params)
    plugintools.log("data= "+data)
    url = data.strip()

    # Cargamos función de encabezado del playlist
    title_header = ""
    title_header = header_pl(data, title_header)

    # Cargamos botón de página siguiente (+100 vídeos)
    load_more = plugintools.find_single_match(data, 'data-uix-load-more-href="([^"]+)')
    load_more = 'https://www.youtube.com/'+load_more
    plugintools.log("load_more= "+load_more)
    plugintools.add_item(action="load_more_vids", title = "[COLOR lightyellow]Cargar más...[/COLOR]", url = load_more, extra = str(i), page = title_header , folder=True, isPlayable=False)    
    
    i = 1
    canal = plugintools.find_multiple_matches(data, '<tr class="pl-video yt-uix-tile(.*?)</span>')
    for entry in canal:
        plugintools.log("Núm. "+str(i))
        plugintools.log("Canal= "+entry)
        vid_title = plugintools.find_single_match(entry, 'data-title="([^"]+)')
        vid_title = parsing_yt(vid_title)
        plugintools.log("URL= "+vid_title)
        vid_url = plugintools.find_single_match(entry, 'data-video-id="([^"]+)').strip()        
        vid_url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + vid_url
        vid_url = vid_url.strip()
        plugintools.log("URL= "+vid_url)        
        vid_thumb = plugintools.find_single_match(entry, 'src="(.*?)"')
        vid_thumb = 'https:'+vid_thumb
        vid_thumb = vid_thumb.replace("vi_webp", "vi")
        vid_thumb = vid_thumb.replace("default.webp", "default.jpg")
        plugintools.log("thumbnail= "+vid_thumb)
        fanart = art+'youtube.png'
        plugintools.add_item(action="play", title=str(i)+'. '+vid_title+ ' [COLOR white][[COLOR red]You[COLOR white]tube Video][/COLOR]', url=vid_url, thumbnail = vid_thumb, fanart=fanart, folder=False, isPlayable=True)
        i = i + 1


# Petición de la URL
def load_more_vids(params):
    plugintools.log("arena+.gethttp_headers "+repr(params))

    url = params.get("url")
    i=params.get("extra")
    title_header = params.get("page")
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",'http://www.digitele.com/pluginfiles/canales/'])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    body = body.replace('\u003c', '<')
    body = body.replace('\u003e', '>')
    body = body.replace('\u003a', ':')
    body = body.replace('\u003b', ';')
    body = body.replace('\u003d', '=')
    body = body.replace('\u003f', '?')
    body = body.replace('\u002f', '/')
    body = body.replace('\u002e', '.')
    body = body.replace('\u002d', '-')
    body = body.replace('\u002c', ',')
    body = body.replace('\u0026', '&')
    body = body.replace('\u0023', '#')
    body = body.replace('\u0020', ' ')
    body = body.replace('\u00e1', 'á')
    body = body.replace('\u00e0', 'á')
    body = body.replace('\u00e9', 'é')
    body = body.replace('\u00a1', '¡')
    body = body.replace('\u00d1', 'ñ')
    body = body.replace('\u00f1', 'ñ')
    body = body.replace('&#39', 'á')
    body = body.replace('\u00fa', 'ú')
    body = body.replace('\u00c1', 'Á')
    body = body.replace('\u00ed', 'í')
    body = body.replace('\u00cd', 'Í')
    body = body.replace('\u00eb', 'ë')
    #plugintools.log("body= "+body)

    title_header = header_pl(body, title_header)

    # Comprobamos si hay más vídeos en el playlist que no ha mostrado Youtube
    load_more = plugintools.find_single_match(body, 'data-uix-load-more-href="([^"]+)')
    load_more_2 = plugintools.find_single_match(body, 'data-uix-load-more-href=\"|/(.*?)data-uix-load-more-target-id')
    plugintools.log("load_more= "+load_more)
    plugintools.log("load_more_2= "+load_more_2)
    if load_more != "":
        load_more_fixed = 'https://www.youtube.com/'+load_more
        plugintools.log("load_more= "+load_more_fixed)
        i = 200
        plugintools.add_item(action="load_more_vids", title = "[COLOR lightyellow]Cargar más...[/COLOR]", url = load_more_fixed, extra = str(i), page = title_header , folder=True, isPlayable=False)

    elif load_more_2 != "":
        load_more_fixed = 'https://www.youtube.com/'+load_more_2
        plugintools.log("load_more= "+load_more_fixed)
        i = 100
        plugintools.add_item(action="load_more_vids", title = "[COLOR lightyellow]Cargar más...[/COLOR]", url = load_more_fixed, extra = str(i), page = title_header , folder=True, isPlayable=False)
    else:
        i = 101
        
        

        

    # Vamos a mostrar los videos...        
    matches = plugintools.find_multiple_matches(body, '<tr(.*?)tr>')
    for entry in matches:
        vid_title = plugintools.find_single_match(entry, 'data-title(.*?)data-video-id')
        vid_title = vid_title.replace("data-set-video-id", "").replace('=\\"', "").replace('\\"', "").replace("&quot;",'"').strip()
        title_fixed = vid_title.split(">")
        if len(title_fixed) >= 2:
            vid_title = title_fixed[0]
            vid_title = vid_title.replace("&quot;", '"')
        vid_url = plugintools.find_single_match(entry, 'data-video-id(.*?)">')
        vid_url = vid_url.replace('=\\"', "")
        vid_url_fixed = vid_url.split('\\')
        if len(vid_url_fixed) >= 2:
            vid_url = vid_url_fixed[0]
        vid_url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + vid_url
        #plugintools.log("vid_url= "+vid_url)
        vid_thumb = plugintools.find_single_match(entry, 'src(.*?)width')
        vid_thumb = vid_thumb.replace("\\/", "/")
        vid_thumb = vid_thumb.replace('=\\"', "")
        vid_thumb = vid_thumb.replace('\\"', "")
        vid_thumb = vid_thumb.replace('//', "")
        vid_thumb = vid_thumb.replace('.webp', ".jpg")
        vid_thumb = 'http://'+vid_thumb
        i = int(i) + 1
        print i
        plugintools.add_item(action="play", title=str(i)+'. '+vid_title+ ' [COLOR white][[COLOR red]You[COLOR white]tube Video][/COLOR]', url=vid_url, thumbnail = vid_thumb, fanart=art+'youtube.png', folder=False, isPlayable=True)
    
    
    
# Petición de la URL
def gethttp_headers(params):
    plugintools.log("arena+.gethttp_headers "+repr(params))

    url = params.get("url")
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",'http://www.digitele.com/pluginfiles/canales/'])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    #plugintools.log("body= "+body)
    return body



def parsing_yt(vid_title):
    
    vid_title = vid_title.replace("&quot;", '"')
    vid_title = vid_title.replace("&#39;", "'")
    
    return vid_title


def header_pl(data, title_header):
    # Mostramos encabezado
    header = plugintools.find_single_match(data, '<div id="pl-header"(.*?)</ul>')
    #plugintools.log("header= "+header)
    title = plugintools.find_single_match(header, '<h1 class="pl-header-title">(.*?)</h1>').strip()
    plugintools.log("title= "+title)
    pl_name = plugintools.find_single_match(header, 'data-name="">(.*?)</a>').strip()
    hits = plugintools.find_multiple_matches(header, '<li>(.*?)</li>')
    hit_list = []
    for entry in hits:
        #plugintools.log("hit= "+entry)
        hit_list.append(entry)

    if title == "":
        plugintools.add_item(action="", title = title_header, url = "", folder=False, isPlayable=False)
        return title_header       
    else:
        try:
            title_header = '[COLOR orange][B]'+title+'[/B][I][COLOR white] '+hit_list[1]+' [COLOR lightyellow]'+hit_list[2]+'[/I][/COLOR]'
            plugintools.add_item(action="", title = title_header, url = "", folder=False, isPlayable=False)
            return title_header
        except:
            title_header = '[COLOR orange][B]'+title+'[/B][I][COLOR white] '+hit_list[1]+' [/I][/COLOR]'
            plugintools.add_item(action="", title = title_header, url = "", folder=False, isPlayable=False)
            return title_header            
            
        
      

    
        
    
        

        




