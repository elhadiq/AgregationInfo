all: mon_exe

mon_exe: foo.o bar.o
	gcc foo.o bar.o -o mon_exe

foo.o: foo.c
	gcc -c foo.c -o foo.o
bar.o: bar.c bar.h
	gcc -c bar.c -o bar.o

