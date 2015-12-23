# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para beta.1
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.5 (04.11.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

import os,sys,urlparse,urllib,urllib2,re,shutil,zipfile,inspect,types

import xbmc,xbmcgui,xbmcaddon,xbmcplugin,plugintools
'''
#from inspect import getmembers, isfunction
print "WISE\n"
functions_list = [o for o in getmembers(unwise) if isfunction(o[1])]
print str(functions_list)
print getmembers(unwise)
for i in dir(unwise): print i
for i in getmembers(unwise): print i
print [key for key in locals().keys()
       if isinstance(locals()[key], type(sys)) and not key.startswith('__')]
'''
#print unwise



def shsp(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	plugintools.add_item( action="shsp3" , title="[COLOR=orange]Shedule[/COLOR]" , url=url ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
	plugintools.add_item( action="shsp5" , title="[COLOR=orange]List[/COLOR]" , url="http://showsport-tv.com/",thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
	plugintools.add_item( action="shsp4" , title="[COLOR=orange]Embed[/COLOR]" , url="http://showsport-tv.com/update/embed.html" ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
	
def shsp3(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body
	#print "START="+params.get("url")
	import re
	p = re.compile(ur'(<a\sclass="mac".*?<\/div>)', re.DOTALL)
	matches = re.findall(p, data)
	#del matches[0]
	for match in matches:
		#url = scrapedurl.strip()
		#print match
		p = re.compile(ur'<img\ssrc=\'?"?([^\'"]+).*?<span\sclass="mactext">([^<]+).*?\s(<div.*?<\/div>)', re.DOTALL)
		links=re.findall(p, match)
		for imgs,titles,divs in links:
		 title=titles.replace("&nbsp; ","")
		 title=title.replace("&nbsp;","|")
		 #print divs
		 plugintools.add_item( action="shsp2" , title=title , url=divs ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
	
def shsp5(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body;
	#print "START="+params.get("url")
	import re
	p = re.compile(ur'<a\sclass="menuitem\ssubmenuheader".*?>([^<]+)(.*?)<\/div>', re.DOTALL)
	matches = re.findall(p, data)
	#del matches[0]
	for match,links in matches:
		url="http://showsport-tv.com/"+links
		plugintools.add_item( action="shsp6" , title=match , url=url ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )

def shsp6(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	import re
	p = re.compile(ur'href="([^"]+).*?>([^<]+)', re.DOTALL)
	a=re.findall(p,url);
	for links,channels in a:
		url="http://showsport-tv.com/"+links
		plugintools.add_item( action="shsp7" , title=channels , url=url ,thumbnail=thumb ,fanart=thumb , isPlayable=True, folder=False )


def shsp7(params):
	url = params.get("url")
	url=url.replace("/ch/","/update/").replace("php","html");
	ref="http://showsport-tv.com/"
	thumb = params.get("thumbnail")
	title = params.get("title")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",ref])
	bodyy,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	if bodyy.find("googlecode"):
	 print "GOING XUSCACAMUSCA"
	 p = re.compile(ur'id="([^"]+).*?src="([^"]+)', re.DOTALL)
	elif bodyy.find("iguide"):
	 p = re.compile(ur'var\s?id\s?=\s?([^;]+).*?src="?\'?([^\'"]+)', re.DOTALL)
	 print "GOING IGUIDE"
	else:
	 print "UNKNOWN"
	pars=re.findall(p,bodyy);ref=url;res='';
	for id,script in pars:
	 if script.find("xuscacamusca"):
	  ref=url
	  url='http://xuscacamusca.se/gen_h.php?id='+id+'&width=100%&height=100%'
	  peak2(params)
	 elif script.find("iguide"):
	  url=script+"1009&height=460&channel="+id+"&autoplay=true"
	  from nstream import iguide2
	  iguide2(url,ref,res)
	 else:
	  print "NO SCRIPT"

def shsp4(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#print body
	import re
	p = re.compile(ur'<div class="match1"(.*?\s+.*?)\$\(\s"\#m\d"\s\)', re.DOTALL)
	a=re.findall(p,body);
	for match in a:
		#print "\nFFFFFF";print match;
		p = re.compile(ur'img\ssrc="([^"]+).*?div\sclass="name">([^<]+)', re.DOTALL)
		foldr=re.findall(p,match)
		for img,catg in foldr:
		 #print "\n"+img;print "\n"+catg;
		 thumb="http://showsport-tv.com/"+img
		 title=catg
		 plugintools.add_item( action="shsp1" , title=title , url=match ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )
		 #plugintools.add_item( action="" , title=title , url=str(match) ,thumbnail=thumb ,fanart=thumb , isPlayable=False, folder=True )

def shsp1(params):
	url = params.get("url")
	thumb = params.get("thumbnail")
	import re
	p = re.compile(ur'<div\sclass="name">([^<]+).*?fid=\&quot;([^\&]+).*?v_width=([^;]+).*?v_height=([^;]+).*?src=\&quot;([^\&]+)', re.DOTALL)
	foldr=re.findall(p,url)
	for name,fid,w,h,jsrc in foldr:
		 thumb=thumb
		 title=name
		 url='http://showsport-tv.com/update/'+ fid +".html"
		 plugintools.add_item( action="peaktv2" , title=title , url=url ,thumbnail=thumb ,fanart=thumb , isPlayable=True, folder=False )
	
def shsp2(params):
	divs = params.get("url")
	thumb = params.get("thumbnail")
	import re
	p = re.compile(ur'href=\'?"?([^\'"]+).*?>([^<]+)')
	link=re.findall(p, divs)
	#print link
	for lin in link:
	 url="http://showsport-tv.com"+lin[0].replace("/ch/","/update/").replace("php","html");
	 title=lin[1];print url+"\n"+title
	 plugintools.add_item( action="peaktv2" , title=title , url=url , isPlayable=True, folder=False )
		
def peaktv(params):
	#plugintools.get_localized_string(21)
	url = params.get("url")
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body
	#print "START="+params.get("url")
	p = 'href="([^<]*)'
	matches = plugintools.find_multiple_matches_multi(data,p)
	del matches[0]
	for scrapedurl in matches:
		url = scrapedurl.strip()
		#print url
		title = plugintools.find_single_match(url,'>(.*?:[^:]+)')
		#title = title.replace("\xe2","a".encode('iso8859-16'));
		title = title.replace("\xe2","a");
		title = title.replace("\xc3","t");
		title = title.replace("\xe0","f");
		title = title.replace("\xfc","u");
		title = title.replace("\xdb","s");
		title = title.replace("\x15f","s");
		'''
		#print title.decode("utf-8")
		print unicode(title,"iso8859-16")
		'''
		canal = plugintools.find_single_match(url,'php\?([^"]+)')
		url = 'http://peaktv.me/Live.php/?'+canal.strip()
		if 'DigiSport1' in str(url):
		 thumb='http://www.digisport.ro/img/sigla_digisport1.png'
		elif 'DigiSport2' in str(url):
		 thumb='http://itutorial.ro/wp-content/uploads/digi_sport2.png'
		elif 'DigiSport3' in str(url):
		 thumb='http://www.sport4u.tv/web/logo/sport/digi_sport3_ro.png'
		elif 'DolceSportHD' in str(url):
		 thumb='http://static.dolcetv.ro/img/tv_sigle/sigle_black/116.png'
		elif 'DolceSport1' in str(url):
		 thumb='http://static.dolcetv.ro/img/tv_sigle/sigle_black/101.png'
		elif 'DolceSport2' in str(url):
		 thumb='http://static.dolcetv.ro/img/tv_sigle/sigle_black/107.png'
		elif 'DolceSport3' in str(url):
		 thumb='http://static.dolcetv.ro/img/tv_sigle/sigle_black/134.png'
		elif 'DolceSport4' in str(url):
		 thumb='http://static.dolcetv.ro/img/tv_sigle/sigle_black/247.png'
		elif 'EuroSport2HD' in str(url):
		 thumb='http://www.sport4u.tv/web/logo/sport/eurosport-2.png'
		elif 'EuroSport1HD' in str(url):
		 thumb='http://4.bp.blogspot.com/-k50Qb45ZHGY/UrMCA2zRoGI/AAAAAAAAStA/Dj6sF0dHcs8/s1600/790px-Eurosport_logo.svg.png'
		elif 'LookPlusHD' in str(url):
		 thumb='http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Look_Plus_HD.png/100px-Look_Plus_HD.png'
		elif 'LookTVHD' in str(url):
		 thumb='http://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Look_TV_HD_logo.png/100px-Look_TV_HD_logo.png'
		else:
		 thumb='http://frocus.net/images/logotv/Sport-ro_HD.jpg'
		 print thumb
		fanart = thumb
		plugintools.add_item( action="peaktv2" , title=title , url=url ,thumbnail=thumb ,fanart=fanart , isPlayable=True, folder=False )

def peaktv2(params):
	msg = "Buscando enlace\nespere,porfavor... "
	#plugintools.message("CipQ-TV",msg)
	url = params.get("url")
	print "START="+url
	title = params.get("title")
	thumb = params.get("thumbnail")
	ref=url
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers,timeout=30)
	#os.environ["HTTP_PROXY"]=Proxy
	data=body
	#print "START="+data
	p = '<script type="text\/javascript">id="([^"]+).*?width="([^"]+).*?height="([^"]+).*?src="([^"]+)'
	matches = plugintools.find_multiple_matches_multi(data,p)
	#print "START=";print matches
	for id,width,height,cast in matches:
		#url = 'http://xuscacamusca.se/?id='+id+'&width='+width+'&height='+height.strip()
		url = 'http://fa16bb1eb942c5c48ac3cd66aff4c32f2a015b1af198c14b88.com/gen_s.php?id='+id+'&width='+width+'&height='+height.strip()
		#print "START="+url
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",ref])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers,timeout=10)
	data=body
	#print "START="+data
	p='src=\'?"?([^\/]+)\/jwplayer\.js\.pagespeed'
	swf = plugintools.find_single_match(data,p)
	#print "SWF";print swf
	swf='http://xuscacamusca.se/'+swf+'/jwplayer.flash.swf'
	print "SWF = "+swf
	p = ';eval(.*?)<\/script>'
	mat = plugintools.find_multiple_matches_multi(data,p)
	print "wisenx="+str(mat)
	'''
	try:
	 print "wisenx="+str(mat)
	 swfobj=str(mat)
	 #print "swfobj="+swfobj
	 import unwise
	 decr = unwise.unwise_process(data)
	except:
		print "Link outdated"
		msg = "Enlace caducado,solo estara activo durante el partido ... "
		plugintools.message("CipQ-TV",msg)
	'''
	if mat:
	 swfobj=mat[1]
	 #print "swfobj="+swfobj
	 import unwise
	 decr = unwise.unwise_process(data)
	else:
	 print "Link outdated"
	 msg = "Enlace caducado,solo estara activo durante el partido ... "
	 plugintools.message("CipQ-TV",msg)
	 return
	#print "DECR="+decr
	p = ",file:'(.*?)'"
	rtmp = plugintools.find_single_match(decr,p)
	print "PLPATH="+rtmp
	media_url = rtmp+' swfUrl='+swf+' live=1 timeout=15 swfVfy=1 pageUrl='+url
	#plugintools.add_item( action="play_resolved_url" , title=title , url=media_url ,thumbnail=thumb , isPlayable=True, folder=False )
	plugintools.play_resolved_url(media_url)
	print media_url

def pltptc(params):
    url = params.get("url")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    data=body
    print "START="+params.get("url")
    if params.get("title")=="PonTuCanal" :
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://canalesgratis.me/canales/"
	 pattern3 = ".php"
    else :
	 pattern1 = 'popUp\(\'([^\']+).*src="([^"]+)'
	 pattern2 = "http://verdirectotv.com/canales/"
	 pattern3 = ".html"
    matches = plugintools.find_multiple_matches_multi(data,pattern1)
    for scrapedurl, scrapedthumbnail in matches:
		#thumbnail = urlparse.urljoin( params.get("url") , scrapedthumbnail )
		thumbnail = scrapedthumbnail
		url = urlparse.urljoin( params.get("url") , scrapedurl.strip() )
		rep = str.replace(url,pattern2,"")
		title = str.replace(rep,pattern3,"").capitalize()
		plot = ""
		msg = "Resolviendo enlace ... "
		uri=url
		rref = 'http://verdirectotv.com/carrusel/tv.html'
		uri = uri+'@'+title+'@'+rref
		#plugintools.log("URI= "+uri)
		pattern = "\s+"
		import re
		uri = re.sub(pattern,'',uri)
		uri = uri.encode('base64')
		url = 'http://localhost/000/ptc2xbmc.php?page='+uri
		url = re.sub(pattern,'',url)
		plugintools.log("LSP URL= "+url)
		url = 'plugin://plugin.video.live.streamspro/?url='+plugintools.urllib.quote_plus(url)+'&mode=1&name='+plugintools.urllib.quote_plus(title)
		#plugintools.log("LINK= "+url)
		plugintools.add_item( action="runPlugin" , title=title , plot=plot , url=url ,thumbnail=thumbnail , isPlayable=False, folder=True )
		
def vipracing0(params):
#plugintools.log("cipq.webpage "+repr(params))#print list of pages (PLT,PTC)
# Fetch video list from website feed
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"])
	url = params.get("url")
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#plugintools.log("data= "+body)
	thumb="http://cs301412.vk.me/v301412640/5ab5/fJUqz4EDdTM.jpg"
	pattern1 = '"shortcut":"([^"]*)'
	match = plugintools.find_multiple_matches_multi(body,pattern1)
	match = sorted(list(set(match)))
	#match = sorted(match.items(), key=lambda x: x[1])
	for opcions in match:
	 title = "Vip Racing "+str(opcions.replace("opcion-",""))
	 title = title.capitalize()
	 url = "http://vipracing.tv/channel/"+opcions
	 #url = str(url.split())
	 url = ", ".join(url.split())
	 #plugintools.log("TITLE:"+url)
	 plugintools.add_item(action="vipracing2" ,title=title ,url=url ,thumbnail=thumb ,fanart=thumb ,isPlayable=True, folder=False )

def vipracing2(params):
        msg = "Resolviendo enlace ... "
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"])
	request_headers.append(["Referer","http://vipracing.tv"])
	ref = 'http://vipracing.tv'
	url = params.get("url");ref=url
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	data = body.replace('window\.location\.replace\(ncr\)','')
	'''
	array('freelivetv','byetv','9stream','castalba','castamp','direct2watch','kbps','flashstreaming','cast247','ilive','freebroadcast','flexstream','mips','veemi','yocast','yukons','ilive','iguide','ucaster','ezcast','maxstream','dinozap','janjua','tutelehd')
	'''
	pattern = '<script type="text\/javascript" src="(.*direct2watch[^"]+)'
	uri = plugintools.find_single_match(body,pattern)
	pattern = 'embed\/([^\&]+).*?width=([^\&]+).*?height=([^\&]+)'
	match = plugintools.find_multiple_matches_multi(uri,pattern)
	for id,width,height in match:
	 plugintools.log("ID= "+id)
	 plugintools.log("WIDTH= "+width)
	 plugintools.log("HEIGHT= "+height)
	data = plugintools.read(uri)
	p = 'src=\'?"?([^\'"]+)'
	uri = plugintools.find_single_match(data,p)
	plugintools.log("URI= "+uri)
	url=uri
	#print "URL = "+url;print "REF = "+ref;
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",ref])
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#print "List : ", request_headers;
	bodi = body
	import ioncube
	vals=ioncube.ioncube1(bodi)
	#print tkserv+"\n"+strmr+"\n"+plpath+"\n"+swf#print valz;#
	print "URL = "+url;print "REF = "+ref;
	tkserv=vals[0][1];strmr=vals[1][1].replace("\/","/");plpath=vals[2][1].replace(".flv","");swf=vals[3][1];
	ref=url;url=tkserv;bodyi=[];bodyy='';urli=[];
	from plt import curl_frame
	bodi=curl_frame(url,ref,body,bodyi,bodyy,urli);
	p='token":"([^"]+)';token=plugintools.find_single_match(bodi,p);#print token
	media_url = strmr+'/'+plpath+' swfUrl='+swf+' token='+token+' live=1 timeout=15 swfVfy=1 pageUrl='+ref
	#media_url ='http://cpliga.nmp.hls.emision.dof6.com/hls/live/201767/channelpc2/index.m3u8'
	#media_url ='http://cpliga.nmp.hls.emision.dof6.com/hls/live/201767/channelpc2/20141028T074633-05-15185.ts'
	plugintools.play_resolved_url(media_url)
	print media_url
	'''
	p = '(\$\.getJSON\(|streamer\'?"?:?\s?|file\'?"?:?\s?|flash\'?"?,\s?src:?\s?)\'?"?([^\'"]+)'
	match = plugintools.find_multiple_matches_multi(body,p)
	print str(match);
	tokserv = match[0][1]
	strmr = match[1][1].replace("\\","")
	plpath = match[2][1].replace(".flv","")
	swf = match[3][1]
	#print strmr
	request_headers=[]
	request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
	request_headers.append(["Referer",uri])
	body,response_headers = plugintools.read_body_and_headers(tokserv, headers=request_headers)
	p=':\'?"?([^\'"]+)'
	tok=plugintools.find_single_match(body,p)
	media_url=strmr+"/"+plpath+" swfUrl="+swf+" live=1 token="+tok+" timeout=15 swfVfy=1 pageUrl="+uri
	plugintools.play_resolved_url(media_url)
	print media_url
	'''
	 
def dolce(params):
	plugintools.get_localized_string(21)
#plugintools.log("cipq.webpage "+repr(params))#print list of pages (PLT,PTC)
# Fetch video list from website feed
	#data = plugintools.read( params.get("url") )
	url = 'http://www.dolcetv.ro/tv-live'
	data = plugintools.read(url)
	#plugintools.log("DATA:"+data)
	
    #returnheaders = plugintools.read_body_and_headers( params.get("url") )
    #data = plugintools.read_body_and_headers( params.get("url") )
    #for tup, tur, other in returnheaders:
		#plugintools.log("TUPLE:"+tup+"STR:"+tur+"OTHER:"+other)
    #plugintools.log("bug tuple " + data(tuple(tmp.split(', '))))
	pattern1 = '<img\s+class="thumb".*?alt="([^"]+).*?\s+<span class="thumbtvlive_over"><\/span>\s+<img\s+class="thumbtvlive_logo"\s+src="([^"]+)'
	pattern2 = "\/([0-9]{1,3})\.png"
	pattern3 = "thumb-([^\/]+)"#wigs,title
	match = plugintools.find_multiple_matches_multi(data,pattern1)
	match = sorted(list(set(match)))
	for wigs,sigle in match:
	 #plugintools.log("WIGS:"+wigs)
	 #plugintools.log("SIGLE:"+sigle)#print list of url
	 title = plugintools.find_single_match(wigs,pattern3)
	 title = title.capitalize()
	 thumb = sigle
	 id = plugintools.find_single_match(sigle,pattern2)
	 pattern4 = 'href=.*?'+id+'.*?class="acum">([^<]+)'
	 pattern5 = 'href=.*?'+id+'.*?class="next">([^<]+)'
	 #acum = plugintools.find_single_match(data,pattern4)
	 #next = plugintools.find_single_match(data,pattern5)
	 #title=acum
	 url = 'http://www.dolcetv.ro/service/play/index/id/'+id+'/category/0/type/live-tv/editionId/0/module_name/androidtablet'
	 url=url.strip()
	 show="ACUM1"
	 episode="ACUM2"
	 extra="ACUM3"
	 page="ACUM4"
	 info_labels="ACUM5"
	 plugintools.add_item( action="dolce2" ,title=title ,url=url ,thumbnail=wigs ,fanart=thumb , page=page,isPlayable=False, folder=True )

def dolce2(params):
        msg = "Resolviendo enlace ... "
	url = params.get("url")
	data = plugintools.read(params.get("url"))
	data = data.replace('&amp;','&')
	data = data.replace('&quot;',"'")
	#plugintools.log("LSS URL= "+url)
	thumbnail=params.get("thumbnail")
	title = params.get("title")
	plot=params.get("plot")
	pattern = '"high quality stream name":"([^"]+).*?token-low":"([^"]+).*?token-high":"([^"]+)'
	match = plugintools.find_multiple_matches_multi_multi(data,pattern)
	for name,low,high in match:
	 plugintools.log("NAME= "+name)
	 #plugintools.log("HIGH= "+high)
	 plugintools.add_item( action="" , title=title , plot=plot , url=url ,thumbnail=thumbnail , isPlayable=False, folder=False )

def lsstv(params):
	 thumbnail=params.get("thumbnail");
	 fanart=params.get("fanart");
	 data = plugintools.read("http://www.livesportstreams.tv/sidebar.php?top=1&type=1&l=es");
	 grups='<span\sid="span_link_sidebar.*?(\(.*?\)).*?<\/span>';grups=plugintools.find_multiple_matches(data,grups);grups=list(set(grups));grup=[];
	 for i in range(1,len(grups)):
	  a=grups[i].replace("1, ","").split("'");grup+=([a[1],a[7],a[9]]);
	 j=0
	 for j in range(len(grup)):
	  if j%3==0:
	   sport=grup[j];
	  elif j%3==1:
	   link="http://www.livesportstreams.tv/events.php?top=1&type=1&l=es&"+grup[j];
	   plugintools.add_item( action="lsstv1" , title=sport , url=link ,thumbnail=thumbnail , isPlayable=False, folder=True )
	   #print "sport="+grup[j];j+=1;print "link="+grup[j];j+=1;print "nrevnt="+grup[j];j+=1;
	  else:
	   sport=sport+' ('+grup[j]+'partidos)';


def lsstv1(params):
	 data=plugintools.read(params.get("url"));
	 pattern1 = 'onClick=\'showLinks\("event_", (.*?<img alt=".*?style="width: 40px;">.*?letter-spacing: 0px;">.*?<td rowspan=2 style="font-size:11px; font-style: italic; text-align: right;" title=\'[^\']+.)'
	 pattern2 = '"([^"]+).*<img alt="([^"]+).*style="width: 40px;">([^<]+).*?letter-spacing: 0px;">([^<]+).*<td rowspan=2 style="font-size:11px; font-style: italic; text-align: right;" title=\'([^\']+)'
	 pattern3 = ""
	 match = plugintools.find_multiple_matches_multi_multi(data,pattern1)
	 #for (i,id) in enumerate(match):
	 match = sorted(list(set(match)))#array_unique !!!
	 for ids in match:
		'''
		thumbnail = "http://cdn-a.streamshell.net/images/icons/48x48px.png"
		#plugintools.log("TITLE"+ids)#print list of channels
		url = "http://www.livesportstreams.tv/es/player.php?e=" + ids + "&s=13&c=4"
		url = url.strip()
		plot = ""
		title = ids.capitalize()
		'''
		matches = plugintools.find_multiple_matches_multi(ids,pattern2)
		for id, champ, ora, meci, lang in matches:
			thumbnail = "http://cdn-a.streamshell.net/images/icons/48x48px.png"
			url = "http://www.livesportstreams.tv/es/links.php?links=1&id=" + id
			url = url.strip()
			plugintools.log("URL:"+url)#print list of url
			#champ = champ.replace('futbol','') 
			mec = "[COLOR=green]"+ ora + "[COLOR=yellow] : " + meci.upper() + " ([COLOR=red]" + lang.lower() + "[/COLOR][/COLOR][/COLOR]) :" + champ
			title = mec
			plot = ""
			#plugintools.log("cipq.webpage_play "+title)#print list of channels
			#uri = plugintools.find_single_match(data,rep)
			# Appends a new item to the xbmc item list
			plugintools.add_item( action="lsstv2" , title=title , plot=plot , url=url ,thumbnail=thumbnail , isPlayable=True, folder=True )


def lsstv2(params):
        msg = "Resolviendo enlace ... "
	ref = params.get("url")
	data = plugintools.read( params.get("url") )
	data = data.replace('&amp;','&')
	data = data.replace('&quot;',"'")
	#plugintools.log("LSS URL= "+data)
	thumbnail=params.get("thumbnail")
	title = params.get("meci")
	plot=params.get("plot")
	pattern = '\?(e=[^\'"]+)'
	match = plugintools.find_multiple_matches_multi_multi(data,pattern)
	match = sorted(list(set(match)))
	i=1
	for id in match:
		url = "http://www.livesportstreams.tv/es/player.php?" + id + "@" + ref
		url=url.strip()
		plugintools.log("LSS URL= "+url)
		title = "Link " + str(i)
		i+=1
		#xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
		#params['action'] = 'runPlugin'
		#plugintools.play_resolved_url(url)
		#xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')
		#xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(item=url)
		plugintools.add_item( action="lsstv3" , title=title , plot=plot , url=url ,thumbnail=thumbnail , isPlayable=True, folder=False )


def lsstv3(params):
	splitted = params.get("url").split('@')
	page=splitted[0]
	ref =splitted[1]
	plugintools.log("FIRST URL= "+page)
	plugintools.log("REFERER= "+ref)
	title=params.get("title")
	plot=params.get("plot")
	thumbnail=params.get("thumbnail")
	'''
	msg = "Pasando enlace a SpDevil... "
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('CipQ TV', msg, 1 , art+'icon.png'))#quitar art+...
	url = 'plugin://plugin.video.SportsDevil/?item=catcher=streams&title='+title+'&url='+page+'&videoTitle='+title+'&director=arena+&genre=Live TV&referer='+ref+'&definedIn=&type=rss&icon='+thumbnail+'&mode=1'
	url=url.strip()
	#url=urllib.quote_plus("url")
	plugintools.log("LINK= "+str(url))
	xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
	ref = 'http://www.livesportstreams.tv/es/main.php'
	http://www.castasap.pw/public/embed.php?id=b2bbaf4db04a87f50bf659b5df1939f9a805698fa2d5a0ce0ff8c45807033ee4&cid=1413903241&eid=5446206223e03717132813&rid=54467440a19a7&hon=1&w=768&h=432
	Referer: http://www.livesportstreams.tv/es/player.php?e=5446206223e03717132813&s=13&c=51
	
	http://37.48.85.217:43911/ls/51/index.m3u8?c=1eca49fd84273d860fa4783f036c2f280df754b3ac57c7d1a5206e5b95bc52b7&cid=1413903241&eid=5446206223e03717132813
	Referer:http://www.castasap.pw/public/embed.php?id=b2bbaf4db04a87f50bf659b5df1939f9a805698fa2d5a0ce0ff8c45807033ee4&cid=1413903241&eid=5446206223e03717132813&rid=54467440a19a7&hon=1&w=768&h=432
	'''
	pattern = 'document.write\(\'<iframe\s+frameborder\=0 marginheight\=0\s+marginwidth\=0\s+scrolling\=no\s+src=\'?"?([^\'"]+)';
	data = plugintools.read(page)
	url = plugintools.find_single_match(data,pattern)
	url = unescape(url).encode("utf-8")
	ref=page
	print "CASTURL:"+url
	print "CASTREF:"+ref
	txt='\.([^\/]+)';txt=plugintools.find_single_match(url,txt);
	#plugintools.log("LINK EMBED= "+url)
        request_headers=[]
        request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"])
        request_headers.append(["Referer",ref])#"http://www.livesportstreams.tv/es/main.php"
        body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	#print "<br>"+body
	p='(swfobject\.embedSWF\("|st":?\s?|file\'?"?:?\s?|flash\'?"?,\s?src:?\s?)\'?"?([^\'"]+)'
	match = plugintools.find_multiple_matches_multi(body,p)
	#print match;
	strmr = match[0][1].replace("\\","")
	plpath = match[1][1].replace(".flv","")
	swf = match[2][1]
	print swf;
	print "STRM="+strmr
	print "PATH="+plpath
	a='http://cdn-b.streamshell.net/swf/uppod-hls.swf';b='http://www.'+txt+'/st/'+txt+'.txt';txt=a+'?st='+b+'&file='+plpath;print txt
	#plugintools.play_resolved_url(txt);sys.exit()
	#data = plugintools.read(txt);print data;
	#'(http.*?index\.m3u8.*)'
	splitted = url.split('?')
	splitte = splitted[1].split('=')
	id=splitte[1].split('&cid')
	id = id[0]
	#id = unescape(id[0]).encode("utf-8")
	#id = xpodd(id)
	print "XPODD="+id
	cid=splitte[2].split('&')
	eid=splitte[3].split('&')
	rid=splitte[4].split('&')
	url = 'http://37.48.85.217:43911/ls/58/index.m3u8?c='+id+'&cid='+cid[0]+'&eid='+eid[0]
	url='http://37.48.82.65:43911/ls/95/index.m3u8?c=500c4c9a8b7c345a15fe37e17bda7f2a0c673b920dd3ac41d54e6c23c642d241'+'&cid='+cid[0]+'&eid='+eid[0]
	plugintools.play_resolved_url(url);sys.exit()
	url = url.strip()
	#plugintools.play_resolved_url(url);sys.exit();
	print "URL="+url
	print "REF="+ref
	rtmplink="rtmp://37.48.85.217:43911/ls/58/"+strmr+" playpath="+plpath+" swfUrl="+swf+" live=true timeout=30 swfVfy=1 pageUrl="+unescape(ref).encode("utf-8")+" Conn=S:OK --live"
	plugintools.play_resolved_url(rtmplink)
	'''
	request_headers=[]
	request_headers.append(["Referer",ref])
	print request_headers
	body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
	print body
	'''

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def xpodd(param):
    #-- define variables
    loc_3 = [0,0,0,0]
    loc_4 = [0,0,0]
    loc_2 = ''
    #-- define hash parameters for decoding
    dec = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    hash1 = ["Z", "v", "6", "W", "m", "y", "g", "X", "b", "o", "V", "d", "k", "t", "M", "Q", "u", "5", "D", "e", "J", "s", "z", "f", "L", "="]
    hash2 = ["a", "G", "9", "w", "1", "N", "l", "T", "I", "R", "7", "2", "n", "B", "4", "H", "3", "U", "0", "p", "Y", "c", "i", "x", "8", "q"]


    #-- decode
    for i in range(0, len(hash1)):
        re1 = hash1[i]
        re2 = hash2[i]

        param = param.replace(re1, '___')
        param = param.replace(re2, re1)
        param = param.replace('___', re2)

    i = 0
    while i < len(param):
        j = 0
        while j < 4 and i+j < len(param):
            loc_3[j] = dec.find(param[i+j])
            j = j + 1

        loc_4[0] = (loc_3[0] << 2) + ((loc_3[1] & 48) >> 4);
        loc_4[1] = ((loc_3[1] & 15) << 4) + ((loc_3[2] & 60) >> 2);
        loc_4[2] = ((loc_3[2] & 3) << 6) + loc_3[3];

        j = 0
        while j < 3:
            if loc_3[j + 1] == 64:
                break
            try:
                loc_2 += unichr(loc_4[j])
            except:
                pass
            j = j + 1

        i = i + 4;

    return loc_2

def find_multiple_matches_multi(text,pattern):
    matches = re.findall(pattern,text, re.MULTILINE)
    return matches	
