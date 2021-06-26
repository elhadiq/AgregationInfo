#include<stdio.h>
#include<stdlib.h>
#include"../Headers/file.h"


void testFile(){
	printf("in file.c\n");
	file* f=Initialisefile();
	AfficherFile(f);
	printf("Le file est-t-il vide =%d [Y/N]=[1,0]:",isEmptyFile(f));
	for(int i=0; i<5;i++)emfiler(f,i);
	AfficherFile(f);
	printf("Inverser File");
	inverser(f);
	AfficherFile(f);
	printf("Le file est-t-il vide =%d [Y/N]=[1,0]:\n",isEmptyFile(f));
	printf("Defiler(void): %d",defiler(f));
	AfficherFile(f);
	printf("Defiler 2 elements:");
	defilerKElt(f,2);
	AfficherFile(f);
	printf("Defiler l'element 3:");
	defilerElt(f,3);
	AfficherFile(f);
}


file* Initialisefile(){
	// Initialisation d'un pile
	file* f;
	f=(file*) malloc(sizeof(file));
	f->deb=NULL;
	return f;
}
int isEmptyFile(file* f){
		 //1 si vide 0 si non
	 int isVide=0;
	 if (f->deb==NULL)isVide=1;
	 return isVide;
}

file* emfiler(file* f,int val){
	noeud* new=creatNoeud(val);
	new->next=f->deb;
	f->deb=new;
	return f;
}

int defiler(file* f){
	if (isEmptyFile(f))return -1;
	int val;
	if (f->deb->next==NULL){
		val =f->deb->val;
		free(f->deb);
		f->deb=NULL;
	}
	else{
	noeud* last=f->deb;
	noeud* prevousLast=f->deb;
	while(last->next!=NULL){
		prevousLast=last;
		last=last->next;
	}
	val=last->val;
	free(last);
	prevousLast->next=NULL;
	}
	return val;
}

int AfficherFile(file* f){
	printf("\nNULL <--- ");
	if(isEmptyFile(f)){
	printf("DEB\n");
	return 0;
	}
	file* temp=Initialisefile();

	while (!isEmptyFile(f)){
	int val;
	val= defiler(f);
	emfiler(temp,val);
	printf("%d <--- ",val);
	}
	while (!isEmptyFile(temp))	emfiler(f,defiler(temp));
	printf("DEB\n");
	return 1;
	}
	
void defilerKElt(file* f,int k){
	int i=0;
	while(!isEmptyFile(f)&& i<k){
	defiler(f);
	i++;
	};
}

void defilerElt(file* f, int elt){
	while(!isEmptyFile(f)&& elt!=defiler(f));
}
file* inverser(file* f){
        if (isEmptyFile(f)) return f;
        pile* temp =initialisePile();
        while(!isEmptyFile(f))empiler(temp,defiler(f));
        while(!isEmpty(temp))emfiler(f,depiler(temp));
        return f;
        }
