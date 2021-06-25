#ifndef FILE_H_
#define FILE_H_
#include"noeud.h"
#include"pile.h"

typedef struct file{
	noeud* deb;
}file;


file* emfiler(file*,int);
int isEmptyFile(file*);
int defiler(file* );
file* Initialisefile(void);
int AfficherFile(file* );
void defilerKElt(file*,int );
void defilerElt(file*, int);
file* inverser(file*);
void testFile(void);
#endif // FILE_H_

