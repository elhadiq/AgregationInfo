import numpy as np
import pandas as pd
class GHC:
    __name__="GHC"

    def __init__(self,grammaire):
        self.Sigma=set(grammaire["Sigma"])
        self.P=grammaire["P"]
        self.V=set(grammaire["V"])
        self.S0=grammaire["S0"]

    def copy(self,ghc):
        self.Sigma=ghc.Sigma
        self.V=ghc.V
        self.P=ghc.P
        self.S0=ghc.S0

    def __repr__(self) -> str:
        return str(self.__name__)+"\nSigma: "+str(self.Sigma)+"\nV: "+str(self.V)+"\nP: "+str(self.P)

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
        W0=set()
        W1={self.S0}
        while W1!=W0:
            W0=W1
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
                newAccesibles=set(rulesfromW0)
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

    @staticmethod
    def substitute(word,toSub,done=""):
        if (not len(word)):
            return {done}
        if (word[0] not in toSub):
            return GHC.substitute(word[1:],toSub,done+word[0])
        return GHC.substitute(word[1:],toSub,done+word[0]).union(GHC.substitute(word[1:],toSub,done))


    def dependeceDictionary(self):
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
        """ removing primitives variables"""
        for Var in list(allDependances):
            if allDependances[Var]==set():
                allDependances.pop(Var)
        return allDependances


    @staticmethod
    def alldependants(Var,directDependants,dependants=set()):
        """ compute all dependants (ie Variables primitives) of a givven Var"""
        dependants.add(Var)
        newDependants=GHC.unionReducer([directDependants[D] for D in dependants]).difference(dependants)
        if(len(newDependants)!=0):
            dependants=dependants.union(newDependants)
            dependants=dependants.union(GHC.unionReducer([GHC.alldependants(V,directDependants,dependants) for V in newDependants]))
        return dependants.difference(Var)


    def productionOf(self,Var,done=set()):
        """Compute the non Variable production of each Variable """
        if Var not in self.P:
            return set()
        done.add(Var)
        return self.P[Var].difference(self.V).union(GHC.unionReducer([self.productionOf(D,done) for D in self.P[Var].intersection(self.V).difference(done)]))
    
    
    def substitutionByEpsilon(self,Uepsilon):
        """Return a dictionary {Var: new set substitued} for each Var in V"""
        return {Var:GHC.unionReducer( [GHC.substitute(word,Uepsilon) for word in self.P[Var]]) for Var in self.P}
    
    def selectMAx(dictionary):
        """ key who has the max of values and remove it"""
        assert len(dictionary),"dictionary empty"
        elems=list(dictionary)
        nbElem=list(map(lambda v:len(dictionary[v]),elems))
        imax=nbElem.index(max(nbElem))
        Max=elems[imax]
        dependants=dictionary.pop(Max)
        return Max,dependants

class GHCReduced(GHC):
    __name__="GHC Reduite"
    def __init__(self, ghc):
        super().__init__(GHCReduced.reductionGrammar(ghc))
    @staticmethod
    def reductionGrammar(ghc):
        Rgrammaire=dict()
        Rgrammaire["Sigma"]=ghc.Sigma
        Rgrammaire["S0"]=ghc.S0
        Rgrammaire["V"]=ghc.accessiblesVariables().intersection(ghc.generatorVariables())
        Rgrammaire["P"]=dict()
        acceptedAlphabet=ghc.Sigma.union(Rgrammaire["V"])
        """Elimination of word that containe an unccessible or an non generator variable """
        for Var in set(ghc.P).intersection(Rgrammaire["V"]):
            destinations={word if GHC.isIn(word,acceptedAlphabet) else 1 for word in ghc.P[Var]}
            try :
                destinations.remove(1)
            except KeyError:
                pass
            if (len(destinations)):
                Rgrammaire["P"][Var]=destinations
        return Rgrammaire
    

class GHCPropre(GHC):
    __name__="GHC Propre"
    def __init__(self, ghc):
        self.copy(ghc)
        self.cleaner()
    def cleaner(self):
        self.removeEpsilons()
        self.removeDirectDependency()

    def removeEpsilons(self):
        Uepsilon=self.epsilonGeneratorVariables()
        self.P=self.substitutionByEpsilon(Uepsilon)
        for V in Uepsilon:
                self.P[V]=self.P[V].difference({"e",""})

    def removeDirectDependency(self):
        dependancyDictionary=self.dependeceDictionary()
        while len(dependancyDictionary)!=0:
            V,dependants=GHC.selectMAx(dependancyDictionary)
            productions=self.productionOf(V)
            for D in dependants:
                self.P[D]=self.P[D].union(productions).difference({V})

class GHCChomsky(GHCReduced,GHCPropre):
    __name__="GHC Forme normale chomsky"
    def __init__(self,ghc):
        propre=GHCPropre(ghc)
        reduite=GHCReduced(propre)
        self.copy(reduite)

    def cyk(self,word):
        assert GHC.isIn(word,self.Sigma),"word %s not in alphabet %s"%(word,str(self.Sigma))
        n=len(word)
        T=pd.DataFrame([[set()]*n]*n)
        for i,wi in enumerate(word):
            Tii=set()
            for A in self.V:
                if wi in self.P[A]:
                    Tii.add(A)
            T[i][i]=T[i][i].union(Tii)
        
        for j in range(n):
            for i in reversed(range(j)):
                for k in range(i,j):
                    for A in self.P:
                        for B in T[i][k]:
                            for C in T[k+1][j]:
                                if B+C in self.P[A]:
                                    T[i][j].add(A)
        T[0][n-1]=str(T[0][n-1])+"*"
        print("Analysis Table of the word: ",word,"\n",T.transpose())
    
grammaire={
"Sigma":"abcd",
"V":"ABCS",
"P":{
    "S":{"a","B"},
    "B":{"b","bC","C"},
    "C":{"cd","c",'d'}
},
"S0":"S"
}
G=GHC(grammaire)
chomsky=GHCChomsky(G)
print(chomsky)
chomsky.cyk("abcd")