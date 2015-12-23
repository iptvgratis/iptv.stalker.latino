# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Creado por CipQ para beta.1 
# Version 0.1 (18.03.2015)
#------------------------------------------------------------
from __main__ import *
baseurl='http://www.entutele.com/canal/';#'http://www.entutele.com/programacion/totalplay/';
burl='http://www.entutele.com'
def get_tepg(channel):
 epg_channel=[];sin='';cor='[COLOR white]';timestp=int(time.time());ahora=datetime.now();
 url=baseurl+str(channel);request_headers=[];request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"]);data,response_headers=plugintools.read_body_and_headers(url,headers=request_headers);
 r='<table class="canal_horario">(.*?)<\/table>';data=plugintools.find_single_match(data,r);
 r='class="\s?past">.*?<th>([^<]+).*?href="([^"]+).*?>([^<]+).*?href="([^"]+).*?>([^<]+).*?<div class="showinfo hide">(.*?)<\/div>';
 eventpast=plugintools.find_multiple_matches(data,r);#eventpast=eventpast[0][0],eventpast[0][2]
 r='<tr class="now\s?">.*?<th>([^<]+).*?href="([^"]+).*?>([^<]+).*?href="([^"]+).*?>([^<]+).*?<div class="showinfo hide">.*?"tags">([^<]+).*?>(.*?)<br';
 eventnow=plugintools.find_multiple_matches(data,r);#hora|url|tit|urlwhen|titwhen|cat|details
 try:
  r='>(.*?)<';syn=plugintools.find_multiple_matches(eventnow[0][6]+'<',r);syn=[x.replace('\n','') for x in syn if x<>''];syn=list(filter(None,syn));
  sin='[CR][COLORred]'+syn[0]+'[/COLOR][CR]'.join(syn[1:]);
 except: sin='';
 print sin
 r='<tr class="\s?">.*?<th>([^<]+).*?href=".*?>([^<]+)';
 eventnext=plugintools.find_multiple_matches(data,r);
 epg_channel+=eventpast[0][0],eventpast[0][2].replace('\n',''),'[COLORgreen]'+eventnow[0][0],eventnow[0][2].replace('\n','')+'[/COLOR]',eventnext[0][0],eventnext[0][1].replace('\n',''),eventnext[1][0],eventnext[1][1].replace('\n','');fan='';print epg_channel;#print epg_channel,fan,syn;sys.exit();#
 return epg_channel,fan,sin
def dict_chn_name(ch):
 print '****************  '+ch+'    ****************'
 if ch=="AZTECA 13": ch=""
 elif ch=="AZTECA NOTICIAS": ch=""
 elif ch=="ANIMAL PLANET": ch="animal-planet"
 elif ch=="AZTECA 7": ch="azteca-7"
 elif ch=="BANDAMAX": ch="bandamax"
 elif ch=="BBC ENTERTAINMENT": ch="bbc-entertainment"
 elif ch=="BOOMERANG": ch="boomerang"
 elif ch=="CANAL TRECE": ch="el-trece"
 elif ch=="CANAL 5 SD": ch="canal-5"
 elif ch=="CARTOON NETWORK": ch="cartoon-network"
 elif ch=="CBEEBIES": ch="cbeebies"
 elif ch=="COMEDY CENTRAL HD" or ch=="COMEDY CENTRAL": ch="comedy-central"
 elif ch=="CANAL AXN" or ch=="AXN": ch="axn"
 elif ch=="CINEMAX": ch="cinemax-w"
 elif ch=="CASA CLUB HD": ch="casa-club"
 elif ch=="CINECANAL": ch="cinecanal-hd"
 elif ch=="CANAL A E" or ch=="A E": ch="ae"
 elif ch=="CIVILIZATION": ch="discovery-civilization"
 elif ch=="DE PELICULA": ch="de-pelicula-hd"
 elif ch=="DISCOVERY CHANNEL": ch="discovery-channel"
 elif ch=="DISTRITO COMEDIA": ch="distrito-comedia"
 elif ch=="DISNEY JUNIOR": ch="disney-jr"
 elif ch=="DISNEY CHANNEL": ch="disney-channel"
 elif ch=="DISCOVERY KIDS": ch="discovery-kids"
 elif ch=="DISNEY XD": ch="disney-xd"
 elif ch=="ESPN 2": ch="espn-2"
 elif ch=="ESPN 3": ch="espn-3"
 elif ch=="ESPN": ch="espn"
 elif ch=="E ENTERTAINMENT": ch="e-entertainment-television"
 elif ch=="FORO TV HD" or ch=="FORO TV": ch="foro-tv"
 elif ch=="FOX CINEMA": ch="fox-cinema"
 elif ch=="FOX CLASSICS": ch="fox-classics"
 elif ch=="FOX 1": ch="fox-1-hd"
 elif ch=="FOX MOVIES": ch="fox-movies-hd"
 elif ch=="FOX LIFE": ch="fox-life"
 elif ch=="FOX FAMILY HD" or ch=="FOX FAMILY": ch="fox-family-w" #fox-family-e
 elif ch=="FOX ACTION HD" or ch=="FOX ACTION": ch="fox-action-hd"
 elif ch=="FOX": ch="fox-1-w" #fox-1-hd
 elif ch=="FOX SPORT 2" or ch=="fox sport 2": ch="fox-sports-2"
 elif ch=="FOX SPORT" or ch=="fox sport": ch="fox-sports"
 elif ch=="FX": ch="fx-hd"
 elif ch=="GLITZ": ch="glitz"
 elif ch=="GOURMET": ch="el-gourmet"
 elif ch=="GOLDEN EDGE": ch="golden-edge"
 elif ch=="GOLDEN": ch="golden-hd"
 elif ch=="HISTORY": ch="history-hd"
 elif ch=="I SAT": ch="isat"
 elif ch=="INFINITO HD": ch="infinito"
 elif ch=="ID INVESTIGATION DISCOVERY": ch="investigacion-discovery"
 elif ch=="MTV": ch="mtv"
 elif ch=="MTV LIVE": ch="mtv-live-hd"
 elif ch=="NAT GEO WILD": ch="natgeo-wild-hd"
 elif ch=="NATIONAL GEOGRAPHIC": ch="natgeo"
 elif ch=="NICK": ch="nick-hd"
 elif ch=="NICK JR": ch="nick-jr"
 elif ch=="NICKELODEON HD": ch="nickelodeon-nick"
 elif ch=="NICKTOONS": ch="nick-hd" #?
 elif ch=="ONCE MEXICO": ch="once-tv"
 elif ch=="ONCE TV": ch="once-tv"
 elif ch=="PROYECTO 40": ch="proyecto-40"
 elif ch=="SONY": ch="sony-hd"
 elif ch=="SPACE": ch="space-hd"
 elif ch=="STUDIO UNIVERSAL": ch="studio-universal"
 elif ch=="SYFY HD": ch="syfy"
 elif ch=="TLC": ch="tlc"
 elif ch=="TRUTV HD": ch="trutv-hd"
 elif ch=="TCM": ch="tcm"
 elif ch=="TELEHIT": ch="telehit-hd"
 elif ch=="THE FILM ZONE": ch="the-film-zone-hd"
 elif ch=="TLNOVELAS": ch="tlnovelas"
 elif ch=="TBS": ch="tbs"
 elif ch=="TBS VERY FUNNY": ch="tbs"
 elif ch=="TNT": ch="tnt"
 elif ch=="TOONCAST": ch="tooncast"
 elif ch=="TIIN": ch="tiin"
 elif ch=="UNIVERSAL CHANNEL": ch="universal-channel"
 elif ch=="UNIVERSAL CHANNEL": ch="universal-channel"
 elif ch=="VH1": ch="vh1-hd"
 elif ch=="CANAL 40 TV AZTECA": ch=""
 elif ch=="CANAL 7 MEXICO": ch=""
 elif ch=="BIO": ch=""
 elif ch=="H H": ch=""
 elif ch=="THE WALKING DEAD": ch=""
 elif ch=="STV": ch=""
 elif ch=="TMZ WARNER BROS": ch=""
 elif ch=="WARNER BROS": ch=""
 elif ch=="TEST": ch=""
 elif ch=="FUTURAMA TV": ch=""
 elif ch=="LOS SIMPSONS": ch=""
 elif ch=="MGM": ch=""
 if not ch: print '***  (No hay EPG in "entutele",procesando con "...") ***'
 fan='';syn='';epg_ch,fan,syn=get_tepg(ch);return epg_ch,fan,syn
#def epg_tnow(params): dict_chn_name('ESPN');
def epg_tnow1(params): #usado con otro modulo(epgtest) para sacar los numeros de los canales;solo sirve para actualizar si cambian...
 request_headers=[];request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"]);
 data,response_headers=plugintools.read_body_and_headers('http://www.entutele.com/programacion/totalplay/',headers=request_headers);
 r='href="([^"]+)">\n([^<]+)<.*?canalimg';w=plugintools.find_multiple_matches(data,r);print w;sys.exit();#http://www.entutele.com/canal/canal-4-guadalajara
 '''
 01:59:30 T:2164  NOTICE: [ ('/canal/canal-2-hd', 'Canal 2 HD '), ('/canal/foro-tv-hd', 'Foro TV HD '), ('/canal/canal-5-hd', 'Canal 5 HD '), ('/canal/azteca-7', 'Azteca 7 '), ('/canal/once-tv', 'Once TV '), ('/canal/el-trece', 'El Trece '), ('/canal/proyecto-40', 'Proyecto 40 '), ('/canal/canal-22', 'Canal 22 '), ('/canal/cadena-3', 'Cadena 3 '), ('/canal/television-mexiquense', 'Televisi\xc3\xb3n Mexiquense '), ('/canal/canal-2', 'Canal 2 '), ('/canal/foro-tv', 'Foro TV '), ('/canal/canal-5', 'Canal 5 '), ('/canal/gala-tv', 'Gala TV '), ('/canal/teleformula', 'TeleF\xc3\xb3rmula '), ('/canal/efektotv', 'EfektoTV '), ('/canal/multimedios-monterrey', 'Multimedios Monterrey '), ('/canal/canal-capital-21', 'Canal Capital 21 '), ('/canal/sony-hd', 'Sony HD '), ('/canal/warner-hd', 'Warner HD '), ('/canal/universal-hd', 'Universal HD '), ('/canal/fx-hd', 'FX HD '), ('/canal/axn-hd', 'AXN HD '), ('/canal/trutv-hd', 'TruTV HD '), ('/canal/comedy-central-hd', 'Comedy Central HD '), ('/canal/az-corazon', 'Az Coraz\xc3\xb3n '), ('/canal/fox', 'Fox '), ('/canal/sony', 'Sony '), ('/canal/bbc-entertainment', 'BBC Entertainment '), ('/canal/warner-channel', 'Warner Channel '), ('/canal/e-entertainment-television', 'E! Entertainment Television '), ('/canal/universal-channel', 'Universal Channel '), ('/canal/syfy', 'SyFy '), ('/canal/fx', 'FX '), ('/canal/ae', 'A&amp;E '), ('/canal/axn', 'AXN '), ('/canal/hbo-2', 'HBO 2 '), ('/canal/unicable', 'Unicable '), ('/canal/mundo-fox', 'Mundo Fox '), ('/canal/investigacion-discovery', 'Investigaci\xc3\xb3n Discovery '), ('/canal/infinito', 'Infinito '), ('/canal/el-gourmet', 'El Gourmet '), ('/canal/glitz', 'Glitz '), ('/canal/fox-life', 'Fox Life '), ('/canal/distrito-comedia', 'Distrito Comedia '), ('/canal/tbs', 'TBS '), ('/canal/casa-club', 'Casa Club '), ('/canal/tlnovelas', 'Tlnovelas '), ('/canal/az-mundo', 'Az Mundo '), ('/canal/telemundo', 'Telemundo '), ('/canal/comedy-central', 'Comedy Central '), ('/canal/discovery-kids', 'Discovery Kids '), ('/canal/cbeebies', 'CBeebies '), ('/canal/disney-jr', 'Disney Jr '), ('/canal/nick-jr', 'Nick Jr '), ('/canal/disney-channel', 'Disney Channel '), ('/canal/nick-hd', 'Nick HD '), ('/canal/nickelodeon-nick', 'Nickelodeon (Nick) '), ('/canal/cartoon-network', 'Cartoon Network '), ('/canal/disney-xd', 'Disney XD '), ('/canal/boomerang', 'Boomerang '), ('/canal/tiin', 'TIIN '), ('/canal/tooncast', 'Tooncast '), ('/canal/hd-theater', 'HD Theater '), ('/canal/history-hd', 'History HD '), ('/canal/natgeo-wild-hd', 'NatGeo Wild HD '), ('/canal/discovery-world-hd', 'Discovery World HD '), ('/canal/h2', 'H2 '), ('/canal/discovery-channel', 'Discovery Channel '), ('/canal/animal-planet', 'Animal Planet '), ('/canal/home-and-health', 'Home and Health '), ('/canal/history-channel', 'History Channel '), ('/canal/natgeo', 'NatGeo '), ('/canal/lifetime', 'Lifetime '), ('/canal/discovery-science', 'Discovery Science '), ('/canal/discovery-civilization', 'Discovery Civilization '), ('/canal/discovery-turbo', 'Discovery Turbo '), ('/canal/tlc', 'TLC '), ('/canal/wobi-tv', 'WOBI TV '), ('/canal/tv-unam', 'TV UNAM '), ('/canal/hbo-w', 'HBO (W) '), ('/canal/hbo-plus-w', 'HBO Plus (W) '), ('/canal/hbo-signature', 'HBO Signature '), ('/canal/hbo-family-e', 'HBO Family (E) '), ('/canal/hbo-plus-e', 'HBO Plus (E) '), ('/canal/max', 'MAX '), ('/canal/max-hd', 'Max HD '), ('/canal/max-prime-w', 'Max Prime (W) '), ('/canal/max-prime-e', 'Max Prime (E) '), ('/canal/fox-1-hd', 'Fox 1 HD '), ('/canal/fox-action-hd', 'Fox Action HD '), ('/canal/fox-movies-hd', 'Fox Movies HD '), ('/canal/fox-1-w', 'Fox 1 (W) '), ('/canal/fox-cinema', 'Fox Cin\xc3\xa9ma '), ('/canal/fox-action-w', 'Fox Action (W) '), ('/canal/fox-family-w', 'Fox Family (W) '), ('/canal/fox-classics', 'Fox Classics '), ('/canal/paramount-channel', 'Paramount Channel '), ('/canal/cinecanal-hd', 'Cinecanal HD '), ('/canal/tnt-hd', 'TNT HD '), ('/canal/golden-hd', 'Golden HD '), ('/canal/the-film-zone-hd', 'The Film Zone HD '), ('/canal/de-pelicula-hd', 'De Pel\xc3\xadcula HD '), ('/canal/amc-hd', 'AMC HD '), ('/canal/space-hd', 'Space HD '), ('/canal/fox-action-e', 'Fox Action (E) '), ('/canal/fox-family-e', 'Fox Family (E) '), ('/canal/fox-movies', 'Fox Movies '), ('/canal/cinecanal-w', 'Cinecanal (W) '), ('/canal/cinemax-w', 'Cinemax (W) '), ('/canal/tnt', 'TNT '), ('/canal/golden', 'Golden '), ('/canal/golden-edge', 'Golden Edge '), ('/canal/the-film-zone-w', 'The Film Zone (W) '), ('/canal/de-pelicula', 'De Pel\xc3\xadcula '), ('/canal/amc', 'AMC '), ('/canal/space', 'Space '), ('/canal/studio-universal', 'Studio Universal '), ('/canal/europa-europa', 'Europa Europa '), ('/canal/filmarts', 'Film&amp;Arts '), ('/canal/isat', 'I.Sat '), ('/canal/tcm', 'TCM '), ('/canal/golf-channel', 'Golf Channel '), ('/canal/nfl-network-hd', 'NFL Network HD '), ('/canal/tdn-hd', 'TDN HD '), ('/canal/espn-hd', 'ESPN HD '), ('/canal/espn-3', 'ESPN 3 '), ('/canal/fox-sports-hd', 'Fox Sports HD '), ('/canal/fox-sports-2-hd', 'Fox Sports 2 HD '), ('/canal/espn', 'ESPN '), ('/canal/espn-2', 'ESPN 2 '), ('/canal/fox-sports', 'Fox Sports '), ('/canal/fox-sports-2', 'Fox Sports 2 '), ('/canal/fox-sports-3', 'Fox Sports 3 '), ('/canal/nfl-network', 'NFL Network '), ('/canal/aym-sports', 'AyM Sports '), ('/canal/milenio-tv', 'Milenio TV '), ('/canal/cnn-en-espanol', 'CNN en espa\xc3\xb1ol '), ('/canal/fox-news', 'Fox News '), ('/canal/tve', 'TVE '), ('/canal/antena-3', 'Antena 3 '), ('/canal/tv-globo', 'TV Globo '), ('/canal/tv-5', 'TV 5 '), ('/canal/rai', 'RAI '), ('/canal/cctv', 'CCTV '), ('/canal/mtv-live-hd', 'MTV Live HD '), ('/canal/telehit-hd', 'Telehit HD '), ('/canal/vh1-hd', 'VH1 HD '), ('/canal/az-clic', 'Az Clic '), ('/canal/mtv', 'MTV '), ('/canal/ritmoson-latino', 'Ritmoson Latino '), ('/canal/bandamax', 'Bandamax '), ('/canal/telehit', 'Telehit '), ('/canal/muchmusic', 'MuchMusic '), ('/canal/vh1', 'VH1 '), ('/canal/htv', 'HTV ')]
 '''