#include<stdio.h>
#include<stdlib.h>
#include"../Headers/pile.h"


void testPile(void){
	pile*p= initialisePile();
	printf("Le pile est-t-il vide =%d [Y/N]=[1,0]:",isEmpty(p));
	printf("\nEmpiler\n");
	for (int i=0;i<5;i++)empiler(p,i);	
	printf("Le pile est-t-il vide =%d [Y/N]=[1,0]:",isEmpty(p));
	Afficher(p);
	printf("Depiler 3 elements");
	depilerKElt(p,3);
	Afficher(p);
	printf("depiler jusqu'a 0 \n");
	depilerElt(p,0);
	Afficher(p);
	}

noeud* creatNoeud(int val){
	noeud* new=(noeud*) malloc(sizeof(noeud));
	new->val=val;
	new->next=NULL;
	return new;
	}
	
	
	
pile* empiler(pile* p,int val){
	noeud* new=creatNoeud(val);
	new->next=p->deb;
	p->deb=new;
	return p;
}

int isEmpty(pile* p){
	 //1 si vide 0 si non
	 int isVide=0;
	 if (p->deb==NULL)isVide=1;
	 return isVide;
 }
 

int depiler(pile* p){
	if (isEmpty(p)){
	 return -1; }
	int val= p->deb->val;
	noeud* toRemove=p->deb;
	p->deb=p->deb->next;
	free(toRemove);
	return val;
	}

pile* initialisePile(){
	// Initialisation d'un pile
	pile* p;
	p=(pile*) malloc(sizeof(pile));
	p->deb=NULL;
	return p;
}
int Afficher(pile* p){
	if(isEmpty(p))return 0;
	pile* temp=initialisePile();
	printf("\nDEB ---> ");
	while (!isEmpty(p)){
	int val;
	val= depiler(p);
	empiler(temp,val);
	printf("%d ---> ",val);
	}
	while (!isEmpty(temp))	empiler(p,depiler(temp));
	printf("NULL\n");
	return 1;
	}
void depilerKElt(pile* p,int k){
	int i=0;
	while(!isEmpty(p)&& i<k){
	depiler(p);
	i++;
	};
}
void depilerElt(pile* p, int elt){
	while(!isEmpty(p)&& elt!=depiler(p));
}

