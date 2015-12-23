# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Creado por CipQ para beta.1 
# Version 0.1 (18.03.2015)
#------------------------------------------------------------
from __main__ import *
baseurl='http://estaticos.elmundo.es/elmundo/television/guiatv/js_parrilla/';
burl='http://elmundo.es'
a=['Y2FuYWwx','Y2FuYWwy','YWNjaW9u','Y29tZWRpYQ==','ZGNpbmU=','cGx1cy1zZXJpZXM=','cGx1cy1idXp6','YW1j','aG9sbHl3b29k','Y2FsbGUxMw==','YXhu','YXhud2hpdGU=','Zm94','Zm94bGlmZQ==','dG50','YW50ZW5hMw==','bGFzZXh0YQ==','dGlraXRha2FzcG9ydHM=','bGlnYQ==','Z29sdHY=','ZnV0Ym9s','cGx1cy1nb2xm','bmF0Z2Vvd2lsZA==','bmlja2Vqcg==','ZGlzbmV5Y2hhbm5lbA==','ZGlzbmV5anVuaW9y']
def get_nepg(channel):
 epg_channel=[];sin='';cor='[COLOR white]';timestp=int(time.time());ahora=datetime.now();
 url=baseurl+str(channel)+'.js';data=plugintools.read(url)
 r='new\sPrograma\("([^"]+).*?(\d{10}).*?(\d{10})",\s"([^"]+).*?(\d{2}:\d{2}).*?(\/[^"]+)';#tit|ini|end|cat|hora|url
 event=plugintools.find_multiple_matches(data,r);
 for i in range(len(event)):
  if int(event[i][1])<int(timestp)<int(event[i][2]): j=i-1;sin=burl+event[i][5];print sin;
 sin=get_sin(sin,url);fan,syn=process_sin(sin);#procesar sin para sacar fanart,descripcion,categoria,etc
 for i in range(0,5,1):
  if i==1: cor='[COLOR green]'
  else: cor='[COLOR white]';
  epg_channel+=cor+event[j+i][4],event[j+i][0]+'[/COLOR]';
 return epg_channel,fan,syn
def get_sin(sin,url):
 request_headers=[];request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"]);request_headers.append(["Referer",url])
 data,response_headers=plugintools.read_body_and_headers(sin,headers=request_headers);
 for i in response_headers:
  if i[0]=='location': url=sin;sin=i[1]
 request_headers.append(["Referer",url]);data,response_headers=plugintools.read_body_and_headers(sin,headers=request_headers);
 return data
def process_sin2(sin): #solo para sacar fanart
 r='class="fichatecnica">.*?class="foto".*?<img\ssrc="([^"]+)';sin=plugintools.find_single_match(sin,r);
 return sin
def process_sin(sin):
 '''No esta implementado aun!!!'''
 datamovie={};fan='';syn='';cor1='[CR][COLORcyan]';cor2='[CR][COLORred]';cor3='[/COLOR]';cor4='[CR][CR][B][COLORgreen]';#class="fichatecnica">.*?class="foto".*?<img\ssrc="([^"]+).*?<ul>(.*?)<\/ul>.*?<h3>([^<]+).*?class="genero">([^<]+).*?<p>(.*?)<\/p>.*?<h3>([^<]+).*?<p>(.*?)<\/p> #fan|syno|titulo serie|cat|descripcion serie|titulo episode|descripcion episode
 try: r='class="fichatecnica">.*?class="foto".*?<img\ssrc="([^"]+)';fan=plugintools.find_single_match(sin,r);
 except: fan='';pass
 try:
  r='<ul>(.*?)<\/ul>';syno=plugintools.find_single_match(sin,r);
  r='>(.*?)<';synos=plugintools.find_multiple_matches(syno,r);synos=[i.rstrip('\n') for i in synos];synos=filter(None,synos);syn='';
  for i in range(len(synos)):
   if i%2==0: cor=cor2
   else: cor=cor1
   syn+=cor+synos[i]
  syn+=cor3;
 except: syn='';pass
 try: r='<h3>([^<]+)';tit=plugintools.find_single_match(sin,r);tit=tit.upper();sin=sin.replace('<h3>'+tit+'</h3>','')
 except: tit='';pass
 try: r='class="genero">([^<]+)';cat=plugintools.find_single_match(sin,r);
 except: cat='';pass
 try: r='<p>(.*?)<\/p>';titplot=plugintools.find_single_match(sin,r);sin=sin.replace('<p>'+titplot+'</p>','')
 except: titplot='';pass
 try: r='<h3>([^<]+)';epsd=plugintools.find_single_match(sin,r);
 except: epsd='';pass
 try: r='<p>(.*?)<\/p>';epsdplot=plugintools.find_single_match(sin,r);
 except: epsdplot='';pass
 #print syn,tit,titplot,cat,epsd,epsdplot;
 syn=cor4+tit+'[/B]'+syn+cor1+titplot+cor2+cat+cor2+epsd+cor1+epsdplot+cor3
 return fan,syn
def dict_ch_name(ch):
 print '****************  '+ch+'    ****************'
 if ch=="digitv-canal1": ch="250"
 elif ch=="digitv-canal2": ch=""
 elif ch=="digitv-accion": ch=""
 elif ch=="digitv-comedia": ch=""
 elif ch=="digitv-dcine": ch=""
 elif ch=="plus-series": ch=""
 elif ch=="plus-buzz": ch="688"
 elif ch=="amc": ch="481"
 elif ch=="digitv-hollywood": ch="61"
 elif ch=="digitv-calle13": ch="64"
 elif ch=="digitv-axn": ch="63"
 elif ch=="digitv-axnwhite": ch="512"
 elif ch=="digitv-fox": ch="202"
 elif ch=="digitv-foxlive": ch="660"
 elif ch=="digitv-tnt": ch="577"
 elif ch=="antena3": ch="2"
 elif ch=="lasexta": ch="510"
 elif ch=="tikitakasports": ch="tiki"
 elif ch=="liga" or ch=="digitv-liga": ch="746"
 elif ch=="goltv": ch="620"
 elif ch=="digitv-futbol": ch=""
 elif ch=="plus-golf": ch=""
 elif ch=="digitv-natgeowild": ch="681"
 elif ch=="digitv-nickejr": ch="687"
 elif ch=="digitv-disneychannel": ch="2091"
 elif ch=="digitv-disneyjunior": ch="292"
 if not ch: print '***  (No hay EPG in "elmundo.es",procesando con "epg_miguiatv") ***'
 fan='';syn='';epg_ch,fan,syn=get_nepg(ch);return epg_ch,fan,syn
def epg_nnow(params): #usado con otro modulo(epgtest) para sacar los numeros de los canales;solo sirve para actualizar si cambian...
 url='http://www.elmundo.es/elmundo/television/guiatv/';body=plugintools.read(url);
 r='<span id="nombre_canal_([^"]+)">([^<]+)<\/span>';w=plugintools.find_multiple_matches(body,r);print w;sys.exit()
 '''
 02:20:57 T:2132  NOTICE: [('689', '13tv'), ('163', '40 TV'), ('551', '7 Regi\xf3n de Murcia'), ('586', '8 Madrid TV'), ('243', '8tv'), ('492', 'A&E'), ('539', 'Al Jazeera English'), ('481', 'AMC'), ('32', 'Andaluc\xeda TV'), ('2', 'Antena 3'), ('704', 'Antena 3 Internacional'), ('580', 'Aprende Ingl\xe9s TV'), ('522', 'Arag\xf3n Televisi\xf3n'), ('63', 'AXN'), ('512', 'AXN White'), ('607', 'Azteca Internacional TV'), ('573', 'Baby TV'), ('155', 'Bar\xe7a TV'), ('208', 'BBC World'), ('196', 'Bloomberg'), ('665', 'Boing'), ('688', 'Buzz Rojo / Canal 18'), ('64', 'Calle 13'), ('250', 'Canal+ 1'), ('8', 'Canal 24 horas'), ('449', 'Canal 3/24'), ('183', 'Canal Cocina'), ('589', 'Canal de las Estrellas Europa'), ('582', 'Canal Extremadura TV'), ('746', 'Canal+ Liga'), ('698', 'Canal Panda'), ('30', 'Canal Sur'), ('31', 'Canal Sur 2'), ('566', 'Caracol TV'), ('296', 'Castilla - La Mancha TV'), ('656', 'Cazavisi\xf3n'), ('505', 'Clan TVE'), ('204', 'CNBC Europe'), ('203', 'CNN Internacional'), ('493', 'Comedy Central'), ('186', 'Cosmopolitan'), ('691', 'Crimen & Investigaci\xf3n'), ('496', 'Cuatro'), ('324', 'CyLTV'), ('572', 'Decasa'), ('515', 'Deluxe Music'), ('206', 'Deutsche Welle'), ('146', 'Discovery Channel'), ('475', 'Discovery MAX'), ('175', 'Disney Channel'), ('2091', 'Disney Channel +1'), ('292', 'Disney Junior'), ('174', 'Disney XD'), ('683', 'Disney XD +1'), ('697', 'Divinity'), ('709', 'Energy'), ('33', 'ETB 1'), ('34', 'ETB 2'), ('139', 'Euronews'), ('154', 'Eurosport'), ('491', 'Eurosport 2'), ('550', 'Extreme Sports'), ('506', 'FDF Telecinco'), ('202', 'FOX'), ('660', 'Fox Life'), ('140', 'Fox News'), ('547', 'France 24'), ('37', 'Galicia TV'), ('620', 'Gol TV'), ('148', 'Historia'), ('61', 'Hollywood'), ('671', 'Hollywood +1'), ('519', 'IB3'), ('654', 'Iberalia'), ('516', 'Intereconom\xeda TV'), ('639', 'Kiss tv'), ('3', 'La 1'), ('18', 'La 1 Catalunya'), ('690', 'La 1 HD'), ('4', 'La 2'), ('280', 'La 2 Catalunya'), ('643', 'La 8'), ('39', 'La Otra'), ('510', 'laSexta'), ('603', 'Libertad Digital TV'), ('338', 'Mezzo'), ('395', 'Motors tv'), ('469', 'MTV Dance'), ('161', 'MTV Hits'), ('627', 'MTV Music'), ('160', 'MTV Rocks'), ('151', 'National Geographic'), ('681', 'National Geographic Wild HD'), ('134', 'Natura'), ('410', 'Nautical Channel'), ('508', 'Neox'), ('200', 'Nickelodeon'), ('687', 'Nick Junior'), ('509', 'Nova'), ('135', 'Odisea'), ('716', 'Paramount Channel'), ('192', 'Playboy TV'), ('682', 'RT espa\xf1ol'), ('171', 'Sol M\xfasica'), ('501', 'Somos'), ('153', 'Sportman\xeda'), ('699', 'Sundance Channel'), ('541', 'Super 3'), ('520', 'Syfy'), ('59', 'TCM'), ('628', 'TCM +1'), ('1', 'Telecinco'), ('9', 'Teledeporte'), ('316', 'Tele Elx'), ('38', 'Telemadrid'), ('41', 'Televisi\xf3nCanaria'), ('201', 'TL Novelas'), ('577', 'TNT'), ('521', 'TPA'), ('43', 'TV3'), ('47', 'TV3CAT'), ('209', 'TV5 Monde'), ('416', 'TV Chile'), ('613', 'TV Colombia'), ('468', 'TVE Internacional'), ('667', 'TVE Internacional Asia'), ('36', 'TVG'), ('653', 'VE PLUS TV'), ('165', 'VH1'), ('705', 'VH1 Classic'), ('188', 'Viajar'), ('68', 'XTRM'), ('629', 'ZTV')]
 '''