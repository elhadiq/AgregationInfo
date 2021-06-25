message="INFORMATION RESEAUX ET COMMUNICATIONS"
def compterOccurences(message):
    #enlever les espaces
    msg="".join(message.split(' '))
    NbOccurences=dict()
    for c in msg:
        try:
            NbOccurences[c]+=1
        except:
            NbOccurences[c]=1
    return NbOccurences
trierParOccurences =lambda NbOccurences:sorted(NbOccurences.items(), key=lambda tup: tup[1])
initialisationsCodes=lambda NbOccurences:{A:"" for A in NbOccurences}
getWieght=lambda sortedList:sum([s[1] for s in sortedList])
diffWeigth=lambda gauche,droite:abs(getWieght(gauche)-getWieght(droite))
def divide(sortedList):
    assert len(sortedList)>1, "i cant divide this list"
    if len(sortedList)==2:
        return sortedList[:1],sortedList[1:]
    n=len(sortedList)
    gauch,droite=sortedList[:n//2+1],sortedList[n//2+1:]
    m=abs(getWieght(gauch)-getWieght(droite))
    for i in range(n//2,n-1):
        tG,tD=sortedList[:i+1],sortedList[i+1:]
        diff=diffWeigth(tG,tD)
        if diff<m:
            m=diff
            gauch,droite=tG,tD
    return gauch,droite

def affectBits(srtList,codageDict):
    if len(srtList)<=1:
        pass
    else:
        g,d=divide(srtList)
        for C,_ in g:
            codageDict[C]="0"+codageDict[C]
        for C,_ in d:
            codageDict[C]="1"+codageDict[C]
        affectBits(d,codageDict)
        affectBits(g,codageDict)
def shanonFanon(message):
    NbOccurences=compterOccurences(message)
    srt=trierParOccurences(NbOccurences)
    codageDict=initialisationsCodes(NbOccurences)
    affectBits(srt,codageDict)
    codedMessage="".join([codageDict[C] if C!=" " else " " for C in message])
    return codedMessage,codageDict
def decoderShanonFanon(codedMessage,codageDict):
    message=""
    bande=codedMessage[:]
    decodeDict={codageDict[C]:C for C in codageDict}
    decodeDict[" "]=" "
    i=0
    while i<len(bande)>1:
        i=1
        notfound=True
        while notfound and i<len(bande):
            code=bande[:i]
            try:
                decode=decodeDict[code]
                notfound=False
            except:
                i+=1
        message+=decode
        bande=bande[i:]
    return message
codedMessage,codageDict=shanonFanon(message)
print(decoderShanonFanon(codedMessage,codageDict))