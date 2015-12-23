# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para beta.1
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.1 (26.10.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)

import re,math,plugintools


def ioncube1(bodi):
 plugintools.log("bodi= "+bodi)
 p = re.compile(ur'<script language=javascript>(c=".*?)<\/script>')
 result=re.findall(p, bodi)
 p = re.compile(ur'eval\(unescape\(\'?"?"(.*?)\'?"?\)\)')
 result=re.findall(p, str(result))
 import urllib
 result = urllib.unquote_plus(str(result))
 p = re.compile(ur'c="([^"]+)')
 valc=re.findall(p, bodi);valc=valc[0];
 
 p = re.compile(ur'x\("([^"]+)')
 valx=re.findall(p, bodi);valx=valx[0];
 d="";int1 = 0;
 while int1 < len(valc):
  if int1%3==0:
   d+="%";
  else:
   d+=valc[int1];
  int1 += 1
 valc=urllib.unquote_plus(d)
 valt=re.compile('t=Array\(([0-9,]+)\)').findall(valc)[0];
 
 valz=valez(valx,valt);
 p=re.compile(ur'(getJSON\(|streamer|file|flash\'?"?,?\s?src)\'?"?\s?:?\s?\'?"?([^\'"]+)');vals=re.findall(p,valz);
 if len(vals)>=3:
  return vals
 else:
  print "!!! NO PARAMS !!!\n"+str(vals)+"\n"+valc
  return

def valez(valx,tS,b=1024,p=0,s=0,w=0):
		#print "TTTTSSSSS = "+tS
		l=len(valx); valt=tS.split(','); valr=[]
		#print "VALT = "+str(valt)
		for j in range(int(math.ceil(l/b)),0, -1):
			for i in range(min(l,b),0, -1):
				w |= int(valt[ord(valx[p])-48]) << s
				#print "WWW = "+str(w)
				p += 1
				if (s):
					valr.append(chr(165 ^ w & 255))
					#valu=chr(165 ^ w & 255);print "\n"+valu
					#print "VALR NOW = "+str(valr)
					w >>= 8
					s -= 2
				else:
					s = 6
			l -=1
		valr = ''.join(valr)
		#print "VALR FINAL = "+str(valr)
		return valr
#6ik3cdsewu48nt1
