# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:39:40 2019

https://github.com/matinpf/light_DigiCash_python

@author: matin fallahi
"""
import secrets
import prime
import hashlib
import random
from datetime import date 

class clientwallet:
    def __init__(self, name,publiclist,k=10,Rcoin=100):
        self.name = name
        self.publiclist=publiclist
        m = hashlib.sha256()
        m.update(str.encode(name))
        #2**40=1099511627776
        self.ID=int(m.hexdigest()[:10],16)
        self.k=k
        self.Rcoin=Rcoin
        self.wallet = {
                   "coin": "RIS",
                   }
        
        
    def coingenaration(self,amount):
        randend=2**40
        coin=[amount]
        RISpair=[]
        CID=secrets.token_hex(16)
        coin.append(CID)
        coin.append(str(date.today()))
        for x in range(self.k):
            ya=secrets.randbelow(randend)
            yb=ya^self.ID
            RISpair.append([ya,yb])
            a=self.hash_info_int(ya)
            b=self.hash_info_int(yb)
            coin.append([a,b])
        return [coin,RISpair]
    
    def packetgenaration(self,amount):
        if amount in self.publiclist:
            self.strn=str(amount)+'n'
            self.spn=self.publiclist[self.strn]
            self.spublic=self.publiclist[amount]
        else:
            return False
            
        self.hcoins=[]
        self.allcoins=[]
        self.rlist=[]

        for x in range(self.Rcoin) :
            while True:
                r=secrets.randbelow(self.spn)
                xgcdr=self.xgcd(self.spn,r)
                if(r!=1 and r!=0 and xgcdr[0]==1):
                    break
            self.rlist.append(r)
            coin=self.coingenaration(amount)
            self.allcoins.append(coin)
            hashcoin=self.hash_info_int(coin[0])
            inthashcoin=int(hashcoin,16)%self.spn
            bhashcoina=self.power_mod(r,self.spublic,self.spn)
            bhashcoin=(bhashcoina*inthashcoin)%self.spn
            self.hcoins.append(bhashcoin)    
        return(self.hcoins)
        
   
    def reveal(self,idnr):
        self.coinid=idnr
        self.finalcoin=self.allcoins[idnr]
        self.finalr=self.rlist[idnr]
        self.allcoins[idnr]=0
        self.rlist[idnr]=0
        
        return (self.allcoins,self.rlist)
    
    
    def unblind(self,bcoin):
        xr=(self.xgcd(self.spn,self.finalr))[2]
        unblindedS=(xr*bcoin)%self.spn
        unblinded=self.power_mod(unblindedS,self.spublic,self.spn)
        hashcoin=self.hash_info_int(self.finalcoin[0])
        inthashcoin=int(hashcoin,16)%self.spn 
        if  unblinded==inthashcoin:
            return (True,self.finalcoin[0],unblindedS)
        else:
            return (False,0,0)
    
    
    def providek(self,kreq):
        provk=[]
        for x in range(self.k): 
            rislist=self.finalcoin[1]
            rispair=rislist[x]
            provk.append(rispair[kreq[x]])
        return(provk)
    #test wiht https://www.dcode.fr/modular-inverse
    def xgcd(self,a, b):
        b0 , b1=0 , 1
        if a<b:
            a , b= b, a
        while b != 0:
            q , a , b = a // b , b , a%b
            b0 ,b1=b1 ,b0-(q*b1)
        return(a,2,b0) 
        
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
       
    def hash_info_int(self,m1):
        m = hashlib.sha1()
        m.update(str(m1).encode('utf-8'))
        M=m.hexdigest()
        return M
        
