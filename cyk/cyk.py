import numpy as np
from numpy.lib.twodim_base import mask_indices
class GHC:
    def __init__(self,grammaire):
        self.Sigma=grammaire["Sigma"]
        self.P=grammaire["P"]
        self.V=grammaire["V"]
        self.S0=grammaire["S0"]
    def __repr__(self) -> str:
        return "Sigma: "+str(self.Sigma)+"\nV: "+str(self.V)+"\nP: "+str(self.P)
    def reduction(self):
        pass

    def generatorVariables(self):
        U0=self.Sigma
        U1=U0[:]
        while True:
            U0=U1[:]
            mask=list(map(lambda V:any(list(map(lambda word:GHC.isIn(word,U0),self.P[V]))),self.P))
            ##mask is a list of boolean values to indecate whether a V=P.key can generate a word in U0 or not
            U1=U0+list(np.array(list(self.P.keys()))[mask])
            U1=list(set(U1))
            if U1==U0:
                break
        newV=list(np.intersect1d(U1,self.V))
        return newV
    @staticmethod
    def isIn(w,Alphabet):
        #w : word or character, or list of words 
        #if w is a list of words:  each word will be considred as a sngle alphabet
        #if w is a single word : each character will be considred separently
        #return true if the word is in Alphabet false otherwise
        return all(list(map(lambda x:x in Alphabet,set(w))))
grammaire={   
"Sigma":["a","b"],
"V":["S","X","C","D"],
"P":{
    "S":["ab","aSb"],
    "X":["aXb","ab"],
    "C":["D"]
},
"S0":"S"
}
G=GHC(grammaire)
print(G.onlyGeneratorVariables())