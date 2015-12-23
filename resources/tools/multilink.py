# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 - Kodi Add-on by Juarrox (juarrox@gmail.com)
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info
#------------------------------------------------------------

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

import plugintools, ioncube

from __main__ import *
from framescrape import *


# Regex de EPG
from resources.tools.epg_miguiatv import *
from resources.tools.epg_ehf import *
from resources.tools.epg_arenasport import *
from resources.tools.epg_formulatv import *

# Regex de canales
from resources.regex.vaughnlive import *
from resources.regex.ninestream import *
from resources.regex.vercosas import *
from resources.regex.castalba import *
from resources.regex.castdos import *
from resources.regex.directwatch import *
from resources.regex.freetvcast import *
from resources.regex.freebroadcast import *
from resources.regex.sawlive import *
from resources.regex.broadcastlive import *
from resources.regex.businessapp import *
from resources.regex.rdmcast import *
from resources.regex.dinozap import *
from resources.regex.streamingfreetv import *
from resources.regex.byetv import *
from resources.regex.ezcast import *
from resources.regex.iguide import *
from resources.regex.janjua import *


# Tools & resolvers
from resources.tools.resolvers import *
from resources.tools.update import *
from resources.tools.updater import *
from resources.tools.resolvers import *
from resources.tools.mundoplus import *
from resources.tools.nstream import *
from resources.tools.bum import *
from resources.tools.yt_playlist import *
from resources.tools.dailymotion import *


playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def get_server(params):
    plugintools.log('[%s %s].get_server %s' % (addonName, addonVersion, repr(params)))

    show = params.get("page")
    if show == "":
        show = "list"            
    plugintools.modo_vista(show)
    
    url = params.get("url")

    if url.startswith("rtmp") == True:
    
        if url.find("iguide.to") >= 0:
            iguide0(params)

        elif url.find("freetvcast.pw") >= 0:
            freetvcast(params)  
                    
        elif url.find("http://privado.streamingfreetv.net") >= 0:
            streamingfreetv0(params)  		

        elif url.find("9stream") >= 0:            
            ninestreams(params)

        elif url.find("freebroadcast") >= 0:
            freebroadcast(params)   

        elif url.find("cast247") >= 0:
            castdos(params)

        elif url.find("castalba") >= 0:
            castalba(params)     

        elif url.find("direct2watch") >= 0:
            directwatch(params)
        
        elif url.find("vaughnlive") >= 0:
            resolve_vaughnlive(params)

        elif url.find("shidurlive") >= 0:
            shidurlive(params)      
    
        elif url.find("vercosas") >= 0:
            vercosasgratis(params)

        elif url.find("businessapp1") >= 0:
            businessapp0(params)            

        elif url.find("pageUrl=http://rdmcast.com") >= 0:
            rdmcast0(params)

        elif url.find("janjua") >= 0:
            janjua0(params)
            
        else:            
            params["url"]=url            
            plugintools.play_resolved_url(url)
        
    elif url.startswith("serie") >= 0:
        if url.find("seriesadicto") >= 0:
            from resources.tools.seriesadicto import *
            seriecatcher(params)
            
        elif url.find("seriesflv") >= 0:
            from resources.tools.seriesflv import *
            lista_capis(params)

        elif url.find("seriesyonkis") >= 0:
            from resources.tools.seriesyonkis import *
            serie_capis(params)

        elif url.find("seriesblanco") >= 0:
            from resources.tools.seriesblanco import *
            seriesblanco0(params)

        elif url.find("seriesmu") >= 0:
            from resources.tools.seriesblanco import *
            seriesmu0(params)            

    elif url.startswith("bum") == True or url.startswith("BUM") == True:
        from resources.tools.bum import *
        url = url.strip()
        title = title.replace(" [COLOR lightyellow][I][BUM+][/COLOR]", "").strip()
        params["title"]=title
        params["url"]=url
        get_server(params)
        bum_multiparser(params)
 
    else:
	plugintools.play_resolved_url(url)




def play_url(url):
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, url))	

    params = plugintools.get_params()
    show = params.get("page")
    if show == "":
        show = "list"
    plugintools.modo_vista(show)
    
    # Notificación de inicio de resolver en caso de enlace RTMP
    url = url.strip()

    if url.startswith("http") == True:
        if url.find("allmyvideos") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            allmyvideos(params)
        elif url.find("streamcloud") >= 0 :
            params["url"]=url
            params["title"]=title
            params = plugintools.get_params() 
            streamcloud(params)
        elif url.find("vidspot") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vidspot(params)
        elif url.find("played.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            playedto(params)
        elif url.find("vk.com") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vk(params)
        elif url.find("nowvideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            nowvideo(params)
        elif url.find("tumi") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)
        elif url.find("streamin.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            streaminto(params)
        elif url.find("veehd") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            veehd(params)
        elif url.find("novamov") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            novamov(params)
        elif url.find("gamovideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            gamovideo(params)
        elif url.find("movshare") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            movshare(params)
        elif url.find("powvideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            powvideo(params)
        elif url.find("mail.ru") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            mailru(params)
        elif url.find("tumi.tv") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)
        elif url.find("videobam") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            videobam(params)            
            
        else:
            url = url.strip()
            plugintools.play_resolved_url(url)

    elif url.startswith("rtp") >= 0:  # Control para enlaces de Movistar TV
        plugintools.play_resolved_url(url)
       
    else:
        plugintools.play_resolved_url(url)


        
       

def url_analyzer(url):
    plugintools.log('[%s %s].URL Analyzer %s' % (addonName, addonVersion, url))	

    params = plugintools.get_params()
    plugintools.log("params = "+repr(params))

    if url == "mundoplus":
        mundoplus_guide(params)
    
    elif url.startswith("goear") == True:
        id_goear = url.replace("goear:", "").replace('"', "").strip()
        url = 'http://www.goear.com/action/sound/get/'+id_goear
        plugintools.log("url= "+url)
        params["url"]=url.strip()
        play_resolved_url(url)
        
    elif url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            from resources.tools.seriesflv import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            params["page"]=show
            plugintools.modo_vista(show)            
            lista_capis(params)
        elif url.find("seriesyonkis") >= 0:
            from resources.tools.seriesyonkis import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)
            serie_capis(params)
        elif url.find("seriesadicto") >= 0:
            from resources.tools.seriesadicto import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriecatcher(params)
        elif url.find("seriesblanco") >= 0:
            from resources.tools.seriesblanco import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriesblanco0(params)
        elif url.find("series.mu") >= 0:
            from resources.tools.seriesmu import *
            url = url.replace("serie:", "")
            show = plugintools.get_setting("series_id")
            params = plugintools.get_params()
            params["page"]=show            
            params["url"]=url.strip()
            plugintools.modo_vista(show)            
            seriesmu0(params)

    elif url.startswith("rtmp") == True or url.startswith("rtsp") == True:
        params = plugintools.get_params()
        title = params.get("title")
        title = title + ' [rtmp]'
        params["title"]=title
        show = params.get("page")
        url = parse_url(url, show)
        params = plugintools.get_params()
        params["url"]=url
        get_server(params)            
        
    elif url.startswith("http") == True:        
        if url.find("allmyvideos") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            allmyvideos(params)

        elif url.find("streamcloud") >= 0:                        
            params = plugintools.get_params()
            params["url"]=url
            streamcloud(params)

        elif url.find("vidspot") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            vidspot(params)

        elif url.find("played.to") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            playedto(params)       

        elif url.find("vk.com") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            vk(params)

        elif url.find("nowvideo") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            nowvideo(params)          
        
        elif url.find("tumi.tv") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)

        elif url.find("streamin.to") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            streaminto(params)
            
        elif url.find("veehd") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            veehd(params)

        elif url.find("novamov") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            novamov(params)       

        elif url.find("gamovideo") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            gamovideo(params)

        elif url.find("moevideos") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            moevideos(params)

        elif url.find("movshare") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            movshare(params)              
        
        elif url.find("powvideo") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            powvideo(params)

        elif url.find("mail.ru") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            mailru(params)
            
        elif url.find("videobam") >= 0:
            params = plugintools.get_params()
            params["url"]=url
            videobam(params)             

        elif url.find("www.youtube.com") >= 0:
            plugintools.log("Youtube: "+url)
            videoid = url.replace("https://www.youtube.com/watch?v=", "")
            url = 'plugin://plugin.video.youtube/play/?video_id='+videoid
            url = url.strip()
            play_url(url)

        elif url.find("dailymotion.com/video") >= 0:
            plugintools.log("Dailymotion: "+url)
            video_id = dailym_getvideo(url)
            if video_id != "":
                thumbnail = "https://api.dailymotion.com/thumbnail/video/"+video_id+""
                url = "plugin://plugin.video.dailymotion_com/?url="+video_id+"&mode=playVideo"
                play_url(url)

        elif url.find("dailymotion.com/playlist") >= 0:
            plugintools.log("Dailymotion: "+url)
            id_playlist = dailym_getplaylist(url)
            if id_playlist != "":
                url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                thumbnail = "https://api.dailymotion.com/thumbnail/video/"+id_playlist
                if thumbnail == "":
                    thumbnail = 'http://press.dailymotion.com/wp-old/wp-content/uploads/logo-Dailymotion.png'
                url = "https://api.dailymotion.com/playlist/"+id_playlist+"/videos"
                params["url"]=url
                dailym_pl(params)
                
        elif url.find(".m3u8") >= 0:
            plugintools.log("M3u8: "+url)
            url = url.strip()
            play_url(url)

        else:
            url = url.strip()
            play_resolved_url(url)
            
    elif url.startswith("udp") == True:
        plugintools.log("UDP: "+url)
        url = url.strip()
        play_url(url)         
    
    elif url.startswith("rtp") == True:
        plugintools.log("RTP: "+url)
        url = url.strip()
        play_url(url)             
    
    elif url.startswith("mms") == True:
        plugintools.log("mms: "+url)
        url = url.strip()
        play_url(url)       

    elif url.startswith("plugin") == True:
        if url.find("youtube") >= 0 :
            plugintools.log("Youtube: "+url)
            url = url.strip()
            play_url(url)               
            
        elif url.find("mode=1") >= 0 :
            plugintools.log("Acestream: "+url)
            url = url.strip()
            play_url(url)
            
        elif url.find("mode=2") >= 0 :
            plugintools.log("Sopcast: "+url)
            url = url.strip()
            play_url(url)
            
    elif url.startswith("magnet") == True:
        plugintools.log("Magnet link: "+url)
        url_fixed = urllib.quote_plus(data)
        url = 'plugin://plugin.video.xbmctorrent/play/' + url_fixed
        url = url.strip()
        play_url(url)

    elif url.startswith("sop") == True:
        plugintools.log("Sopcast: "+url)
        # plugin://plugin.video.p2p-streams/?url=sop://124.232.150.188:3912/11265&mode=2&name=Titulo+canal+Sopcast
        url = 'plugin://plugin.video.p2p-streams/?url=' + data + '&mode=2&name=' + title_fixed
        url = url.strip()
        play_url(url)
        
    elif url.startswith("ace") == True:
        plugintools.log("Acestream: "+url)
        url = url.replace("ace:", "")
        url = url.strip()
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name='
        url = url.strip()
        play_url(url)                                         
    
    elif url.startswith("yt_playlist") == True:
        pid = url.replace("yt_playlist(", "")
        pid = pid.replace(")", "").strip()
        pid = pid+'/';pid=pid.strip();pid.replace(" ", "")
        url = 'plugin://plugin.video.youtube/playlist/'+pid
        plugintools.log("URL Playlist= "+url)
        run_tube(url)
        
    elif url.startswith("yt_channel") == True:
        uid = url.replace("yt_channel(", "")
        uid = uid.replace(")", "").strip()
        uid = uid+'/';uid=uid.strip();uid.replace(" ", "")        
        url = 'plugin://plugin.video.youtube/user/'+uid
        plugintools.log("URL Channel= "+url)
        run_tube2(params)
            
    elif url.startswith("short") == True:
        url = url.replace("short:", "").strip()
        params["url"]=url;longurl(params)

    elif url.startswith("devil") == True:
        url = url.replace("devil:", "")
        url = url.split(" ")
        url = url[0];ref=url[1];ref=ref.replace("referer=", "").strip()
        url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+referer
        play_devil(url)        

    elif url.startswith("bum") == True:
        params = plugintools.get_params()
        title = params.get("title")
        show = "list"
        title = multiparse_title(title, url, show)        
        bum_multiparser(params)

    elif url.startswith("img") == True:
        url = url.replace("img:", "").strip()        
        params = plugintools.get_params()
        title = params.get("title")
        show = "thumbnail"
        title = multiparse_title(title, url, show)
        show_image(url)        
	
        
        

def youtube_playlists(url):
    plugintools.log('[%s %s].youtube_playlists %s' % (addonName, addonVersion, url))	
    
    data = plugintools.read(url)
        
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        plot = plugintools.find_single_match(entry,"<media\:descriptio[^>]+>([^<]+)</media\:description>")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")           
        url = plugintools.find_single_match(entry,"<content type\='application/atom\+xml\;type\=feed' src='([^']+)'/>")
        fanart = art + 'youtube.png'
        
        plugintools.add_item( action="youtube_videos" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , folder=True )
        plugintools.log("fanart= "+fanart)


# Muestra todos los vídeos del playlist de Youtube
def youtube_videos(url):
    plugintools.log('[%s %s].youtube_videos %s' % (addonName, addonVersion, url))	
    
    # Fetch video list from YouTube feed
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    
    # Extract items from feed
    pattern = ""
    matches = plugintools.find_multiple_matches(data,"<entry(.*?)</entry>")
    
    for entry in matches:
        plugintools.log("entry="+entry)
        
        # Not the better way to parse XML, but clean and easy
        title = plugintools.find_single_match(entry,"<titl[^>]+>([^<]+)</title>")
        title = title.replace("I Love Handball | ","")
        plot = plugintools.find_single_match(entry,"<summa[^>]+>([^<]+)</summa")
        thumbnail = plugintools.find_single_match(entry,"<media\:thumbnail url='([^']+)'")
        fanart = art+'youtube.png'
        video_id = plugintools.find_single_match(entry,"http\://www.youtube.com/watch\?v\=([0-9A-Za-z_-]{11})")
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid="+video_id

        # Appends a new item to the xbmc item list
        plugintools.add_item( action="play" , title=title , plot=plot , url=url , thumbnail=thumbnail , fanart=fanart , isPlayable=True, folder=False )


def parse_url(url, show):
    plugintools.modo_vista(show)
    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")        
        return url
    
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)


def multiparser(params):
    plugintools.log('[%s %s].Multiparser %s' % (addonName, addonVersion, repr(params)))
    dialog = xbmcgui.Dialog()

    show = params.get("page")  # Control de modo de vista predefinido
    plugintools.modo_vista(show)

    #info_plot = params["info_labels"]
    #print 'info_plot',info_plot

    filename = params.get("extra")
    plugintools.log("filename= "+filename)
    file = open(playlists + filename, "r")
    file.seek(0)
    title = params.get("title").replace("[Multiparser]", "").strip()
    title = parser_title(title)
    
    if title.find("  ") >= 0:
        title = title.split("  ")
        title = title[0].strip()
        title = "@"+title  # En la lista aparecerá el título precedido por el símbolo @
        #plugintools.log("title_epg= "+title)
    
    encuentra = '#EXTINF:-1,' + title.replace(" [COLOR lightyellow][Multiparser][/COLOR]","")
    plugintools.log("*** Texto a buscar= "+encuentra)
    i = 0
    data = file.readline()
    #print data
    while i <=8:  # Control para EOF
        if data == "":
            i = i + 1
            data = file.readline().strip()
            #print data
            continue
        else:
            i = 0
            if data.startswith(encuentra) == True:
                data = file.readline().strip()
                print data
                if data == "#multiparser":
                    #Leemos número de enlaces
                    i = 1  # Variable contador desde 1 porque nos servirá para nombrar los títulos
                    # Recopilamos enlaces en una lista
                    linea_url = file.readline().strip()
                    if linea_url.startswith("desc") == True:
                        linea_url = file.readline().strip()
                    print 'linea_url',linea_url
                    menu_seleccion = []
                    url_seleccion = []
                    while linea_url != "#multiparser" :                         
                        linea_url = linea_url.strip().split(",")
                        url_option = linea_url[1]
                        title_option = linea_url[0]                        
                        title_option = str(i) + ': ' + title_option
                        title_fixed = multiparse_title(title_option, url_option, show)
                        title_option = title_fixed
                        plugintools.log("title= "+title_option)
                        i = i + 1
                        menu_seleccion.append(title_option)
                        url_seleccion.append(url_option)
                        linea_url = file.readline()
                        linea_url = linea_url.strip()
                print menu_seleccion
                num_items = i - 1
                plugintools.log("Núm. items= "+str(num_items))
            else:                
                data = file.readline().strip() 

    print menu_seleccion
    print title
    seleccion = plugintools.selector(menu_seleccion,title)
    print seleccion
    if seleccion >= 0:            
        url_analyzer(url_seleccion[seleccion])

    plugintools.modo_vista(show)


def multilink(params):
    plugintools.log('[%s %s].multilink %s' % (addonName, addonVersion, repr(params)))

    show = params.get("page")
    plugintools.set_view(show)
    dialog = xbmcgui.Dialog()
    filename = params.get("extra")
    plugintools.log("filename= "+filename)
    file = open(playlists + filename, "r")
    file.seek(0)
    title = params.get("title")
    #title = parser_title(params.get("title"))
    title_parsed = parser_title(params.get("title"))
    plugintools.log("title= "+title)
    
    if title.find("  ") >= 0:
        title = title.split("  ")
        title = title[0].strip()
        title = "@"+title  # En la lista aparecerá el título precedido por el símbolo @
        
    encuentra = '#EXTINF:-1,' + title.replace(" [COLOR lightyellow][Multilink][/COLOR]","").replace("[COLOR white]", "")
    if encuentra.startswith("#EXTINF:-1,@") == True:
        title_epg = title.replace("[COLOR white]","").split("[COLOR orange")
        if len(title_epg) >= 1:
            title_epg = title_epg[0]
        encuentra = '#EXTINF:-1,'+title_epg;encuentra=encuentra.strip()
    plugintools.log("*** Texto a buscar= "+encuentra)
    i = 0
    data = file.readline()
    if data.startswith("#EXTINF:-1,@") == True:
        epg_no = plugintools.get_setting("epg_no")
        plugintools.log("epg_no= "+epg_no)
        if epg_no == "0":  # No desactivado EPG
            pass
        else:
            data = data.replace("@", "")
    encuentra = encuentra.replace("@", "")
    print data
    while i <=8:  # Control para EOF
        if data == "":
            i = i + 1
            data = file.readline().strip()
            if data.startswith("#EXTINF:-1,@") == True:
                data = data.replace("@", "")
            continue
        else:
            i = 0
            plugintools.log("encuentra= "+encuentra)
            plugintools.log("data= "+data)
            if data.startswith(encuentra) == True or data.startswith('#EXTINF:-1,@' + title.replace(" [COLOR lightyellow][Multilink][/COLOR]","")) == True:
                print 'correcto'
                data = file.readline().strip()
                if data == "#multilink":
                    #Leemos número de enlaces
                    i = 1  # Variable contador desde 1 porque nos servirá para nombrar los títulos
                    # Recopilamos enlaces en una lista
                    linea_url = file.readline().strip()
                    if linea_url.startswith("desc") == True:
                        linea_url = file.readline().strip()
                        
                    title_options = []
                    url_options = []
                    while linea_url != "#multilink" :
                        linea_url = linea_url.strip().split(",")
                        url_option = linea_url[1]
                        title_option = linea_url[0]
                        if title_option.startswith("@") == True:
                            title_option = title_option.replace("@", "")

                            # Ejecutamos EPG...
                            epg_channel = []
                            epg_channel = epg_now(title_option)
                            if epg_now(title_option) == False:
                                print "No hay EPG"
                            else:
                                try:
                                    print epg_channel
                                    ejemplo = epg_channel[0]
                                    print epg_channel[0]                                    
                                    title_option = title_option + " [COLOR orange][I][B] " + epg_channel[0] + "[/B] " + epg_channel[1] + "[/I][/COLOR] "
                                except:
                                    pass

                        title_option = str(i) + ': ' + title_option
                        title_fixed = multiparse_title(title_option, url_option,show)
                        title_option = title_fixed
                        plugintools.log("title= "+title_option)
                        i = i + 1
                        title_options.append(title_option)
                        url_options.append(url_option)
                        linea_url = file.readline()
                        linea_url = linea_url.strip()
                print title_options
                print url_options
                num_items = i - 1
                plugintools.log("Núm. items= "+str(num_items))
                if title.startswith("@") == True:  # Para evitar que en el título del cuadro de diálogo aparezca el nombre del canal precedido por el símbolo arroba (@)
                    title = title.replace("@","")
                                
                try:
                    selector = plugintools.selector(title_options,title)
                    print selector
                    if selector >= 0:            
                        url_analyzer(url_options[selector])

                except KeyboardInterrupt: pass;
                except IndexError: raise;
            else:
                data = file.readline().strip()        

    plugintools.modo_vista(show)

    


# Esta función añade coletilla de tipo de enlace a los multilink
def multiparse_title(title, url, show):
    plugintools.log('[%s %s] Multiparse_title: %s' % (addonName, addonVersion, url))
    
    if show == "":
        show = "list"
        plugintools.modo_vista(show)

    plugintools.log("URL multiparse_title= "+url)

    if url == "mundoplus":
        title = title + ' [COLOR lightyellow][I][Agenda[B]TV[/B]][/I][/COLOR]' 

    elif url.startswith("serie") == True:
        if url.find("seriesflv") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]FLV[/B]][/I][/COLOR]'
        if url.find("seriesyonkis") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Yonkis[/B]][/I][/COLOR]'
        if url.find("seriesadicto") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Adicto[/B]][/I][/COLOR]'
        if url.find("seriesblanco") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B]Blanco[/B]][/I][/COLOR]'
        if url.find("series.mu") >= 0:
            title = title + ' [COLOR lightyellow][I][Series[B].Mu[/B]][/I][/COLOR]'            

    elif url.startswith("goear") == True:
        title = title + ' [COLOR lightyellow][I][goear][/I][/COLOR]'        

    elif url.startswith("http") == True:        
        if url.find("allmyvideos") >= 0:
            title = title + ' [COLOR lightyellow][I][Allmyvideos][/I][/COLOR]'

        elif url.find("streamcloud") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamcloud][/I][/COLOR]'

        elif url.find("vidspot") >= 0:
            title = title + ' [COLOR lightyellow][I][Vidspot][/I][/COLOR]'
            
        elif url.find("played.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Played.to][/I][/COLOR]'       

        elif url.find("vk.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Vk][/I][/COLOR]'

        elif url.find("nowvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Nowvideo.sx][/I][/COLOR]'            
        
        elif url.find("tumi") >= 0:
            title = title + ' [COLOR lightyellow][I][Tumi][/I][/COLOR]'

        elif url.find("streamin.to") >= 0:
            title = title + ' [COLOR lightyellow][I][Streamin.to][/I][/COLOR]'

        elif url.find("veehd") >= 0:
            title = title + ' [COLOR lightyellow][I][Veehd][/I][/COLOR]'
            
        elif url.find("tumi.tv") >= 0:
            title = title + ' [COLOR lightyellow][I][Tumi.tv][/I][/COLOR]'       

        elif url.find("novamov") >= 0:
            title = title + ' [COLOR lightyellow][I][Novamov][/I][/COLOR]'

        elif url.find("gamovideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Gamovideo][/I][/COLOR]'            
        
        elif url.find("moevideos") >= 0:
            title = title + ' [COLOR lightyellow][I][Moevideos][/I][/COLOR]'

        elif url.find("movshare") >= 0:
            title = title + ' [COLOR lightyellow][I][Movshare][/I][/COLOR]'

        elif url.find("powvideo") >= 0:
            title = title + ' [COLOR lightyellow][I][Powvideo][/I][/COLOR]'

        elif url.find("mail.ru") >= 0:
            title = title + ' [COLOR lightyellow][I][Mail.ru][/I][/COLOR]'

        elif url.find("netu") >= 0:
            title = title + ' [COLOR lightyellow][I][Netu][/I][/COLOR]'

        elif url.find("videobam") >= 0:
            title = title + ' [COLOR lightyellow][I][Videobam][/I][/COLOR]'              

        elif url.find("www.youtube.com") >= 0:
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'

        elif url.find("dailymotion.com/video") >= 0:
            title = title + ' [COLOR lightyellow][I][Dailymotion Video][/I][/COLOR]'

        elif url.find("dailymotion.com/playlist") >= 0:
            title = title + ' [COLOR lightyellow][I][Dailymotion Playlist][/I][/COLOR]'            

        elif url.find(".m3u8") >= 0:
            title = title + ' [COLOR lightyellow][I][M3u8][/I][/COLOR]'

        else:
            title = title + ' [COLOR lightyellow][I][HTTP][/I][/COLOR]'
            
    elif url.startswith("rtmp") == True:        
        if url.find("iguide.to") >= 0:
            title = title + ' [COLOR lightyellow][I][iguide][/I][/COLOR]'
        elif url.find("freetvcast.pw") >= 0:
            title = title + ' [COLOR lightyellow[I][freetvcast][/I][/COLOR]'
        elif url.find("pageUrl=http://privado.streamingfreetv.net") >= 0:
            title = title + ' [COLOR lightyellow][I][streamingfreetv][/I][/COLOR]'
        elif url.find("9stream") >= 0:
            title = title + ' [COLOR lightyellow][I][9stream][/I][/COLOR]'
        elif url.find("freebroadcast") >= 0:
            title = title + ' [COLOR lightyellow][I][freebroadcast][/I][/COLOR]'
        elif url.find("cast247") >= 0:
            title = title + ' [COLOR lightyellow][I][cast247][/I][/COLOR]'
        elif url.find("castalba") >= 0:
            title = title + ' [COLOR lightyellow][I][castalba][/I][/COLOR]'
        elif url.find("direct2watch") >= 0:
            title = title + ' [COLOR lightyellow][I][direct2watch][/I][/COLOR]'
        elif url.find("vaughnlive") >= 0:
            title = title + ' [COLOR lightyellow][I][vaughnlive][/I][/COLOR]'
        elif url.find("sawlive") >= 0:
            title = title + ' [COLOR lightyellow][I][sawlive][/I][/COLOR]'        
        elif url.find("shidurlive") >= 0:
            title = title + ' [COLOR lightyellow][I][shidurlive][/I][/COLOR]'
        elif url.find("vercosas") >= 0:
            title = title + ' [COLOR lightyellow][I][vercosas][/I][/COLOR]'
        elif url.find("pageUrl=http://rdmcast.com") >= 0:
            title = title + ' [COLOR lightyellow][I][rdmcast][/I][/COLOR]'
        elif url.find("businessapp1") >= 0:
            title = title + ' [COLOR lightyellow][I][businessapp1][/I][/COLOR]'             
        else:
            title = title + ' [COLOR lightyellow][I][rtmp][/I][/COLOR]'            
            
    elif url.startswith("udp") == True:
        title = title + ' [COLOR lightyellow][I][udp][/I][/COLOR]'         
    
    elif url.startswith("rtp") == True:
        title = title + ' [COLOR lightyellow][I][rtp][/I][/COLOR]'            
    
    elif url.startswith("mms") == True:
        title = title + ' [COLOR lightyellow][I][mms][/I][/COLOR]'      

    elif url.startswith("plugin") == True:
        if url.find("youtube") >= 0 :
            title = title + ' [COLOR lightyellow][I][Youtube][/I][/COLOR]'
            
        elif url.find("mode=1") >= 0 :
            title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'
            
        elif url.find("mode=2") >= 0 :
            title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'
            
    elif url.startswith("magnet") == True:
        title = title + ' [COLOR lightyellow][I][Torrent][/I][/COLOR]'

    elif url.startswith("sop") == True:
        title = title + ' [COLOR lightyellow][I][Sopcast][/I][/COLOR]'        
        
    elif url.startswith("ace") == True:
        title = title + ' [COLOR lightyellow][I][Acestream][/I][/COLOR]'

    elif url.startswith("yt") == True:
        if url.startswith("yt_playlist") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Playlist][/I][/COLOR]'

        elif url.startswith("yt_channel") == True:
            title = title + ' [COLOR lightyellow][I][Youtube Channel][/I][/COLOR]'

    elif url.startswith("bum") == True:
        title_fixed = title
        title = title + ' [COLOR lightyellow][I][BUM+][/I][/COLOR]'        
        params = plugintools.get_params()
        params["title"] = title_fixed
        plugintools.log("params_fixed = "+repr(params))

    elif url.startswith("devil") == True:
        title = title + ' [COLOR lightyellow][I][SportsDevil][/I][/COLOR]'

    elif url.startswith("short") == True:
        title = title + ' [COLOR lightyellow][I][ShortLink][/I][/COLOR]'        

    elif url.startswith("img") == True:
        title = title + ' [COLOR lightyellow][I][IMG][/I][/COLOR]'        
        
    else:
        plugintools.log("URL desconocida= "+url)
        title = title + ' [COLOR lightyellow][I][Unknown][/I][/COLOR]'

    plugintools.log("URL tras multiparser title= "+url)
    return title


# Función modificada de show_image para multilinks para evitare rror en url = params.get("url") porque url es #multilink 
def show_image(url):
    plugintools.log('[%s %s].show_image %s' % (addonName, addonVersion, url))

    plugintools.log("Iniciando descarga desde..."+url)
    h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
    request = urllib2.Request(url)
    opener = urllib2.build_opener(h)
    urllib2.install_opener(opener)
    filename = url.split("/")
    max_len = len(filename)
    max_len = int(max_len) - 1
    filename = filename[max_len]
    fh = open(__temp__ + filename, "wb")  #open the file for writing
    connected = opener.open(request)
    meta = connected.info()
    filesize = meta.getheaders("Content-Length")[0]
    size_local = fh.tell()
    print 'filesize',filesize
    print 'size_local',size_local
    while int(size_local) < int(filesize):
        blocksize = 100*1024
        bloqueleido = connected.read(blocksize)
        fh.write(bloqueleido)  # read from request while writing to file
        size_local = fh.tell()
        print 'size_local',size_local
    imagen = __temp__ + filename
    xbmc.executebuiltin( "ShowPicture("+imagen+")" )

def play_devil(url):
    plugintools.modo_vista("tvshows")
    plugintools.log("URL SportsDevil= "+url)
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')

def run_tube(url):    
    plugintools.log("RunPlugin = "+url)
    xbmc.executebuiltin('XBMC.RunPlugin('+url+')')

def run_tube2(params):    
    plugintools.log("RunPlugin = "+repr(params))
    url = params.get("url")
    xbmc.executebuiltin('XBMC.RunScript('+url+')')
    
