# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Backup de enlaces de regex de series (BERS) de SeriesYonkis para beta.1 (beta.1.net)
# Version 0.1 (25.04.2015)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)
#
#
#
# Esta función guarda enlaces de UN CAPÍTULO de los regex de series
# Crea archivo M3U con el formato: TEMPxCAP TITULO DE LA SERIE [Seriesyonkis].m3u
# Ejemplo: 04x11 The Walking Dead [Seriesyonkis].m3u
# Creará inicialmente tres archivos M3U, uno por cada tipo de idioma del audio (castellano, latino, vos)
# Esta función debe complementarse con otra que agrupe los tres multilinks de cada capítulo en un único archivo M3U
# Además, debería crearse un archivo M3U para indexar todos los archivos M3U
#
# El proceso debe automatizarse de forma que al seleccionar una serie de un regex se guarden todos los enlaces de todos los capítulos
# Comprobar tiempo de ejecución de la función y calcular variable seg/url
#
#
# Agregar variable "bers" en settings.xml para activar esta herramienta

import os
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import plugintools

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

from __main__ import *
fanart = 'fanart.jpg'
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))


def bers_sy0(params):
    plugintools.log('[%s %s] Iniciando BERS de SeriesYonkis %s' % (addonName, addonVersion, repr(params)))

    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    plugintools.modo_vista(show)

    datamovie={}
    plot = params.get("plot")
    if plot != "":
        datamovie["Plot"]=plot  # Cargamos sinopsis de la serie... (si existe)
    else:
        datamovie["Plot"]="."    
    
    url = params.get("url")
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url,referer,show)
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV    
    plugintools.modo_vista(show)          
    #Carátula
    cover = plugintools.find_single_match(data, '<img src="([^"]+)')
    match_temporadas = plugintools.find_single_match(data, '<div id="section-content">(.*?)</ul>')
    temps = plugintools.find_multiple_matches(match_temporadas, '<h3 class="season"(.*?)</li>')
    
    for entry in temps:
        capis = plugintools.find_multiple_matches(entry, '<td class="episode-title">(.*?)</td>')
        for entri in capis:
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
            plot = datamovie["Plot"]; page_url = url_cap; title = title_capi; source_web = "seriesyonkis"; thumbnail = cover;title_serie = params.get("title")
            #bers_sy1(plot, title_fixed, title, title_serie, page_url, thumbnail, fanart, source_web)
            referer = 'http://www.seriesyonkis.sx/'
            data = gethttp_referer_headers(page_url,referer,show)
            plugintools.modo_vista(show)
            #plugintools.log("data= "+data)
            matches = plugintools.find_single_match(data, '<h2 class="header-subtitle veronline">(.*?)</table>')
            match_veronline = plugintools.find_single_match(matches, '<tbody>(.*?)</tbody>')
            match_links = plugintools.find_multiple_matches(match_veronline, '<tr>(.*?)</tr>')
            for entry in match_links:
                #plugintools.log("entry= "+entry)
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
                plugintools.log("bers_sy_on= "+bers_sy_on)
        
                if server.find("tumi.tv") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == 1:
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                
                elif server.find("streamin.to") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                   
                elif server.find("vidspot") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                 
                elif server.find("allmyvideos") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                              
                elif server.find("streamcloud") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                     
                elif server.find("nowvideo.sx") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                   
                elif server.find("veehd") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                    
                if server.find("allmyvideos") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'          
                    
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                    
                elif server.find("novamov.com") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                   
                elif server.find("Moevideos") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                 
                elif server.find("Gamovideo") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                              
                elif server.find("movshare.net") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                                 
                elif server.find("played.to") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                       
                elif server.find("mail.ru") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)

                elif server.find("vk") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)
                    
                elif server.find("videobam") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)

                elif server.find("powvideo.net") >= 0:
                    title = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    title_bers = title_fixed + ' [COLOR lightyellow][I]'+idioma_capi+'[/I][/COLOR]'
                    if bers_sy_on == "true":  # Control para ejecutar BERS a nivel de capítulo
                        bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web)

            filename = parser_title(title_serie) + " " + parser_title(title_fixed)+".m3u"
            backup_serie = open(temp + filename, "a")
            backup_serie.write('#multilink\n')
            backup_serie.close()
            bers_sy4(filename, title_serie)                        

               



def bers_sy1(plot, title_fixed, title, title_serie, title_bers, page_url, thumbnail, fanart, source_web):
    plugintools.log('[%s %s] Creando archivos BERS... %s' % (addonName, addonVersion, title))

    params = plugintools.get_params()
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    plugintools.modo_vista(show)

    plugintools.log("title_fixed= "+title_fixed)
    plugintools.log("title= "+title)
    plugintools.log("title_serie= "+title_serie)

    title_fixed = title_serie + " " + title_fixed
    filename = parser_title(title_fixed)+".m3u"
    plugintools.log("page_url= "+page_url)
    	
    # Vamos a crear los archivos si no existen para cada idioma de audio
    if not os.path.isfile(temp + filename):    
        plugintools.log("Creando archivo... temp/"+filename)
        backup_serie = open(temp + filename, "a")
        backup_serie.seek(0)
        title = parser_title(title_fixed)
        #backup_serie.write('#EXTM3U,view:tvshows\n\n')  # Fijamos modo de vista para la lista de películas
        backup_serie.write('#EXTINF:-1,'+title+',tvg-logo="'+thumbnail+'",'+'plot="'+plot+'"\n')
        backup_serie.write('#multilink\n')
        backup_serie.close()

    bers_sy2(title, title_bers, page_url, thumbnail, fanart, filename)

        

def bers_sy2(title, title_bers, page_url, thumbnail, fanart, filename):
    plugintools.log('[%s %s] Guardando URL...%s ' % (addonName, addonVersion, title))

    params = plugintools.get_params()
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    plugintools.modo_vista(show)
    url = params.get("url")
    backup_serie = open(temp + filename, "a")  # Abrimos el archivo en modo escritura    
    url = bers_sy3(page_url)
    filename_fixed = title
    backup_serie.write(title_bers+','+url+'\n')
    backup_serie.close()
    plugintools.log('[%s %s] BERS: %s , %s' % (addonName, addonVersion, title, page_url))



def bers_sy3(page_url):
    plugintools.log('[%s %s].bers_sy2 %s' % (addonName, addonVersion, page_url))

    params = plugintools.get_params()
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    plugintools.modo_vista(show)
    
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(page_url,referer,show)
    #plugintools.log("data= "+data)
    
    match = plugintools.find_single_match(data, '<table class="episodes full-width">(.*?)</table>')
    url_final = plugintools.find_single_match(match, '<a href="([^"]+)')
    plugintools.log("url_final= "+url_final)
    return url_final

    plugintools.modo_vista(show)



def bers_sy4(filename, title_serie):
    plugintools.log('[%s %s] Guardando multilink en %s...' % (addonName, addonVersion, title_serie))

    params = plugintools.get_params()
    show = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    plugintools.modo_vista(show)    
	
    filename_serie = parser_title(title_serie)+'.m3u'
        
    m3u_cap = open(temp + filename, "r")
    m3u_cap.seek(0)
    data = m3u_cap.read()
    
    if os.path.exists(filename_serie):
        plugintools.log("Creando archivo... temp/"+filename_serie)
        m3u_serie = open(temp + filename_serie, "a")
        m3u_serie.seek(0)
        m3u_serie.write('#EXTM3U,view:tvshows\n\n')  # Fijamos modo de vista para el BERS
        m3u_serie.write(data+'\n')

    else:
        m3u_serie = open(temp + filename_serie, "a")
        m3u_serie.write(data+'\n')        
        
    m3u_cap.close()
    m3u_serie.close()
    

        

def parser_title(title):
    plugintools.log('[%s %s].parser_title %s' % (addonName, addonVersion, title))

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")

    cyd = cyd.replace("&quot;", '"')

    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")
    cyd = cyd.replace(" [COLOR lightyellow][Multilink]", "")  # No borro etiqueta final para que no haya error en el formato y aparezca [COLOR...] en el título
    cyd = cyd.replace(" [Multiparser]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]PLX[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR orange][Lista [B]M3U[/B]][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] playlist][/COLOR]", "")
    cyd = cyd.replace(" [COLOR lightyellow][B][Dailymotion[/B] video][/COLOR]", "")
    cyd = cyd.replace(' [COLOR gold][CBZ][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][CBR][/COLOR]', "")
    cyd = cyd.replace(' [COLOR gold][Mediafire][/COLOR]', "")
    cyd = cyd.replace(' [COLOR lightyellow][Multiparser][/COLOR]', "")
    cyd = cyd.replace(' [CBZ]', "")
    cyd = cyd.replace(' [CBR]', "")
    cyd = cyd.replace(' [Mediafire]', "")
    
    # Control para evitar errores al crear archivos
    cyd = cyd.replace("[", "")
    cyd = cyd.replace("]", "")
    cyd = cyd.replace(":", "").replace("  ", " ").strip()
    #cyd = cyd.replace(".", "")
    
    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")

    plugintools.log("title_parsed= "+title)
    return title



def gethttp_referer_headers(url,referer,show):

    params = plugintools.get_params()
    show_default = params.get("series_id")  # Obtenemos modo de vista del usuario para series TV
    #plugintools.modo_vista(show)
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    plugintools.modo_vista(show)
    return body


