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
    def dropNonGeneratorVariables(self):
        U=[self.Sigma]
        pass

    @staticmethod
    def isIn(word,Alphabet):
        #return true if the word is in Alphabet false otherwise
        return all(list(map(lambda x:x in Alphabet,set(word))))
grammaire={   
"Sigma":["a","b"],
"V":["S","X","C","D"],
"P":{
    "S":["e","aSb"],
    "X":["aXb","e"],
    "C":["D"]
},
"S0":"S"
}
G=GHC(grammaire)
print(G)