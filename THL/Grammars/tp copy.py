from itertools import groupby
Sigma=['(',')','+','*','a']
V=['E','Ep','T','Tp','F']
P={
'E':[['T','Ep']],
'Ep':[['e'],['+','T','Ep']],
'T':[['F','Tp']],
'Tp':[['*','F','Tp'],['e']],
'F':[['(','E',')'],['a']]}
G=[Sigma,V,'E',P]

def suffixeAlpha(alpha):
    if alpha ==[]:
        return []
    return [alpha]+suffixeAlpha(alpha[1:])
a=['*','F','Tp']
#print(suffixeAlpha(a))
# Question 2
listOflist=lambda lst:list(map(lambda el:[el], lst))
dropDuplicates=lambda a:[k for k,v in groupby(sorted(a))]

def colonesPremier(P,Sigma,V):
    retrn=listOflist(Sigma)+[['e']]+listOflist(V)
    for A in list(P.values()):
        for a in A:
            retrn=retrn+suffixeAlpha(a)
    return dropDuplicates(retrn)
print(colonesPremier(P,Sigma,V))

def premier0(alpha,Sigma,P):
    if alpha=='e':
        return ['e']
    if alpha in Sigma:
        return [alpha]
    try:
        destinations=P[alpha]
        if ['e'] in destinations:
            return ['e']
    except:
         

def calcul_ensemble_premier(G):
    cp=colonesPremier(G[3],G[0],G[1])
    #print(cp)      
#calcul_ensemble_premier(G)