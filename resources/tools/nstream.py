# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para beta.1
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.0.5 (04.11.2014)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

#import re,urllib,urllib2,sys,time,msg,plugintools,ioncube
from __main__ import *
import inspect
cipqq='$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$';

def nstream2(url,ref,caster,res,script):
 #print cipqq,url,ref,caster,res,script;sys.exit();
 if caster == '9stream': nstr(url,ref,res)
 elif caster == 'verdirectotv': verdirectotv(url,ref,res)
 elif caster == 'jwplayer': jwplayer(url,ref,res,script)
 elif caster == '1broadcastlive': broadcastlive(url,ref,res)
 elif caster == 'iguide': iguide(url,ref,res)
 elif caster == 'ucaster': ucaster(url,ref,res)
 elif caster == 'mips': mips(url,ref,res)
 elif caster == 'ezcast': ezcast(url,ref,res)
 elif caster == 'tvonlinegratis': tvonlinegratis(url,ref,res)
 elif caster == 'm3u8': m3u8(url,ref,res)
 elif caster == 'dinozap': dinozap(url,ref,res);
 elif caster == 'popeoftheplayers.eu': popeoftheplayers(url,ref,res,script);
 elif caster == 'streamup': streamup(url,ref,res,script);
 elif caster == 'ustream': ustream(url,ref,res,script);
 elif caster == 'cndhlsstream': cndhlsstream(url,ref,res,script);
 elif caster == 'byetv': byetv(url,ref,res,script);
 elif caster == 'privatestream': privatestream(url,ref,res,script);
 else: print "\nNSCRIPT = "+str(script);print "\nURL = "+url;print "\nREFERER = "+str(ref);print "\nCASTER = "+str(caster);
 #print bodyy;sys.exit()

def privatestream(url,ref,res,script):
 from roja import new_frame;body,jar,resp,ref=new_frame(url,ref,'','','');pgurl=url;
 r='.*var a =\s*([^;]+).*var b =\s*([^;]+).*var c =\s*([^;]+).*var d =\s*([^;]+).*var f =\s*([^;]+).*var v_part =\s*\'([^\']+).*';
 w=plugintools.find_multiple_matches(body,r);rtmp='rtmp://'+str(int(w[0][0])/int(w[0][4]))+'.'+str(int(w[0][1])/int(w[0][4]))+'.'+str(int(w[0][2])/int(w[0][4]))+'.'+str(int(w[0][3])/int(w[0][4]))+w[0][5]+' swfUrl=http://privatestream.tv/js/jwplayer.flash.swf live=1 timeout=15 swfVfy=1 pageUrl='+pgurl;
 what_to_do(rtmp);
 
def jwplayer(url,ref,res,script):
 from roja import new_frame;p='file:\s?window\.atob\(\'([^\']+)';p=plugintools.find_single_match(script,p);media_url=p.decode('base64')
 what_to_do(media_url)
 	 
def byetv(url,ref,res,script):
 from roja import new_frame;res=res[0][2];
 if 'channel.php' in res:file='file=([^\&]+)';res='http://www.byetv.org/embed.php?a='+plugintools.find_single_match(res,file)+'&id=&width=653&height=410&autostart=true&strech=';body,jar,resp,ref=new_frame(res,url,'','');
 swf='new\sSWFObject\(\'?"?([^\'"]+)';swf='http://www.byetv.org'+plugintools.find_single_match(body,swf)
 p='(token|file|streamer)\',\s\'([^\']+)';match=plugintools.find_multiple_matches_multi(body,p);
 media_url=match[2][1]+" playpath=file:"+match[1][1]+" swfUrl="+swf+" live=1 token="+match[0][1]+" timeout=15 swfVfy=1 pageUrl="+url;
 what_to_do(media_url)
 	 
def streamingfreetv(url,ref,res):
 bodi=curl_frame(url,ref,'');ref=url;p='(width|height|channel)=\'?([^,\']+)';p=plugintools.find_multiple_matches(bodi,p);
 url='http://privado.streamingfreetv.net/embed/embed.php?channel='+p[2][1]+'&w='+p[0][1]+'&h='+p[1][1];bodi=curl_frame(url,ref,'');
 p='<param\sname=\'(movie|flashvars)\'\svalue=\'([^\']+)';p=plugintools.find_multiple_matches(bodi,p);
 rtmp='rtmp://188.165.213.105:1935/redirect?'+p[1][1].split('&')[1].split('=',1)[1].split('?')[1]
 w=rtmp+' playpath='+p[1][1].split('&')[0].split('=')[1]+' timeout=15 swfUrl='+p[0][1].lower()+' live=true pageUrl='+url;
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 		
def cndhlsstream(url,ref,res,script):
 #xbmcUtils.showBusyAnimation()
 from roja import new_frame;body,jar,resp,ref=new_frame(url,url,'','');r='document\.write\(\s?unescape\(\s?\'([^\']+)';
 r=urllib.unquote_plus(plugintools.find_single_match(body,r));p='src="([^"]+)';purl=plugintools.find_single_match(r,p);
 p='src="([^\?]+).*?streamer=([^\&]+).*?file=([^\&]+)';p=plugintools.find_multiple_matches(r,p);
 w=p[0][1]+' playpath='+p[0][2]+' swfUrl='+p[0][0]+' live=true pageUrl='+purl
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 		
def streamup(url,ref,res,script):
 w='rtmp://167.114.157.89/app playpath='+res[0][2].split('rooms/')[1].split('/plugins')[0].lower()+' swfUrl=https://streamup.com/assets/StreamupVideoChat.swf timeout=15 pageUrl='+url
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 	
def ustream(url,ref,res,script):
 #print("streamup\n%s\n%s\n%s"%(url,res,ref))
 #http://cdngw.ustream.tv/Viewer/getStream/1/%s.amf
 w='http://iphone-streaming.ustream.tv/uhls/'+res+'/streams/live/iphone/playlist.m3u8'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 	
def popeoftheplayers(url,ref,res,script):
 from roja import new_frame;purl=urlparse.urlsplit(url);burl='%s://%s/';burl=burl%(purl[0],purl[1]);p='(id|width|height)=\'?([^,\']+)';
 p=plugintools.find_multiple_matches(res[0][0],p);url='http://popeoftheplayers.eu/player4.php?id='+p[0][1]+'&width'+p[1][1]+'&height='+p[2][1];
 body,jar,resp,ref=new_frame(url,burl,'','');p='(x-shockwave-flash"\sdata|flashvars"\svalue)="([^"]+)';p=plugintools.find_multiple_matches(body,p);
 print body,url,ref,burl,jar;sys.exit()
 plpath=p[1][1].split('&amp;')[0].split('=')[1];rtmp=p[1][1].split('&amp;')[1].split('=')[1];swf=p[0][1];
 w=rtmp+' playpath='+plpath+' timeout=15 swfUrl='+swf+' live=true pageUrl='+url;print w
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 
def broadcastlive(url,ref,res):
 bodi=curl_frame(url,ref,'');ref=url;p='(width|height|channel)=\'?([^,\']+)';p=plugintools.find_multiple_matches(bodi,p);
 url='http://1broadcastlive.com/embed/embed.php?channel='+p[2][1]+'&w='+p[0][1]+'&h='+p[1][1];bodi=curl_frame(url,ref,'');
 p='<param\sname=\'(movie|flashvars)\'\svalue=\'([^\']+)';p=plugintools.find_multiple_matches(bodi,p);
 w='rtmp://188.165.213.105:1935/redirect?'+p[1][1].split('&')[1].split('=',1)[1].split('?')[1]+' playpath='+p[1][1].split('&')[0].split('=')[1]+' timeout=15 swfUrl='+p[0][1].lower()+' live=true pageUrl='+url;
 #66.85.133.160
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 
def dinozap(url,ref,res):
 url=res[0][2]+'&width=680&height=390&autostart=true';body='';body=curl_frame(url,ref,body);
 reff=url;url=plugintools.find_single_match(body,'iframe\ssrc="([^"]+)');
 for i in range(1,10):
  k=url;body=curl_frame(url,reff,'');
  scrpt='document\.write\(unescape\(\'([^\']+)';scrpt=plugintools.find_single_match(body,scrpt);
  tok='securetoken([^\n]+)';tok=plugintools.find_single_match(body,tok);
  try: hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
  except: i-=1;
  diov='var\s(sUrl|cod1)\s=\s\'([^\']+)';diov=plugintools.find_multiple_matches(body,diov);
  Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));jquery = '%s?callback=jQuery17049106340911455604_%s&v_cod1=%s&v_cod2=%s&_=%s';
  jurl=jquery%(hidd[3][1].decode('base64'),Epoc_mil,hidd[1][1],hidd[2][1],Epoc_mil);r='"result\d{1}":"([^"]+)';p='plugintools.find_multiple_matches(body,r)';
  body=curl_frame(jurl,k,'');x=eval(p)[0];
  if x=='not_found': print 'try '+str(i)+' : '+x;
  else: print 'try '+str(i)+' : OK :)';break;
 if x=='not_found': eval(nolink);sys.exit();
 swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(eval(p)[1].replace('\\',''),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=eval(p)[1].replace('\\','')+' app='+app+' playpath='+eval(p)[0]+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
 
def nstr(url,ref,res):
 #print str(res);
 p1 = re.compile(ur'embed\/=?\'?"?([^\'"\&,;]+)')
 p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)')
 p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)')
 f1=re.findall(p1, str(res));f2=re.findall(p2, str(res));f3=re.findall(p3, str(res));#res=list(set(f));
 w=f2[0];h=f3[0];c=f1[0];
 url='http://www.9stream.com/embedplayer.php?width='+w+'&height='+h+'&channel='+c+'&autoplay=true';body='';#
 bodi=curl_frame(url,ref,body)
 #print "\nURLXXX = "+url+"\nREFXXX = "+ref#+"\n"+bodi
 tkserv='';strmr='';plpath='';swf='';vala='';
 #AHORA VAN SIN IONCUBE,desactivo la llamada al ioncube de abajo!!!
 try: vals=ioncube.ioncube1(bodi)
 except: vals=ioncube.noioncube(bodi);pass
 #print tkserv+"\n"+strmr+"\n"+plpath+"\n"+swf#print valz;#
 tkserv=vals[0][1];strmr=vals[1][1].replace("\/","/");plpath=vals[2][1].replace(".flv","");swf=vals[3][1];
 ref=url;url=tkserv;bodi=curl_frame(url,ref,body);
 p='token":"([^"]+)';token=plugintools.find_single_match(bodi,p);print token
 media_url = strmr+'/'+plpath+' swfUrl='+swf+' token='+token+' live=1 timeout=15 swfVfy=1 pageUrl='+ref
 #media_url ='http://cpliga.nmp.hls.emision.dof6.com/hls/live/201767/channelpc2/index.m3u8'
 #media_url ='http://cpliga.nmp.hls.emision.dof6.com/hls/live/201767/channelpc2/20141028T074633-05-15185.ts'
 plugintools.play_resolved_url(media_url)
 print "MEDIA URL="+media_url
 
def ezcast(url,ref,res):
 #print "NEDEFINIT";sys.exit()
 p = re.compile(ur'(width|height|channel)=\'?"?([^\,\'"]+)');par=re.findall(p,str(res));#print par;
 w=par[0][1];h=par[1][1];c=par[2][1];ref=url;url='http://www.ezcast.tv/embedded/'+c+'/1/'+w+'/'+h;
 body='';#print url+ref,res;sys.exit()
 bodi=curl_frame(url,ref,body);#print bodi;sys.exit()
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ezcast.tv'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);
 p = re.compile(ur'\&?=([^\&]+)');flvs=re.findall(p,flashvars);id=flvs[0];c=flvs[1];
 lb='http://ezcast.tv:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
'''
Si hay mas de un caster,se tiene que cambiar el "estado" del item (de playable=True a False y crear un popup para eligir opcion!!!
 #listitem.setProperty('IsPlayable', 'false');msg="Elige stream:\nezcast";
 #xbmc.Notification("CipQ-TV","ezcast\n9stream",300)
 #return media_url
'''
 
 
def iguide(url,ref,res):
 #clodfront protect,print resp in try_to_parse_as_new
 #vipracing tiene otro referer no el que sale aqui
 #print sys._getframe().f_code.co_argcount,locals().keys(),sys._getframe().f_code.co_varnames
 #print("\n$[ %s ]$\n%s\n%s\n%s"%(sys._getframe().f_code.co_name.upper(),url,ref,res));sys.exit();
 from roja import new_frame;refi=ref;body,jar,resp,ref=new_frame(res[0][2],ref,'','');url=plugintools.find_single_match(body,'src=\'([^\']+)');
 body,jar,resp,ref=new_frame(url,refi,'',jar);
 p = re.compile(ur'(\$\.getJSON\(\'?"?.*?)<\/script>', re.DOTALL);
 pars=re.findall(p,body);pars=str(pars[0]);pars=pars.replace("\n","").replace("\t","");
 tokserv=plugintools.find_single_match(str(pars),'getJSON\(\'?"?([^\'"]+)');
 strmr=plugintools.find_single_match(str(pars),'streamer\'?"?:\s?\'?"?([^\'"]+)');
 plpath=plugintools.find_single_match(str(pars),'file\'?"?:\s?\'?"?([^\.]+)');
 if plpath=="'": plpath=res;
 swf=plugintools.find_single_match(str(pars),'flash\'?"?,\s?src\'?"?:\s?\'?"?([^\'"]+)');
 body='';tok=curl_frame(tokserv,url,body);tok=plugintools.find_single_match(str(tok),'token":"([^"]+)');
 media_url = str(strmr)+' playpath='+str(plpath)+' flashver='+urllib.quote_plus('WIN 14,0,0,176')+' swfUrl='+str(swf)+' timeout=15 live=1 pageUrl='+url+' token='+tok
 what_to_do(media_url)

def iguide2(url,ref,res):
 print url,res,ref
 body='';body=curl_frame(url,ref,body);
 p = re.compile(ur'(\$\.getJSON\(\'?"?.*?)<\/script>', re.DOTALL)
 pars=re.findall(p,body);pars=str(pars[0]);pars=pars.replace("\n","").replace("\t","");
 tokserv=plugintools.find_single_match(str(pars),'getJSON\(\'?"?([^\'"]+)');
 strmr=plugintools.find_single_match(str(pars),'streamer\'?"?:\s?\'?"?([^\'"]+)');
 plpath=plugintools.find_single_match(str(pars),'file\'?"?:\s?\'?"?([^\.]+)');
 if plpath=="'": plpath=res;
 swf=plugintools.find_single_match(str(pars),'flash\'?"?,\s?src\'?"?:\s?\'?"?([^\'"]+)');
 body='';tok=curl_frame(tokserv,url,body);tok=plugintools.find_single_match(str(tok),'token":"([^"]+)');
 media_url = str(strmr)+' playpath='+str(plpath)+' swfUrl='+str(swf)+' live=1 pageUrl='+url+' token='+tok
 print media_url
 plugintools.play_resolved_url(media_url)

def mips(url,ref,res):
 #print "RESSSSSSSSS";print res;sys.exit()
 #print url+ref;body='';sys.exit()
 p = re.compile(ur'(width|height|channel)=\'?"?([^\,\'"]+)');par=re.findall(p,str(res));#print par;sys.exit()
 w=par[0][1];h=par[1][1];c=par[2][1];ref=url;url='http://www.mips.tv/embedplayer/'+c+'/1/'+w+'/'+h;
 body='';#print url+ref;sys.exit()
 bodi=curl_frame(url,ref,body);#print bodi
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.mips.tv'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);
 p = re.compile(ur'\&?.*?=([^\&]+)');flashvars=re.findall(p,flashvars);id=flashvars[0];c=flashvars[1];
 lb='http://mips.tv:1935/loadbalancer?'+id;lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' timeout=14 swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
 print "MEDIA URL="+media_url

def tvonlinegratis(url,ref,res):
 print "NSTREAM"+url+ref;body='';
 bodi=curl_frame(url,ref,body);
 try:
  ref=url;p = re.compile(ur'src="(.*tvonlinegratis[^"]+)');url=re.findall(p,bodi);url=str(url[0])
  bodi=curl_frame(url,ref,body);
 except:pass
 try:
  ref=url;url=plugintools.find_single_match(bodi,'href="([^"]+)');
  bodi=curl_frame(url,ref,body);#
 except:pass
 f='fid="([^"]+)';w='width=([^;]+)';h='height=([^;]+)';
 f=plugintools.find_single_match(bodi,f);w=plugintools.find_single_match(bodi,w);h=plugintools.find_single_match(bodi,h);
 ref=url;url='http://www.tvonlinegratis.mobi/player/'+ f +'.php?width='+w+'&height='+h;
 try:
  bodi=curl_frame(url,ref,body);print bodi
 except:pass
 ref=url;url='src="(.*?tvonlinegratis[^"]+)';url=plugintools.find_single_match(bodi,url);
 bodyy=curl_frame(url,ref,body);#print bodi
 from plt import jscalpe
 jscalpe(bodyy,url,ref)

def verdirectotv(url,ref,res):
 try:bodi=curl_frame(url,ref,'');ref=url;url=plugintools.find_single_match(bodi,'src="(http:\/\/(tv\.verdirectotv\.org|www\.dinostream\.pw)\/channel\.php\?file=[^"]+)');
 except:pass
 try: businessapp1(url[0],ref,bodi);
 except:
  try: businessapp2(url[0],ref,bodi);
  except:
   try: businessapp3(url[0],ref,bodi);
   except:pass

def businessapp3(url,ref,bodi):
 bodi=curl_frame(url,ref,'');url=plugintools.find_single_match(bodi,'iframe\ssrc="([^"]+)');
 body=curl_frame(url,ref,'');r='function\sgetURL03(.*?)setStream\(data\);';
 try: hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
 except:pass
 try:body=plugintools.find_single_match(body,r);
 except:eval(nolink);sys.exit();
 try:r='[\'|"]result\d{1}[\'|"]\s?:\s?[[](.*?)[]]';p=plugintools.find_multiple_matches(body,r);
 except:pass
 if not p:
  try:r='var\s(.*?)\s=\s?[\'|"]([^\'"]+)';p=plugintools.find_multiple_matches(body,r);#jq_cback(p,url);#jquery callback method!!!
  except:sys.exit();
  jq_cback(p,url);
 else:var_1_2_b64(p,url);#var1,var2 base64 method!!!
def jq_cback(p,url):
 Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));jquery = '%s?callback=jQuery1705415557138621807_%s&v_cod1=%s&v_cod2=%s&_=%s';
 jurl=jquery%(b64_error(p[2][1]).decode('base64'),Epoc_mil,urllib.quote_plus(p[0][1]),urllib.quote_plus(p[1][1]),Epoc_mil);
 r='"result\d{1}":"([^"]+)';p='plugintools.find_multiple_matches(body,r)';body=curl_frame(jurl,url,'');#jQuery17036659089173190296
 swfUrl='http://downloads.b88.org/flex.swf?id=1402202_0&ln=es';app=plugintools.find_single_match(eval(p)[1].replace('\\',''),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=eval(p)[1].replace('\\','')+' app='+app+' playpath='+eval(p)[0]+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+url+' live=1 timeout=15'
 #print("\n[%s]\n%s\n%s\n%s"%(sys._getframe().f_code.co_name,eval(p)[1].replace('\\',''),w,url));sys.exit()
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
def var_1_2_b64(p,url):
 r='var\s('+p[0]+'|'+p[1]+')\s?=\s?[\'|"](.*?)[\'|"]';p=plugintools.find_multiple_matches(body,r);
 swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(b64_error(p[1][1]).decode('base64'),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=b64_error(p[1][1]).decode('base64')+' app='+app+' playpath='+b64_error(p[0][1]).decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+url+' live=1 timeout=15'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
   
def b64_error(b64_str):
 missing_padding=4-len(b64_str)%4
 if missing_padding: b64_str+=b'='*missing_padding;return b64_str
  
def businessapp2(url,ref,bodi):
  bodi=curl_frame(url,ref,'');reff=url;url=plugintools.find_single_match(bodi,'<iframe src="([^"]+)');k=url;body=curl_frame(url,reff,'');
  hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
  swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));
  app=plugintools.find_single_match(hidd[2][1].decode('base64').replace('\\',''),'1735\/([^"]+)');
  q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
  w=hidd[2][1].decode('base64').replace('\\','')+' app='+app+' playpath='+hidd[1][1].decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
  #print w;sys.exit();
  if w: plugintools.play_resolved_url(w);sys.exit();
  else: eval(nolink);sys.exit();
  
def businessapp1(url,ref,bodi):
 #print("\n[%s]\n%s\n%s\n%s"%(sys._getframe().f_code.co_name,ref,caster,script));sys.exit()
 bodi=curl_frame(url,ref,'');reff=url;url=plugintools.find_single_match(bodi,'<iframe src="([^"]+)');#print cipqq,url,reff,bodi;sys.exit();
 for i in range(1,10):
  k=url;body=curl_frame(url,reff,'');
  scrpt='document\.write\(unescape\(\'([^\']+)';scrpt=plugintools.find_single_match(body,scrpt);
  tok='securetoken([^\n]+)';tok=plugintools.find_single_match(body,tok);
  try: hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
  except: i-=1;
  diov='var\s(sUrl|cod1)\s=\s\'([^\']+)';diov=plugintools.find_multiple_matches(body,diov);
  Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));jquery = '%s?callback=jQuery1705112804693635553_%s&v_cod1=%s&v_cod2=%s&_=%s';
  jurl=jquery%(hidd[3][1].decode('base64'),Epoc_mil,urllib.quote_plus(hidd[1][1]),urllib.quote_plus(hidd[2][1]),Epoc_mil);
  r='"result\d{1}":"([^"]+)';p='plugintools.find_multiple_matches(body,r)';
  body=curl_frame(jurl,k,'');x=eval(p)[0];
  if x=='not_found': print 'try '+str(i)+' : '+x,body;
  else: print 'try '+str(i)+' : OK :)';break;
 if x=='not_found': eval(nolink);sys.exit();
 swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(eval(p)[1].replace('\\',''),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=eval(p)[1].replace('\\','')+' app='+app+' playpath='+eval(p)[0]+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
  
def ucaster(url,ref,res):
 p1 = re.compile(ur'channel=?\'?"?([^\'"\&,;]+)');f1=re.findall(p1, str(res));
 p2 = re.compile(ur'width=?\'?"?([^\'"\&,;]+)');f2=re.findall(p2, str(res));
 p3 = re.compile(ur'height=?\'?"?([^\'"\&,;]+)');f3=re.findall(p3, str(res));
 c=f1[0];w=f2[0];h=f3[0];
 url='http://www.ucaster.eu/embedded/'+c+'/1/'+w+'/'+h;body=''
 #print "UCASTER body="+bodi;sys.exit();
 bodi=curl_frame(url,ref,body)
 p ='SWFObject\(\'?"?([^\'"]+)';swf='http://www.ucaster.eu'+plugintools.find_single_match(bodi,p);
 p = 'FlashVars\'?"?,?\s?\'?"?([^\'"]+)';flashvars=plugintools.find_single_match(bodi,p);print flashvars;
 p = re.compile(ur'\&?.*?=([^\&]+)');flashvars=re.findall(p,flashvars);print flashvars;id=flashvars[0];c=flashvars[1];
 lb='http://www.ucaster.eu:1935/loadbalancer';lb=plugintools.read(lb);lb=plugintools.find_single_match(lb,'redirect=(.*)');
 #print lb;sys.exit()
 #rtmp://109.123.126.66/live/ playpath=canal89?id=76120 swfUrl=http://www.ucaster.eu/static/scripts/fplayer.swf swfVfy=1 conn=S:OK live=true pageUrl=
 media_url = 'rtmp://'+lb+'/live/ playpath='+c+'?id='+id+' swfUrl='+swf+' swfVfy=1 conn=S:OK live=true pageUrl='+url
 plugintools.play_resolved_url(media_url)
 print "MEDIA URL="+media_url
  
def m3u8(url,ref,res):
 #print res;
 plugintools.play_resolved_url(str(res))
		
def curl_frame(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	#print "HEADERS:N";print response_headers
	return body
	
def what_to_do(w):#se puede poner return o play_resolved_url segun la necesidad
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();