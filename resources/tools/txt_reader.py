# -*- coding: utf-8 -*-
#------------------------------------------------------------
# TXT_Reader para beta.1
# Version 0.1 (18.10.2014)
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

import plugintools, requests
from __main__ import *

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")



def txt_reader(params):
    plugintools.log('[%s %s] TXT_reader %s' % (addonName, addonVersion, repr(params)))
    url=params.get("url")
    url = url.replace("txt:", "")

    if url.startswith("http") == True:  # Control para textos online
        plugintools.log("Iniciando descarga desde..."+url)
        h=urllib2.HTTPHandler(debuglevel=0)  # Iniciamos descarga...
        request = urllib2.Request(url)
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        filename = url.split("/")
        max_len = len(filename)
        max_len = int(max_len) - 1
        filename = filename[max_len]
        fh = open(playlists + filename, "wb")  #open the file for writing
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
        filename = url.split("/")
        inde = len(filename);print inde
        filename = filename[inde-1]
        txt_file = filename
        txt_path = playlists + txt_file
        TextBoxes("[B][COLOR lightyellow][I]playlists / [/B][/COLOR][/I] "+txt_file,txt_path)       
        
    else:
        txt_path = url
        TextBoxes("[B][COLOR lightyellow][I]EPG Infotext [/B][/COLOR][/I] ",txt_path)       
        


    

def TextBoxes(heading,anounce):
    class TextBox():
        """Thanks to BSTRDMKR for this code:)"""
            # constants
        WINDOW = 10147
        CONTROL_LABEL = 1
        CONTROL_TEXTBOX = 5

        def __init__( self, *args, **kwargs):
            # activate the text viewer window
            xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
            # get window
            self.win = xbmcgui.Window( self.WINDOW )
            # give window time to initialize
            xbmc.sleep( 500 )
            self.setControls()

        def setControls( self ):
            # set heading
            self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
            try:
                f = open(anounce)
                text = f.read()
            except: text=anounce
            self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
            return
    TextBox()



