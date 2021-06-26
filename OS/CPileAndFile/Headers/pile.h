#ifndef PILE_H_
#define PILE_H_
#include"noeud.h"

typedef struct pile{
	noeud* deb;
}pile;


noeud* creatNoeud(int);
pile* empiler(pile*,int);
int isEmpty(pile*);
int depiler(pile* );
pile* initialisePile(void);
int Afficher(pile* );
void depilerKElt(pile*,int );
void depilerElt(pile*, int);
void testPile(void);
#endif // FOO_H_

