# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 08:39:40 2019

https://github.com/matinpf/lightDigiCashppython

@author: matin fallahi

sole1: need sig valu ?
sole2: half protocol and try same k pair req
"""

from clientwallet import clientwallet
from bank import bank
from merchant import merchant
#publist =	{
#  20: 33311,
# '20n': 353943246937112285293981239515905696028726767979680517697317617057767641412188407096796391239734118852318724977559824723863657237630321788906892545060994451412235500062190426775267756082986228684020646347919043494613308197668324063148124441237778770634424676068435643359337356553172235330867319287395296793801,
#}
print("************************")
print("************************")
coinlist=[20,10]
bankm = bank(coinlist)
print(bankm.account)
print("=====================")

#RSA key genaration bank and public send to CA
publist= bankm.listpublic
print(publist)
print("=====================")
#client genarat k coin and send to back
matin = clientwallet("matin",publist)
amount=20
bhcoins=matin.packetgenaration(amount)

#bank send list of Reveal coin
notreaveal=bankm.getblind(bhcoins,matin.name)
print(notreaveal)
print("=====================")
#client send list of r and reveal coins to bank for verify
#if verify true bank return blindsigcoin else false
allcoin,rlist=matin.reveal(notreaveal)
blindsigcoin=bankm.verifycoins(allcoin,rlist,amount)
#print(blindsigcoin)
print(bankm.account)
print("=====================")
#client unblind and check coin
result,coin,sig=matin.unblind(blindsigcoin)
print(result,"matin ublind")
print("=====================")

#:) :-) :-)

#client send coin to merchant 
mer = merchant(publist,'ali')
#res,kreq=mer.sell(coin,sig+1)
res,kreq=mer.sell(coin,sig)
print(res,kreq,"merchant result")
print("=====================")

#clint provide kreq for merchant
kprov=matin.providek(kreq)
print(kprov)
print("=====================")

#merchant verify provide k if ok sell Succeeded
#kprov=[0, 0, 1, 0, 1, 1, 0, 1, 0, 0]
res=mer.verify(kprov)
print(res,"sell")
print("=====================")

#merchant other time send coin to bank and add money to account
res=bankm.merchant(coin,sig,mer.namem,kprov)
print(res)
print("=====================")

res=bankm.merchant(coin,sig,mer.namem,kprov)
print(res)
print("=====================")


mer2 = merchant(publist,'reza')
#res,kreq=mer.sell(coin,sig+1)
res,kreq=mer2.sell(coin,sig)
print(res,kreq)
print("=====================")

#clint provide kreq for merchant
kprov=matin.providek(kreq)
print(kprov)
print("=====================")

#merchant verify provide k if ok sell Succeeded
#kprov=[0, 0, 1, 0, 1, 1, 0, 1, 0, 0]
res=mer2.verify(kprov)
print(res,"sell")
print("=====================")

#merchant other time send coin to bank and add money to account
res=bankm.merchant(coin,sig,mer2.namem,kprov)
print(res)
print("=====================")
