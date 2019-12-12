#include <stdio.h>

double sigmoid(double x){
	float sigmoidValue;
	sigmoidValue =1/(1+exp(-x));
	return sigmoidValue
}

int main(){
	int b;
	b=sigmoid(3);
	printf("%d",b)
}
