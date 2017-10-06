#include "stdio.h"
#include "stdlib.h"
#include "time.h"

#define N 200  //max number of node
#define RATE 0.5  //rate of the connection of node to node

int main(int argc, char *argv[]) 
{
	int n;  //number of node
	float net[N][N];  //adjacency matrix of network
	float randnum;  //value of the networking delay
	FILE *fp; //pointer of net.txt
	int i,j;
	
	
	/*write the number of node to net.txt*/
	if(argc==1) n=20;  //default number of node is 20
	else if(argc==2) n=atoi(argv[1]);
	else
	{
		printf("argc error");
		return -1;
	}
	if((fp=fopen("net.txt", "w"))== NULL)
	{
		printf("The file can not be opened.\n");
		return -1;
	}
	fprintf(fp,"%d\n",n);

	
	/*write the value of delay to net.txt*/	
	srand((int)time(NULL));
	for(i=0;i<N;i++) for(j=0;j<N;j++) net[i][j]=0.0;
	for(i=0;i<n;i++)
	{
		for(j=0;j<i;j++)
		{
			randnum=(float)rand()/(float)RAND_MAX;
			if(randnum>RATE) net[i][j]=net[j][i]=randnum-RATE;  //RATE is the rate of the connection of node to node
		}
	}	
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			fprintf(fp, "%d<->%d %f\n", i, j, net[i][j]);
		}
	}	
	

	fclose(fp);
	return 0; 
}