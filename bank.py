# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:39:40 2019

https://github.com/matinpf/lightDigiCashppython

@author: matin fallahi
"""
import secrets
import prime
import hashlib
import random

class bank:
    def __init__(self,listcoin,k=10,Rcoin=100):
        self.k=k
        self.Rcoin=Rcoin
        self.expairtime='2019-01-01'
        self.listpublic,self.listprivate=self.pairkeygenaration(listcoin)
        self.account = {
                   "matin": 1200,
                   "ali": 1500,
                   "reza": 1800,
                   }
        self.transaction = {
                   "tag": "RIS",
                   }        
        
    def merchant(self,coin,sig,name,kprov):
        if coin[0] in self.listpublic:
            self.strn=str(coin[0])+'n'
            self.spn=self.listpublic[self.strn]
            self.spublic=self.listpublic[coin[0]]
        else:
            return False
        
        unsig=self.power_mod(sig,self.spublic,self.spn)
        hashcoin=self.hash_info_int(coin)
        inthashcoin=int(hashcoin,16)%self.spn 
        if unsig==inthashcoin:
            if coin[1] in self.transaction:
                ris=self.transaction[coin[1]]
                for xy in range(self.k):
                    if ris[xy] != kprov[xy]:
                        idFraud=ris[xy]^kprov[xy]
                        namef=self.idtoname(idFraud)
                        return("clint Fraud",namef)
                return("merchant Fraud",name)
            self.transaction[coin[1]]=kprov
            self.account[name]=self.account[name]+coin[0]
            return (True, self.account)
        else:
            return (False,0)        
    

    def idtoname(self,id):
        for x in self.account :
            m = hashlib.sha256()
            m.update(str.encode(x))
            self.ID=int(m.hexdigest()[:10],16)
            if id==self.ID:
                return(x)
        
        
    def pairkeygenaration(self,listcoins):
        print(listcoins)
        listpublic = {
                   "start": 56,
                   }
        listprivate = {
                    "start": 56,
                    }
         
        for x in listcoins :
                d,e,n=self.rsakeygenarate()
                listpublic.update( {x : e} )
                listprivate.update( {x : d} )
                strn=str(x)+'n'
                listpublic.update( {strn : n} )
        return (listpublic,listprivate)
        
             




    def getblind(self,bhash,name) :
        self.name=name
        m = hashlib.sha256()
        m.update(str.encode(name))
        self.ID=int(m.hexdigest()[:10],16)
        self.rand=secrets.randbelow(self.Rcoin)
        self.sbhash=bhash
        return(self.rand)
        
        
    def verifycoins(self,allcoin,rlist,amount):
        if amount in self.listpublic:
            self.strn=str(amount)+'n'
            self.spn=self.listpublic[self.strn]
            self.spublic=self.listpublic[amount]
        else:
            return False
        bhash=self.sbhash
        vv=1
        for x in range(self.Rcoin) :
            if self.rand==x :
                continue
            re=(self.power_mod(rlist[x],self.spublic,self.spn))
            xre=(self.xgcd(self.spn,re))[2]    
            ubhash=(bhash[x]*xre)%self.spn
            getxcoinpair=allcoin[x]
            coin=getxcoinpair[0]
            RIS=getxcoinpair[1]
            hcoin=self.hash_info_int(coin)
            inthcoin=int(hcoin,16)%self.spn
            if inthcoin!=ubhash:
                vv=0
            if coin[0]!=amount:
                vv=0
                
            if coin[2]<self.expairtime:
                vv=0
                
            if self.account[self.name]<amount:
                vv=0
                
            for y in range(self.k) :
                yy=y+3
                rispair=RIS[y]
                gid=rispair[0]^rispair[1]
                hrispair0=self.hash_info_int(rispair[0])
                hrispair1=self.hash_info_int(rispair[1])
                hcoinpair=coin[yy]
                if gid != self.ID or hrispair0 != hcoinpair[0] or hrispair1 != hcoinpair[1] :
                    vv=0
                
            
            
            if vv==1:
                print(x,'verify')
            else:
                return False
        
        coinBS=(self.power_mod(bhash[self.rand],self.listprivate[amount],self.spn))
        self.account[self.name]=self.account[self.name]-amount
        return(coinBS)
        
        
    def power_mod(self,m,r,n):
        M=0
        l=[m]
        flagodd=0
        if(r%2==1):
            r=r-1
            flagodd=1
        M=m
        i=1
        while((r//2)>=i):
            i=i+i
            M=(M*M)%n
            l.append(M)
        j=len(l)-1
        while(1):
            if i==r :
                break
            if(r>=i+2**(j)):
                i=(i)+2**(j)
                M=(M*(l[j]))%n
            j=j-1    
        if(flagodd==1):
            M=(M*m)%n 
        return M    

    
    
    def rsakeygenarate(self):
        #test with https://www.dcode.fr/primality-test
        #qr , pr =gen_pq(1024)
        #!!!!!!!!! slow speed for prime 2048 - use defult prime or other algorithms
        qr , pr =self.gen_pq(1024)
        n=qr*pr
        phy=(qr-1)*(pr-1)
        while True:
            er=secrets.randbelow(65000)
            xgcdr=self.xgcd(phy,er)
            if(er!=1 and er!=0 and xgcdr[0]==1):
                break
        dr=xgcdr[2]
        if dr<0 :
            dr=dr+phy
        return (dr,er,n)
    

    def gen_pq(self,bits):
        """
        generate keypair (pr, qr)
        """
        assert bits >= 512, 'key length must be at least 512 bits'
        l = bits >> 1
        while True:
            pr = prime.randprime_bits(l)
            if prime.is_probable_prime(pr, None, l // 8):
                break
        while True:
            qr = prime.randprime_bits(bits - l)
            if pr != qr and prime.is_probable_prime(qr, None, l // 8):
                break
        return qr,pr
    
    
    def xgcd(self,a, b):
        b0 , b1=0 , 1
        if a<b:
            a , b= b, a
        while b != 0:
            q , a , b = a // b , b , a%b
            b0 ,b1=b1 ,b0-(q*b1)
        return(a,2,b0)
        
        
    def hash_info_int(self,m1):
        m = hashlib.sha1()
        m.update(str(m1).encode('utf-8'))
        M=m.hexdigest()
        return M
        
