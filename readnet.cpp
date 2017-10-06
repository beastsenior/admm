#include "stdio.h"

#define N 200  //max number of node

int main()
{
	int n;  //number of node
	float net[N][N];  //adjacency matrix of network
	float randnum;  //value of the networking delay
	FILE *fp; //pointer of net.txt
	int i,j,k;

	if((fp=fopen("net.txt", "r"))== NULL)
	{
		printf("The file can not be opened.\n");
		return -1;
	}
	fscanf(fp,"%d\n",&n);
	printf("%d\n",n);
	
	for(i=0;i<N;i++) for(j=0;j<N;j++) net[i][j]=0.0;
	for(k=0;k<n*n;k++)
	{
		fscanf(fp,"%d<->%d %f\n", &i, &j, &randnum);
		net[i][j]=randnum;
	}
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			printf("%d<->%d %f\n", i, j, net[i][j]);
		}
	}

	return 0;
}