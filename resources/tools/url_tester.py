# -*- coding: utf-8 -*-
#------------------------------------------------------------
# URL Tester on beta.1
# Version 0.1 (01.12.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

from __main__ import *

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
from resources.tools.server_rtmp import *

thumbnail = 'http://static.myce.com/images_posts/2011/04/kickasstorrents-logo.jpg'
#fanart = 'http://i.imgur.com/LaeHXnR.png'
fanart = 'https://yuq.me/users/19/529/lcqO6hj0XK.png'

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

def url_tester(params):
    url_test = plugintools.keyboard_input("", "Probar URL!")
    params["plot"]=url_test
    url_test = url_test.lower()
    if url_test == "":
        errormsg = plugintools.message("Arena+","Por favor, introduzca el canal a buscar")        
    else:
        plugintools.log('[%s %s] Probando URL... %s' % (addonName, addonVersion, url_test))
        url_test = url_test.strip()
        params["url"]=url_test
        title = multiparse_title('URL Tester', url_test, 'list')
        params["title"]=title
        if url_test.startswith("rtmp") == True:
            server_rtmp(params)
            print params
            plugintools.add_item(action="launch_rtmp", title=title+' [I][COLOR lightyellow]['+params.get("server")+'][/I][/COLOR]', url=url_test, folder=False, isPlayable=True)
        else:
            plugintools.add_item(action="launch_rtmp", title=title, url=url_test, folder=False, isPlayable=True)
            
            
        



