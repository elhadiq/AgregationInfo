all: mon_exe

mon_exe: f1.o f2.o 
	gcc f1.o f2.o -o mon_exe
f1.o: f1.c f1.h
	gcc -c f1.c -o f1.o
f2.o: f2.c
	gcc -c f2.c -o f2.o
