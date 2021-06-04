def PDBUCombinaison(n,p): 
    Track=[[0]*(p+1)]*(n+1)
    print("Tableau avant:",Track)
    for i in range (p+1): 
        Track[0][i]=0 
    # Track[0][]
    for i in range (1,n+1):
        for j in range(p+1): 
            if j==0 or j== i:
                Track[i][j]=1 
            elif j==1 or j== i-1:
                Track[i][j]=i
            else:
                Track[i][j]=Track[i-1][j-1]+Track[i-1][j]
    print("Tableau apres:",Track)            
    return Track[n][p]

def PDTDRecCombinaison(n,p,T): 
    if p==0 or p==n:
        T[p][n]=1
        return 1
    elif p==1 or p==n-1 : 
       T[p][n]=n
       return n
    # elif T[p][n]>0:
        # return T[p][n]
    else:
        T[p][n]=PDTDRecCombinaison(n-1,p-1,T)+PDTDRecCombinaison(n-1,p,T)
        return T[p][n]
        
def PDTDCombinaison(n,p):
     T=[[0]*(n+1)]*(p+1)
     return PDTDRecCombinaison(n,p,T)
    
    
print("BOTTOM UP Result:",PDBUCombinaison(4,2))
print("TOP DOWN Result:",PDTDCombinaison(4,2))