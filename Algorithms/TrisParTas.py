parent,gauche,droite=lambda index:(index-1)//2,lambda index:eval(bin(index)+"0")+1,lambda index:eval(bin(index)+"0")+2
#TAS MAX: A[parent(index)]>=A[index],
def EntasserMax(T,i):
    #si i est feuille
    imax,g,d,n=i,gauche(i),droite(i),len(T)
    if g<n and T[g]>T[imax]:
        imax=g
    if d<n and T[d]>T[imax]:
        imax=d
    if imax!=i:
        T[i],T[imax]=T[imax],T[i]
        EntasserMax(T,imax)
def ConstruireTaxMax(T):
    B=list(range(len(T)))
    for i in range(len(T)//2,-1,-1):
        EntasserMax(T,i)
def TrisTas(T):
    B=list(range(len(T)))
    ConstruireTaxMax(T)
    for i in range(len(T)-1,0,-1):
        T[i],T[0]=T[0],T[i]
        EntasserMax(T,0)
A=[1,4,5,2,10,3,9,6,7,8]
TrisTas(A)
print(A)
