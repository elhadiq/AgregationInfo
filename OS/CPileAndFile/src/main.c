#include <stdio.h>
#include "../Headers/file.h"
int main(void)
{
	char select='P';
	printf("Voulez vous tester les pile uu bien les files [P\\f]: ");
	scanf("%c",&select);
	if (select=='f'||select=='F')testFile();
	else 	testPile();
	return 0;
}

