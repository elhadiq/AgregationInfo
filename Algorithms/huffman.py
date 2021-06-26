from ShannonFano import compterOccurences,decoder
TrierParField =lambda listtuple,i:sorted(listtuple, key=lambda tup: tup[i])
def fusionerArbres(A1,A2):
    return [[A1[0]+A2[0],[A1[0],A1[1],A1[2]],[A2[0],A2[1],A2[2]]]]
def constructArbre(message):
    dicttOcurences=compterOccurences(message)
    noeuds=[[dicttOcurences[C],C,[]] for C in dicttOcurences]
    while len(noeuds)>1:
        noeuds=TrierParField(noeuds,0)
        noeuds=fusionerArbres(noeuds[0],noeuds[1])+noeuds[2:]
    return noeuds[0]
def AffectationPrefixe(arbre,codage,prefixe):
    if arbre[2]==[]:
        codage[arbre[1]]=prefixe
    else:
        AffectationPrefixe(arbre[1],codage,prefixe+"0")
        AffectationPrefixe(arbre[2],codage,prefixe+"1")
def codageHoffman(message):
    arbre=constructArbre(message)
    codageDict=dict()
    AffectationPrefixe(arbre,codageDict,"")
    codedMessage="".join([codageDict[C] for C in message])
    return codedMessage,codageDict

if __name__=='__main__':
    message="Hey Every One"
    codedMessage,codageDict=codageHoffman(message)
    print(decoder(codedMessage,codageDict))