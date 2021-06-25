import Noeud as Noeud
import Pile as Pile


class File:
    def __init__(self):
        self.deb = None

    def __repr__(self):
        temp = File()
        representer = "END<---"
        while self.deb:
            temp.emfiler(self.defiler())
            representer += str(temp.deb.val) + "<---"
        representer += "DEB"
        while temp.deb:
            self.emfiler(temp.defiler())
        return representer

    def emfiler(self, val):
        new = Noeud.Noeud(val)
        new.next = self.deb
        self.deb = new

    def defiler(self):
        if self.estVide():
            return None
        beforlast = last = self.deb
        while last.next != None:
            beforLast = last
            last = last.next
        val = last.val
        if last == beforlast:
            self.deb = None
            del last, beforlast
        else:
            del last
            beforLast.next = None
        return val

    def estVide(self):
        return self.deb == None

    def defiletElt(self, elt):
        while self.deb:
            if self.defiler() == elt:
                break

    def inverser(self):
        if self.estVide():
            return None
        temp = Pile.Pile()
        while not (self.estVide()):
            temp.empiler(self.defiler())
        while not (temp.estVide()):
            self.emfiler(temp.depiler())
