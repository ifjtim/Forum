#!/usr/bin/env python
# -*- coding: utf-8 -*-
#autor xkonde 03
import urllib
from bs4 import BeautifulSoup
import re
import sys
import os
import string
children=[] #pole ktrere uchovava všechny potomky

# stahuje přimo konkretni diskuzi je to už potomek hlavniho procesu
# b-odkaz,zanořeni ve webu na konkretni diskuzi
# jmenosouboru - jmeno složky ve ktere se ma vytviřit soubor 
def konkretnivlakno(b,jmenosouboru):
    con="http://forum.autoforum.cz"+b 
    
    #stahnuti stranky
    fc = urllib.urlopen(con)
    data = fc.read()
    fc.close()
    data=unicode(data,'utf-8')
    
    # rozděleni stanky pomoci knihovny BeautifulSoup
    soup=BeautifulSoup(data)
    notices = soup.find_all("div", {"class": "content"})  #text přispevku
    author = soup.find_all("p", {"class": "author"})      #jmneo autora je v tomle bloku
    strany= soup.find_all("div", {"class": "pagination"}) # aktulni stranka
    odkazy= soup.find_all("a", {"class": "right-box right"}) #odkaz na nasledujici stranu konkretni tematu pokud ekyistuje
    prispevky= soup.find_all("div", {"class": "pagination"}) #počet přispevku konkretni čislo
    
    con = ""
    jmeno= ""
    pocet=""
    poletext=[]
    poleutor=[]
    f = open(jmenosouboru,"w")

    #nalezeni a pomocin regularnich vzrazu vzjmuto počet přispevku
    for pocitam in prispevky:
        pocet=str(pocitam)
        navr=re.findall("Příspěv[e]*k[ů]*: \d*",pocet)
        pocet=navr[0]
        sit=re.findall("\d*$",pocet)
        pocet=sit[0]
    f.write(pocet)
    f.write("\n")
       
    #nalezeni textu konkretniho přispevku
    for link in notices:
        con=str(link)
        con=re.sub("<br/>","\n",con)
        con=re.sub("<[^>]*>{1}","",con)
        poletext.append(con)
    #nalezeni konkretniho jmena
    for link in author:
        con=str(link)
        con=re.sub("<[^>]*>{1}","",con)
        poleutor.append(con) #autor se přida do pole autoru
    i=0;  
    
    #uloženi do souboru
    for radek in poletext:
        f.write(poleutor[i]) #autor
        f.write("\n")
        f.write(radek) #text prispevku
        f.write("\n")
        f.write("***********************************************************************************************************************")
        f.write("\n")
        i=i+1
    
    jmeno= ""
    jmeno=str(strany) #aktualni strana

    #print odkazy 
    for link in odkazy:
        con=str(link.get('href'))
    c=0
    #kontrola pokud určite tema ma vic stranek stahu je postupne všechny
    while odkazy!=[]: #stahuje do té doby dokud je ješče nejaka stranka na kterou lze prejit
        c=c+1
        #print c
        con="http://forum.autoforum.cz"+con
        stahnout(f,con);
        fc = urllib.urlopen(con) # staženi nove strany
        data = fc.read()
        fc.close()
        data=unicode(data,'utf-8')
        soup=BeautifulSoup(data)
        odkazy= soup.find_all("a", {"class": "right-box right"}) #staženi odkazu na dalši stranu
        
        for link in odkazy:
            con=str(link.get('href'))

            
    f.close()
    os._exit(0) 
#ruzne temata jsou rodelena na tematicke celky stahnout dalsi
#stahnoudalsi stahuje dalsi tema z dalšich strana
#adres odkaz na stranku z nazvy témat
#jmenosslozky jmeno slozky do ktere se maji ukladat témata
def stahnoudalsi(adres,jmenosslozky):    
        
    fg = urllib.urlopen(adres)
    data = fg.read()
    fg.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "topictitle"}) #jmena témat
    odkazy= soup.find_all("a", {"class": "right-box right"})
    
    con = ""
    jmeno=""
    b=[]
    jmenosouboru=[]
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        print jmeno
        #tyhle ty znaky se nesmi objevit v nazvu souboru
        jmeno=re.sub("\"","N",jmeno)
        #jmeno=re.sub("\\","N",jmeno)
        jmeno=re.sub("/","N",jmeno)
        jmeno=re.sub("\.","N",jmeno)
        jmeno=re.sub("\?","N",jmeno)
        jmeno=re.sub(":","N",jmeno)
        jmeno=re.sub("\*","N",jmeno)
        jmeno=re.sub("<","N",jmeno)
        jmeno=re.sub(">","N",jmeno)
        jmeno=re.sub("\|","N",jmeno)
        jmeno=jmenosslozky+"/"+jmeno
        #uklada všechny témata
        jmenosouboru.append(jmeno)
        #uklada odkazy na temata
        b.append(con)
        
    o=0 
    #stahovani každeho tématu je zvlašč ve vlakne
    for neco in b:
        newpid = os.fork()
        if newpid == 0:
            print jmenosouboru[o]
            konkretnivlakno(neco,jmenosouboru[o])
        
        else:
            o=o+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
            print "parent: %d, child: %d" % pids 
    
    
#temata y prvni strany
#a odkaz
#jmenosslozky jmeno složky
def spracujpar(a,jmenosslozky):
    con="http://forum.autoforum.cz"+a
    fg = urllib.urlopen(con)
    data = fg.read()
    fg.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "topictitle"})
    odkazy= soup.find_all("a", {"class": "right-box right"})
    strany= soup.find_all("div", {"class": "pagination"})
    con = ""
    jmeno=""
    b=[]
    jmenosouboru=[]
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        #print jmeno
        jmeno=re.sub("\"","N",jmeno)
        #jmeno=re.sub("\\","N",jmeno)
        jmeno=re.sub("/","N",jmeno)
        jmeno=re.sub("\.","N",jmeno)
        jmeno=re.sub("\?","N",jmeno)
        jmeno=re.sub(":","N",jmeno)
        jmeno=re.sub("\*","N",jmeno)
        jmeno=re.sub("<","N",jmeno)
        jmeno=re.sub(">","N",jmeno)
        jmeno=re.sub("\|","N",jmeno)
        jmeno=jmenosslozky+"/"+jmeno
        jmenosouboru.append(jmeno)
        b.append(con)

            
    jmeno= ""
    jmeno=str(strany)

    #print odkazy
    for link in odkazy:
        con=str(link.get('href'))
        #print con
    c=0      
    while odkazy!=[]:
        c=c+1
        con="http://forum.autoforum.cz"+con
        stahnoudalsi(con,jmenosslozky);
        fc = urllib.urlopen(con)
        data = fc.read()
        fc.close()
        data=unicode(data,'utf-8')
        soup=BeautifulSoup(data)
        odkazy= soup.find_all("a", {"class": "right-box right"})
        
        for link in odkazy:
            con=str(link.get('href'))
             
    o=0   
    for neco in b:
        newpid = os.fork()
        if newpid == 0:
            print jmenosouboru[o]
            konkretnivlakno(neco,jmenosouboru[o])

        else:
            o=o+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
            print "parent: %d, child: %d" % pids
    
#tato fukce stahuje dalši strany jednoho tematu a všechny přispevky v něm
#f soubor do ktere se zapisje
#adresa nove strany

def stahnout(f,adresa):
    fs = urllib.urlopen(adresa)
    data = fs.read()
    fs.close()
    data=unicode(data,'utf-8')
    
    soup=BeautifulSoup(data)
    notices = soup.find_all("div", {"class": "content"})
    author = soup.find_all("p", {"class": "author"})
    strany= soup.find_all("div", {"class": "pagination"})

    con = ""
    jmeno= ""
    poletext=[]
    poleutor=[]
   
    for link in notices:
        con=str(link)
        con=re.sub("<br/>","\n",con)
        con=re.sub("<[^>]*>{1}","",con)
        poletext.append(con)
        
    for link in author:
        con=str(link)
        con=re.sub("<[^>]*>{1}","",con)
        poleutor.append(con)
    i=0;
    for radek in poletext:
        f.write(poleutor[i])
        f.write("\n")
        f.write(radek)
        f.write("\n")
        f.write("*****************************************************************************************************************************")
        f.write("\n")
        i=i+1
  
  
#***********************aktulizace****************************************************************************************
# aktualizačni mod kontroluje počet přispevku na strance z počtem ztahnutych přispevku
# stahnoudalsiaktual kontrolu dalsi strany tematických celku
# adres je adresa nové strany tematickeho celku
# jmenosslozky je jmeno adresaře do ktereho má byt uložen
def stahnoudalsiaktual(adres,jmenosslozky):       
    fg = urllib.urlopen(adres)
    data = fg.read()
    fg.close()
    data=unicode(data,'utf-8')
    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "topictitle"})
    odkazy= soup.find_all("a", {"class": "right-box right"})
    
    o=0 
    con = ""
    jmeno=""
    b=[]
    jmenosouboru=[]
    nenove=[]
    adresa=[]
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        jmeno=re.sub("\"","N",jmeno)
        #jmeno=re.sub("\\","N",jmeno)
        jmeno=re.sub("/","N",jmeno)
        jmeno=re.sub("\.","N",jmeno)
        jmeno=re.sub("\?","N",jmeno)
        jmeno=re.sub(":","N",jmeno)
        jmeno=re.sub("\*","N",jmeno)
        jmeno=re.sub("<","N",jmeno)
        jmeno=re.sub(">","N",jmeno)
        jmeno=re.sub("\|","N",jmeno)
        jmeno=jmenosslozky+"/"+jmeno

        if os.path.isfile(jmeno):
            #print "neaktual"
            nenove.append(jmeno)
            adresa.append(con)
        else:
            #print "aktual"
            jmenosouboru.append(jmeno)
            b.append(con)
        
    #pokud to téma nekzistuje stahne se cele 
    for neco in b:
        newpid = os.fork()
        if newpid == 0:
            konkretnivlakno(neco,jmenosouboru[o])
        else:
            o=o+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
    pocet=0
    #pokud tema ekzistuje zkontroluje se počet přispevku
    for polozka in adresa:
        newpid = os.fork()
        #pro každou kontrolu se vytvoři nové vlakno
        if newpid == 0:
            #print nenove[pocet]
            kotrolakomentu(polozka,nenove[pocet])
        else:
            pocet=pocet+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
            #print "parent: %d, child: %d" % pids
           
       
#porovna počet ztahnutych přispevku z počtem přispevku na foru          
def kotrolakomentu(adresa,jmeno):
    con="http://forum.autoforum.cz"+adresa

    fc = urllib.urlopen(con)
    data = fc.read()
    fc.close()
    data=unicode(data,'utf-8')
    soup=BeautifulSoup(data)
    prispevky= soup.find_all("div", {"class": "pagination"})
    #print jmeno
    pocet=str(prispevky[0])
    navr=re.findall("Příspěv[e]*k[ů]*: \d*",pocet)
    pocet=navr[0]
    sit=re.findall("\d*$",pocet)
    pocet=sit[0]
    #print pocet
    f = open(jmeno,"r")
    radky=""
    line =f.read(1)
    
    while (line!='\n') :
        radky=radky+line
        line =f.read(1)
    f.close()
    if radky!=pocet:
        try:
            inpocet=int(pocet)
            inradky=int(radky)
        except ValueError:
            print "chyba cislo"
        else:
            vypocet=inpocet-inradky
            if(vypocet>0):
                s = open(jmeno,"r+")
                s.seek(0)  
                s.write(pocet)
                s.write('\n')
                s.close()
                print "pocet"
                print vypocet
                print jmeno
                stahujiaktual(jmeno,vypocet,con)
        
    sys.exit(0)
    


def stahujiaktual(jmeno,vypocet,adresa):

    con=adresa
    fc = urllib.urlopen(con)
    data = fc.read()
    fc.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("div", {"class": "content"})
    author = soup.find_all("p", {"class": "author"})
    strany= soup.find_all("div", {"class": "pagination"})
    odkazy= soup.find_all("a", {"class": "right-box right"})
    prispevky= soup.find_all("div", {"class": "pagination"})

    pocet=""
    #print prispevky
    olast=""
    pocet=str(prispevky[0])
    navr=re.findall("a href=\"[^>]*>{1}",pocet)
    for match in navr:
        olast=match
    #print olast
    if olast :
        olast=re.sub("amp;","",olast)
        #print olast
        olast=re.sub("a href=\"","",olast)
        olast=re.sub("\">","",olast)

        olast="http://forum.autoforum.cz"+olast
        print olast
    
    pocet=""

    fc = urllib.urlopen(olast)
    data = fc.read()
    fc.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("div", {"class": "content"})
    author = soup.find_all("p", {"class": "author"})
    strany= soup.find_all("div", {"class": "pagination"})
    odkazy= soup.find_all("a", {"class": "left-box left"})

    poletext=[]
    poleutor=[]
    c=0
    for link in notices:
        con=str(link)
        con=re.sub("<br/>","\n",con)
        con=re.sub("<[^>]*>{1}","",con)
        poletext.append(con)
            
    for link in author:
        c=c+1
        con=str(link)
        con=re.sub("<[^>]*>{1}","",con)
        poleutor.append(con)  

    link= odkazy[0]
    con=str(link.get('href'))
    print con        
    while odkazy!=[]:
        
        if (c>=vypocet):
            break;
        con="http://forum.autoforum.cz"+con
        
        fc = urllib.urlopen(con)
        data = fc.read()
        fc.close()
        data=unicode(data,'utf-8')

        soup=BeautifulSoup(data)
        notices = soup.find_all("div", {"class": "content"})
        author = soup.find_all("p", {"class": "author"})
        strany= soup.find_all("div", {"class": "pagination"})
        odkazy= soup.find_all("a", {"class": "left-box left"})
        cislo1=len(poletext) 
        for link in notices:
            co=str(link)
            co=re.sub("<br/>","\n",co)
            co=re.sub("<[^>]*>{1}","",co)
            poletext.insert(cislo1,co)
        cislo=len(poleutor)  
        for lin in author:
            c=c+1
            co=str(lin)
            co=re.sub("<[^>]*>{1}","",co)
            poleutor.insert(cislo,co)
        
        
        link= odkazy[0]
        con=str(link.get('href')) 
        print con
    
    f = open(jmeno,"a")
    for hi in range(vypocet):
        f.write(poleutor[hi])
        f.write("\n")
        f.write(poletext[hi])
        f.write("\n")
        f.write("*****************************************************************************************************************************")
        f.write("\n")
        

    
def aktualizacekonkretni(a,jmenosslozky):
    con="http://forum.autoforum.cz"+a
    fg = urllib.urlopen(con)
    data = fg.read()
    fg.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "topictitle"})
    odkazy= soup.find_all("a", {"class": "right-box right"})
    strany= soup.find_all("div", {"class": "pagination"})
    con = ""
    jmeno=""
    b=[]
    jmenosouboru=[]
    nenove=[]
    adresa=[]
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        #print jmeno
        jmeno=re.sub("\"","N",jmeno)
        #jmeno=re.sub("\\","N",jmeno)
        jmeno=re.sub("/","N",jmeno)
        jmeno=re.sub("\.","N",jmeno)
        jmeno=re.sub("\?","N",jmeno)
        jmeno=re.sub(":","N",jmeno)
        jmeno=re.sub("\*","N",jmeno)
        jmeno=re.sub("<","N",jmeno)
        jmeno=re.sub(">","N",jmeno)
        jmeno=re.sub("\|","N",jmeno)
        jmeno=jmenosslozky+"/"+jmeno
        
        #print jmeno 
       
        if os.path.isfile(jmeno):
            #print "neaktual"
            nenove.append(jmeno)
            adresa.append(con)
        else:
            #print "aktual"
            jmenosouboru.append(jmeno)
            b.append(con)
             
    jmeno= ""
    i=0
    jmeno=str(strany)

    for link in odkazy:
        con=str(link.get('href'))
        #print con
    c=0      
    while odkazy!=[]:
        c=c+1
        #print c
        con="http://forum.autoforum.cz"+con
        stahnoudalsiaktual(con,jmenosslozky);
        fc = urllib.urlopen(con)
        data = fc.read()
        fc.close()
        data=unicode(data,'utf-8')
        soup=BeautifulSoup(data)
        odkazy= soup.find_all("a", {"class": "right-box right"})
        
        for link in odkazy:
            con=str(link.get('href'))
           
    o=0   
    for neco in b:   
        newpid = os.fork()
        if newpid == 0:
            print jmenosouboru[o]
            konkretnivlakno(neco,jmenosouboru[o])
        else:
            o=o+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
            print "parent: %d, child: %d" % pids
    pocet=0 
    for polozka in adresa:
        newpid = os.fork()  
        if newpid == 0:
            #print nenove[pocet]
            kotrolakomentu(polozka,nenove[pocet])
           # print "nnnnnn"  
        else:
            pocet=pocet+1
            pids = (os.getpid(), newpid)
            children.append(newpid)
            print "parent: %d, child: %d" % pids
                
def aktualizace():
   
    fp = urllib.urlopen('http://forum.autoforum.cz/')
    #print "tady jj"
    data = fp.read()
    fp.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "forumtitle"})
    con = ""
    jmeno= ""
    i=0
    a=[]
    jmenosslozky=[]
    
    #print "tady jj"
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        jmeno="./forum/"+jmeno
        jmenosslozky.append(jmeno)
        a.append(con)
    
    c=0
    #print "tady jj"
    for neco in a:
        if os.path.isdir(jmenosslozky[c]):
           
            aktualizacekonkretni(neco,jmenosslozky[c]);
        else:
            os.mkdir(jmenosslozky[c],0777)
            spracujpar(neco,jmenosslozky[c]);
        c=c+1
#komplet se vola pokud ma bzt dtahnute cele forum
def komplet():
    os.mkdir("forum",0777) #vytvoři adresař pod jmenem forum
    fp = urllib.urlopen('http://forum.autoforum.cz/')
    data = fp.read()
    #print data
    fp.close()
    data=unicode(data,'utf-8')

    soup=BeautifulSoup(data)
    notices = soup.find_all("a", {"class": "forumtitle"})
    con = ""
    jmeno= ""
    i=0
    a=[]
    jmenosslozky=[]
    
    #najde jmena adresařu a odkazy na ně
    for link in notices:
        con=str(link.get('href'))
        jmeno= (link.string)
        jmeno="./forum/"+jmeno
        jmenosslozky.append(jmeno)
        a.append(con)
    
    c=0
    for neco in a:
        os.mkdir(jmenosslozky[c],0777)
        spracujpar(neco,jmenosslozky[c]);
        c=c+1
    

def main():
   
    if os.path.isdir('./forum'):
        aktualizace();
    else:
        komplet();
    for child in children:
        os.waitpid(child, 0)
    print "dokonceno"
    
            
if __name__ == '__main__':
    main()  


    
   
    

      

