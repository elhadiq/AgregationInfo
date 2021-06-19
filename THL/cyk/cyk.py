__author__      = "Zouhair El Hadiq"
import numpy as np
import pandas as pd
class GHC:
    __name__="GHC"

    def __init__(self,grammaire):
        self.Sigma=set(grammaire["Sigma"])
        self.P=self.getProduction(grammaire["P"])
        self.V=set(grammaire["V"])
        self.S0=grammaire["S0"]
    def getProduction(self,Pdictionary):
        P=dict()
        for V in Pdictionary:
            P[V]=set(Pdictionary[V].split("+"))
        return P
    def copy(self,ghc):
        self.Sigma=ghc.Sigma.copy()
        self.V=ghc.V.copy()
        self.P=ghc.P.copy()
        self.S0=ghc.S0

    def __repr__(self) -> str:
        return str(self.__name__)+"\nSigma: {"+",".join(self.Sigma)+"}"+\
            "\nV: {"+",".join(self.V)+"}"+\
                "\nProduction: \n"+ "\n".join([V+"---> "+"|".join(self.P[V]) for V in  self.P])

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
                    try :
                        newAccesibles.remove("Nan")
                    except KeyError:
                        pass
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
    def substituteByEpsilon(word,toSub,done=""):
        if (not len(word)):
            return {done}
        if (word[0] not in toSub):
            return GHC.substituteByEpsilon(word[1:],toSub,done+word[0])
        return GHC.substituteByEpsilon(word[1:],toSub,done+word[0]).union(GHC.substituteByEpsilon(word[1:],toSub,done))


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
            allDependances[Var]=GHC.alldependants(Var,directDpendants,set().copy())
        """ removing primitives variables"""
        for Var in list(allDependances):
            if allDependances[Var]==set():
                allDependances.pop(Var)
        return allDependances


    @staticmethod
    def alldependants(Var,directDependants,dependants=set().copy()):
        assert Var in directDependants,"Maybe you forgot to add %s to you Variables"%(Var)
        """ compute all dependants (ie Variables primitives) of a givven Var"""
        dependants.add(Var)
        newDependants=GHC.unionReducer([directDependants[D] for D in dependants]).difference(dependants)
        if(len(newDependants)!=0):
            dependants=dependants.union(newDependants)
            dependants=dependants.union(GHC.unionReducer([GHC.alldependants(V,directDependants,dependants) for V in newDependants]))
        return dependants.difference(Var)


    def productionOf(self,Var,done=set()):
        assert Var in self.V, "Rectifier la liste des variable pour contenir %s"%(Var)
        """Compute the non Variable production of each Variable """
        if Var not in self.P:
            return set()
        done.add(Var)
        return self.P[Var].difference(self.V).union(GHC.unionReducer([self.productionOf(D,done) for D in self.P[Var].intersection(self.V).difference(done)]))
    
    
    def substituteAll(self,Uepsilon):
        """Return a dictionary {Var: new set substitued} for each Var in V"""
        return {Var:GHC.unionReducer( [GHC.substituteByEpsilon(word,Uepsilon) for word in self.P[Var]]) for Var in self.P}
    
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
        super().copy(ghc)
        self.reduction()

    def reduction(self):
        V=self.accessiblesVariables().intersection(self.generatorVariables())
        P=dict()
        acceptedAlphabet=self.Sigma.union(V)
        """Elimination of word that containe an unccessible or an non generator variable """
        for Var in set(self.P).intersection(V):
            destinations={word if GHC.isIn(word,acceptedAlphabet) else 1 for word in self.P[Var]}
            try :
                destinations.remove(1)
            except KeyError:
                pass
            if (len(destinations)):
                P[Var]=destinations
        self.V=V
        self.P=P    

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
        self.P=self.substituteAll(Uepsilon)
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
        self.normalisation()

    def cyk(self,word):
        assert GHC.isIn(word,self.Sigma),"word %s not in alphabet %s"%(word,str(self.Sigma))
        n=len(word)
        T=pd.DataFrame([[list() for _ in range(n)] for _ in range(n)] )
        for i,wi in enumerate(word):
            Tii=[]
            for A in self.P:
                if wi in self.P[A]:
                    Tii.append(A)
            T[i][i].extend(Tii)
        
        for j in range(n):
            for i in reversed(range(j)):
                for k in range(i,j):
                    for A in self.P:
                        for B in T[i][k]:
                            for C in T[k+1][j]:
                                if B+C in self.P[A]:
                                    T[i][j].append(A)
        for i in range(n):
            for j in range(n):
                T[i][j]=set(T[i][j])
        T.to_html("cyk_nalyse.html")
        print("Analysis Table of the word %s :\n"%(word),T.transpose())

    def normalisation(self):
        self.substituteByNewVAriables()
        self.devidedRules()
    
    def substituteByNewVAriables(self):
        m=max([ord(A) for A in self.V])
        sigma=sorted(self.Sigma)
        translateDictionary={ord(a):i+m+1 for i,a in enumerate(sigma) }
        self.V=self.V.union(set([chr(V) for V in translateDictionary.values()]))
        for V in self.P:
            self.P[V]=set([word.translate(translateDictionary) for word in  self.P[V]])
        for i,a in enumerate(sigma):
            self.P[chr(i+m+1)]=set([a])
            self.V.add(chr(i+m+1))


    def devidedRules(self):
        m0=max([ord(A) for A in self.V])
        m=m0
        dividedRules=dict()
        for V in self.P:
            for w in list(self.P[V]):
                n=len(w)
                if n>2:
                    s=n-2
                    division={chr(i+m):{w[i+1]+chr(i+m+1)} for i in range(s-1)}
                    division.update({chr(m+s):{w[-2:]}})
                    self.P[V].remove(w)
                    self.P[V]=self.P[V].union({w[0]+chr(m+1)})
                    m+=s
                    dividedRules.update(division)
        self.P.update(dividedRules)
        self.V=self.V.union({chr(m0+i+1) for i in range(m-m0)})
if __name__ == "__main__":
    grammaire={
    "Sigma":"ahmad",
    "V":"ABC",
    "P":{
        "A":"ahB+ad",
        "B":"mA",
        "C":"d"
    },
    "S0":"A"
    }
    G=GHC(grammaire)
    print(G)
    chomsky=GHCChomsky(G)
    print(chomsky)
    chomsky.cyk("ahmad")
