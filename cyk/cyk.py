from functools import singledispatch
import numpy as np
from numpy.core.fromnumeric import var
class GHC:
    def __init__(self,grammaire):
        self.Sigma=grammaire["Sigma"]
        self.P=grammaire["P"]
        self.V=grammaire["V"]
        self.S0=grammaire["S0"]
    def __repr__(self) -> str:
        return "Sigma: "+str(self.Sigma)+"\nV: "+str(self.V)+"\nP: "+str(self.P)

    def generatorVariables(self):
        U0=self.Sigma
        U1=set()
        while U0!=U1:
            U0=U1 if U1!=set() else U0
            Vars=np.array(list(self.P.keys()))
            filter=list(map(lambda V:any(list(map(lambda word:GHC.isIn(word,U0),self.P[V]))),Vars))
            ##mask is a list of boolean values to indecate whether a V=P.key can generate a word in U0 or not
            U1=U0.union(set(Vars[filter]))
        newV=U1.intersection(self.V)
        return newV
    @staticmethod
    def isIn(w,Alphabet):
        #w : word or character, or list of words 
        #if w is a list of words:  each word will be considred as a sngle alphabet
        #if w is a single word : each character will be considred separently
        #return true if the word is in Alphabet false otherwise
        return all(list(map(lambda x:x in Alphabet,set(w))))
    @staticmethod
    def unionReducer(listOfSets):
        u0=set()
        for u in listOfSets:
            u0=u0.union(u)
        return u0
    def accessiblesVariables(self):
        W0={self.S0}
        W1=set()
        while W1!=W0:
            W0=W1 if W1!=set() else W0
            rulesfromW0="".join(GHC.unionReducer([self.P[Var] for Var in W0.intersection(list(self.P.keys()))]))
            #now we have to path in order to menimase: if the alphabet Sigma is so small than the set V we can remove 
            # the alphabet character by charater until having only reachable variables of V
            # OR if the V is small we can test for each var in V if is it reacheable or not
            newAccesibles=set()
            if len(self.V)<len(self.Sigma):
                    newAccesibles={Var if Var in rulesfromW0 else "Nan" for Var in self.V}
                    newAccesibles.remove("Nan")
            else:
                for a in self.Sigma:
                    rulesfromW0=rulesfromW0.replace(a,'')
                newAccesibles=set(list(rulesfromW0))
            W1=W1.union(newAccesibles)
        return W1
    def epsilonGeneratorVariables(self):
        U0={Var if "e" in self.P[Var] else 1 for Var in self.P}
        try:
            U0.remove(1)
        except KeyError:
            pass
        U1=set()
        while U0!=U1:
            U0=U1 if U1!=set() else U0
            U1=U0.union({Var if any(set(map(lambda word:GHC.isIn(word,U0),self.P[Var]))) else 1 for Var in self.P})
            try:
                U1.remove(1)
            except KeyError:
                pass
        return U1
    def substitutionByEpsilon(self,Uepsilon):
        return {Var:GHC.unionReducer( [GHC.substitute(word,Uepsilon) for word in self.P[Var]]) for Var in self.P}
    def cleaner(self):
        subTable= self.substitutionByEpsilon(self.epsilonGeneratorVariables())
        newPtable={V:(self.P[V].union(subTable[V])).difference({"e",""}) for V in self.P}
        return newPtable
    def reduction(self):
        grammaire=dict()
        grammaire["Sigma"]=self.Sigma
        grammaire["S0"]=self.S0
        grammaire["V"]=self.accessiblesVariables().intersection(self.generatorVariables())
        grammaire["P"]=dict()
        acceptedAlphabet=self.Sigma.union(grammaire["V"])
        for Var in self.P:
            destinations={word if GHC.isIn(word,acceptedAlphabet) else 1 for word in self.P[Var]}
            try :
                destinations.remove(1)
            except KeyError:
                pass
            if (len(destinations)):
                grammaire["P"][Var]=destinations
        return GHCReduced(grammaire)
    
    @staticmethod
    def substitute(word,toSub,done=""):
        if (not len(word)):
            return {done}
        if (word[0] not in toSub):
            return GHC.substitute(word[1:],toSub,done+word[0])
        return GHC.substitute(word[1:],toSub,done+word[0]).union(GHC.substitute(word[1:],toSub,done))
    def dependeces(self):
        """
        La raision de travailler sur les dependeants c'est pour savoir la variable qui a 
        le plus grand nombre de depandans en eliminant ces dependances ainsi en montant vers la
        variable qui a un nombre moins eleve jusq'a arrivé à la variable qui un nombre de depandants le moins eleve .. et qui est probabelement 
        depende (se derive derictement) en variables deja traité (ie ne se derive pas)
        """
        directDpendants={Var:set() for Var in self.V}
        allDependances=directDpendants.copy()
        for Var in self.P:
            for alpha in self.P[Var]:
                if alpha in self.V:
                    directDpendants[alpha].add(Var)
        for Var in self.P:
            allDependances[Var]=GHC.alldependants(Var,directDpendants)
        return allDependances

    @staticmethod
    def alldependants(Var,directDependants,dependants=set()):
        dependants.add(Var)
        newDependants=GHC.unionReducer([directDependants[D] for D in dependants]).difference(dependants)
        if(len(newDependants)!=0):
            dependants=dependants.union(newDependants)
            dependants=dependants.union(GHC.unionReducer([GHC.alldependants(V,directDependants,dependants) for V in newDependants]))
        return dependants.difference(Var)
    def productionOf(self,Var,done=set()):
        done.add(Var)
        return self.P[Var].difference(self.V).union(GHC.unionReducer([self.productionOf(D,done) for D in self.P[Var].intersection(self.V).difference(done)]))
class GHCReduced(GHC):
    def __init__(self, grammaire):
        super().__init__(grammaire)
class GHCProper(GHC):
    def __init__(self, grammaire):
        super().__init__(grammaire)
class GHCChomsky(GHCReduced,GHCProper):
    def __init__(self, grammaire):
        super().__init__(grammaire)
    
grammaire={
"Sigma":{"a","b"},
"V":{"A","B","C","D"},
"P":{
    "A":{"B","ab"},
    "B":{"C","a"},
    "C":{"D","aabD"},
    "D":{"C"}
},
"S0":"A"
}
G=GHC(grammaire)
#print("generators: ",G.generatorVariables())
#print("Accecibles: ",G.accessiblesVariables())
#print("new",G.reduction())
#print("epsilon generator",G.epsilonGeneratorVariables())
#print("term",G.cleaner())
#print(G.cleaner())
#print(G.dependeces())
#print(GHC.alldependants("D",G.dependeces()))
print(G.productionOf("A"))