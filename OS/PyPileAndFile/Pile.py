import Noeud as Noeud


class Pile:
    def __init__(self):
        self.deb = None

    def empiler(self, val):
        new = Noeud.Noeud(val)
        new.next = self.deb
        self.deb = new

    def depiler(self):
        if self.estVide():
            return None
        toRemove = self.deb
        self.deb = toRemove.next
        val = toRemove.val
        del toRemove
        return val

    def estVide(self):
        return self.deb == None

    def __repr__(self):
        temp = Pile()
        representer = "DEB--->"
        while self.deb:
            temp.empiler(self.depiler())
            representer += str(temp.deb.val) + "--->"
        representer += "END"
        while temp.deb:
            self.empiler(temp.depiler())
        return representer

    def depilerKElet(self, k):
        i = 0
        while i < k and not (self.estVide()):
            self.depiler()
            i += 1

    def depilerElt(self, elt):
        while not (self.estVide()):
            if self.depiler() == elt:
                break

    def contient(self, elet):
        if self.estVide():
            return False
        temp = Pile()
        contient = False
        while not (self.estVide()):
            temp.empiler(self.depiler())
            if elet == temp.deb.val:
                contient = True
                break
        while not (temp.estVide()):
            self.empiler(temp.depiler())
        return contient
