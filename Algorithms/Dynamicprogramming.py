import time
import math
def coinChangingNaive(Coins,Somme,i=None):
    if i is None:
        i=len(Coins)-1
    if Somme<=0:
        if Somme==0:
            return 0
        else:
            return math.inf
    if i==0:
        return 1 if Somme==Coins[0] else math.inf
    return min(coinChangingNaive(Coins,Somme,i-1),coinChangingNaive(Coins,Somme-Coins[i],i)+1)

def coinChangingNaiveDynamique(Coins,Somme,cash=dict(),i=None):
    if i is None:
        i=len(Coins)-1
    if Somme in cash:
        return cash[Somme]
    if Somme<=0:
        if Somme==0:
            cash[Somme]=0
            return 0
        else:
            cash[Somme]=math.inf
            return math.inf
    if i==0:
        nb=1 if Somme==Coins[0] else math.inf
    else:
        nb= min(coinChangingNaiveDynamique(Coins,Somme,cash,i-1),coinChangingNaiveDynamique(Coins,Somme-Coins[i],cash,i)+1)
    cash[Somme]=nb
    return nb


Coins=[4,3,1]
Somme=600
now=time.time()
print(coinChangingNaive(Coins,Somme))
print("time naive=",time.time()-now)
now=time.time()
print(coinChangingNaiveDynamique(Coins,Somme))
print("time dynamique=",time.time()-now)