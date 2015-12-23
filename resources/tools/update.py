# -*- coding: utf-8 -*-
#------------------------------------------------------------
# beta.1 - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.9 (18.07.2014)
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

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools




def bajalib(params, platform, libdir, filename):
    plugintools.log("[beta.1-0.2.99].bajalib "+platform)

    url = "https://dl.dropboxusercontent.com/u/8036850/librtmp/librtmp-" + platform + ".zip"

    try:
        librtmp_zipfile = "librtmp-" + platform + ".zip"
        url = "https://dl.dropboxusercontent.com/u/8036850/librtmp/" + librtmp_zipfile
        plugintools.log("librtmp_zipfile= "+librtmp_zipfile)
        plugintools.log("url= "+url)
        r = urllib2.urlopen(url)
        f = open(playlists + librtmp_zipfile, "wb")
        f.write(r.read())
        f.close()

    except IOError:
        return -1


    zfobj = zipfile.ZipFile(playlists + librtmp_zipfile)

    for name in zfobj.namelist():           
        try:
            outfile = open(os.path.join(playlists, name), 'wb')
            outfile.write(zfobj.read(name))
            outfile.close()
        except IOError:
            pass #There was a problem. Continue...
            

    zfobj.close()
    
    shutil.copyfile(playlists + filename, libdir + filename)

    try:
        os.remove(playlists + librtmp_zipfile)
        os.remove(playlists + filename)
        
    except IOError:
        pass
    
    xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('beta.1', "Librería actualizada!", 3 , art+'icon.png'))
    return 0 #succesful



def get_system_platform(params):
    plugintools.log("[beta.1-0.2.99].get_system_platform " + repr(params))

   
    if xbmc.getCondVisibility( "system.platform.ipad" ):
        platform = "linux"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)

    if xbmc.getCondVisibility( "system.platform.iphone" ):
        platform = "iphone"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)

    if xbmc.getCondVisibility( "system.platform.appletv" ):
        platform = "appletv"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)         

    elif xbmc.getCondVisibility( "system.platform.linux" ):
        platform = "android"
        # /data / data / org.xbmc.xbmc / lib / librtmp.so
        libdir = xbmc.translatePath(os.path.join('special://data/data/org.xbmc.xbmc/lib/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.so"
        shutil.copyfile(libdir + 'librtmp.so', libdir + 'librtmp.so')

        bajalib(params, platform, libdir, filename)        
                
    elif xbmc.getCondVisibility( "system.platform.windows" ):
        platform = "windows"
        # Program Files (x86)/XBMC/system/players/dvdplayer/librtmp.dll
        # Archivos de Programa/XBMC/system/players/dvdplayer/librtmp.dll
        # Da igual porque special://xbmc/ apunta a la carpeta de instalación de XBMC
        libdir = xbmc.translatePath(os.path.join('special://xbmc/system/players/dvdplayer/', ''))
        filename = "librtmp.dll"
        plugintools.log("dir= "+libdir)
        filename = "librtmp.dll"
        shutil.copyfile(libdir + 'librtmp.dll', libdir + 'librtmp_bakup.dll')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform, libdir, filename)
                
    elif xbmc.getCondVisibility( "system.platform.osx" ):
        platform = "osx"
        # Var / Stash /Applications/ XBMC.app / Frameworks / librtmp.0.dylib
        libdir = xbmc.translatePath(os.path.join('special://xbmc/Frameworks/', ''))
        plugintools.log("dir= "+libdir)
        filename = "librtmp.0.dylib"
        shutil.copyfile(libdir + 'librtmp.0.dylib', libdir + 'librtmp.0.dylib')

        # fh = open(libdir + filename, "wb")
        bajalib(params, platform)        
    else:
        platform = "unknow"
        
    plugintools.log("plataforma= "+platform)

    


