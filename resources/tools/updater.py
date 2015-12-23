# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 Updater v0.2 (21.10.2014)
# Version 0.3.0 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import time
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools



# Comprobamos qué versión es la más reciente
def check_update(params):
    plugintools.log("[beta.1-0.3.0].check_update "+repr(params))

    data = plugintools.read( params.get("url") )
    #plugintools.log("data= "+data)
    title = params.get("title")
    name_channel = parser_title(title)
    # name_channel = parser_title(name_channel)
    data_update = plugintools.find_single_match(data, '<name>'+name_channel+'(.*?)</channel>')
    #plugintools.log("data= "+data_update)

    last_update = plugintools.find_single_match(data_update, '<last_update>(.*?)</last_update>')
    #plugintools.log("last_update= "+last_update)

    subchannel = plugintools.find_multiple_matches(data_update, '<subchannel>(.*?)</subchannel>')
    for entry in subchannel:
        #plugintools.log("entry= "+entry)
        title = plugintools.find_single_match(entry, '<name>(.*?)</name>')
        url = plugintools.find_single_match(entry, '<url>([^<]+)</url>')
        thumbnail = plugintools.find_single_match(entry, '<thumbnail>([^<]+)</thumbnail>')
        action = plugintools.find_single_match(entry, '<action>([^<]+)</action>')
        last_update = plugintools.find_single_match(entry, '<last_update>([^<]+)</last_update>')
        size_remote = plugintools.find_single_match(entry, '<filesize>([^<]+)</filesize>')
        fanart = plugintools.find_single_match(entry, '<fanart>([^<]+)')

        # Control mayus-minus en la lista de actualizaciones
        title_low = title.lower()
        
        if title_low.find("beta.1") >= 0:
            f = open(home + 'default.py', 'r')
            filename = 'plugin.video.t-killa-wip-wip-' + last_update + '.zip'
            actualizar = plugintools.read("http://pastebin.com/raw.php?i=q0aiK6ck")
            plugintools.log("version para actualizar= "+actualizar)
            actualizar = actualizar.strip()
            instalada = '0.3.01'       
            if actualizar == instalada :
                plugintools.log("No es necesario actualizar beta.1")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.log("Actualizar beta.1")                
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)


        if title_low.find("actualizador") >= 0:
            filename = 'updater.py'            
            f = open(tools + 'updater.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar el updater")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)
                

        # ¡OJO! Se aloja en /xbmc/addons/plugin.video-beta.1/settings/
        if title_low.find("config") >= 0:
            f = open(resources + 'settings.xml', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar settings.xml")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        # ¡OJO! Se aloja en /xbmc/addons/plugin.video-beta.1/
        if title_low.find("main") >= 0:
            filename = 'default.py'            
            f = open(home + 'default.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar settings.xml")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)                

        if title_low.find("conectores") >= 0:
            filename = 'resolvers.py'            
            f = open(tools + 'resolvers.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar los conectores multimedia")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("1torrent.ru") >= 0:
            filename = 'torrent1.py'            
            f = open(tools + 'torrent1.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar el conector de 1torrent")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("torrent-tv.ru") >= 0:
            filename = 'torrentvru.py'
            f = open(tools + 'torrentvru.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar el conector multimedia de Torrent-TV.ru")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)                  


        if title_low.find("shidurlive") >= 0:           
            filename = 'shidurlive.py'
            f = open(tools + 'shidurlive.py', 'r')            
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("9stream") >= 0:
            filename = 'ninestream.py'              
            f = open(tools + 'ninestream.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)
               
        if title_low.find("direct2watch") >= 0:
            filename = 'directwatch.py'              
            f = open(tools + 'directwatch.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("vaughnlive") >= 0:
            filename = 'vaughnlive.py'              
            f = open(tools + 'vaughnlive.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("vercosasgratis") >= 0:
            filename = 'vercosas.py'              
            f = open(tools + 'vercosas.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("freebroadcast") >= 0:
            filename = 'freebroadcast.py'              
            f = open(tools + 'freebroadcast.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("freetvcast") >= 0:
            filename = 'freetvcast.py'              
            f = open(tools + 'freetvcast.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("castalba") >= 0:
            filename = 'castalba.py'            
            f = open(tools + 'castalba.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("cast247") >= 0:
            filename = 'castdos.py'            
            f = open(tools + 'castdos.py', 'r')
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)

        if title_low.find("prueba") >= 0:
            f = open(tools + 'prueba.py', 'r')
            filename = 'prueba.py'
            f.seek(0,2)
            size_local = f.tell()
            size_local = str(size_local)                            
            #plugintools.log("size_local= " +size_local)  # Tamaño en bytes
            #plugintools.log("size_remote= "+size_remote)            
            if size_remote == size_local :
                plugintools.log("No es necesario actualizar")
            else:
                # Hay que actualizar, así que mostramos la entrada
                plugintools.add_item(action = action, title = title + '[COLOR lightgreen][I] [' + last_update + '][/I][/COLOR]', url = url , thumbnail = thumbnail , extra = filename , fanart = fanart , folder = False , isPlayable = False)                 
             


def update_file(params):
    plugintools.log("[beta.1-0.3.0].Update_now "+repr(params))


    # Iniciamos barra de progreso BG durante la actualización
    progreso = xbmcgui.DialogProgressBG()
    local_filename = params.get("extra")
    progreso.create("Iniciando actualización de " , local_filename )
    yesno = 0
    
    try:
        remote_filename = "https://dl.dropboxusercontent.com/u/8036850/updater/" + local_filename
        plugintools.log("remote= "+remote_filename)        
        r = urllib2.urlopen(remote_filename)
        f = open(tmp + local_filename, "wb")
        f.write(r.read())
        f.close()

    except IOError:
        pass
        yesno = 0
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Actualización fallida", 3 , art+'icon.png'))    

    try:
		title = params.get("title")
		title = title.lower()
		if title.find("main") >= 0:
			shutil.copyfile(tmp + local_filename, home + local_filename)
			yesno = 1
		else:
			shutil.copyfile(tmp + local_filename, tools + local_filename)
			yesno = 1
    except:
        pass
        yesno = 0
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Error al sobreescribir", 3 , art+'icon.png'))

    try:
        os.remove(tmp + local_filename)        
    except:
        progreso.close()
        pass

    if yesno == 1:
        progreso.close()
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Actualización completada", 3 , art+'icon.png'))


def update_palco(params):
    plugintools.log("[beta.1-0.3.0].update_palco "+repr(params))
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Espere...", 3 , art+'icon.png'))
  
    local_filename = params.get("extra")
    remote_filename = params.get("url")
    plugintools.log("local= "+local_filename)
    plugintools.log("remote= "+remote_filename)

    try:      
        r = urllib2.urlopen(remote_filename)
        f = open(tmp + local_filename, "wb")
        f.write(r.read())
        f.close()
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Actualización completada", 3 , art+'icon.png'))
        

    except IOError:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Error en la descarga", 3 , art+'icon.png'))       

        
    try:
        unzipper = ziptools()
        unzipper.extract(tmp + local_filename, remote_filename, params)
        
    except IOError:
        pass
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Actualización fallida", 3 , art+'icon.png'))

    os.remove(tmp + local_filename)




class ziptools:

    def extract(self, file, dir, params):
        plugintools.log("file=%s" % file)
        #dir = addons
        
        if not dir.endswith(':') and not os.path.exists(dir):
            os.mkdir(dir)

        zf = zipfile.ZipFile(file)
        self._createstructure(file, dir)
        num_files = len(zf.namelist())

        for name in zf.namelist():
            plugintools.log("name=%s" % name)
            if not name.endswith('/'):
                plugintools.log("no es un directorio")
                plugintools.log("dst_folder= "+dir)                                
                try:
                    (path,file) = os.path.split(os.path.join(dir, name))
                    plugintools.log("path=%s" % path)
                    plugintools.log("name=%s" % name)
                    os.makedirs( path )
                except:
                    pass
                outfilename = os.path.join(dir, name)
                plugintools.log("outfilename=%s" % outfilename)
                try:
                    outfile = open(outfilename, 'wb')
                    outfile.write(zf.read(name))
                except:
                    plugintools.log("Error en fichero "+name)

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)

    def create_necessary_paths(filename):
        try:
            (path,name) = os.path.split(filename)
            os.makedirs( path)
        except:
            pass

    def _makedirs(self, directories, basedir):
        for dir in directories:
            curdir = os.path.join(addons, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        zf = zipfile.ZipFile(file)
        dirs = []
        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs
    
 

      
def parser_title(title):
    plugintools.log("[beta.1-0.3.0].parser_title " + title)

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
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")

    title = cyd
    title = title.strip()
    plugintools.log("title_parsed= "+title)
    return title

