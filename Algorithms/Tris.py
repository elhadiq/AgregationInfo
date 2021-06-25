def TriInsertion(T):
    for i in range(2,len(T)):
        for j in range(i):
                if(T[i]<T[j]):
                    #Insertion Une seule fois
                    T[:i+1]=T[:j]+[T[i]]+T[j:i]
                    break
def TriBulle(T):
    for i in range(len(T)-1):
        for j in range(len(T)-1,i-1,-1):
            if T[j-1]>T[j]:
                T[j-1],T[j]=T[j],T[j-1]
A=[3,5,19,10,13]
#TriInsertion(A)
TriBulle(A)
print(A)