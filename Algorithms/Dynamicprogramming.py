import math
def coinChanging(Coins,S,i=None,Sollutions=[]):
    if i is None:
        i=len(Coins)-1
    if S<=0:
        if S==0:
            return 0
        else:
            return math.inf
    if i==0:
        return 1 if S==Coins[0] else math.inf
    return min(coinChanging(Coins,S,i-1),coinChanging(Coins,S-Coins[i],i)+1)
Coins=[4,3,1]
S=6
print(coinChanging(Coins,6))