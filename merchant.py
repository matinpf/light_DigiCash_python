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

class merchant:
    def __init__(self,publiclist,namem,k=10):
        self.namem=namem
        self.publiclist=publiclist
        self.k=k
        

    def sell(self,coin,sig):
        self.kreq=[]
        if coin[0] in self.publiclist:
            self.strn=str(coin[0])+'n'
            self.spn=self.publiclist[self.strn]
            self.spublic=self.publiclist[coin[0]]
        else:
            return False
        
        self.coin=coin
        unsig=self.power_mod(sig,self.spublic,self.spn)
        hashcoin=self.hash_info_int(self.coin)
        inthashcoin=int(hashcoin,16)%self.spn 
        if unsig==inthashcoin:
            for x in range(self.k):
                self.kreq.append(secrets.randbelow(2))
            return (True, self.kreq)
        else:
            return (False,0)
        
    def verify(self,kprov):
        for x in range(self.k):
            hk=self.hash_info_int(kprov[x])
            hkcoin=self.coin[x+3]
            if hk != hkcoin[self.kreq[x]]:
                return False
        return True


        
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
        
