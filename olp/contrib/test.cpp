
#include <cstdio>
#include "olpclient.hpp"

using namespace olp;
using namespace std;

int main(int argc, char** argv)
{
	double mom[20];
	double par[1];
	double r[4];

	mom[0] = 7.0;
	mom[3] = 7.0;
	mom[5] = 7.0;
	mom[8] = -7.0;
	mom[10] = 7.0;
	mom[11] = 5.6;
	mom[13] = 4.2;
	mom[15] = 7.0;
	mom[16] = -5.6;
	mom[18] = -4.2;

	par[0] = 0.1183;

	try
	{
		OLPClient client("localhost", 4711);
		char* name = NULL;
		name = client.who();

		printf("Connected with %s\n", name);
		if(name != NULL) free(name);

		int stat = client.setOption("samurai_scalar", 2);
		if (stat != 200)
			printf("Could not set samurai_scalar\n");
		else
			client.restart();

		client(0, 4, mom, 2.7, 1, par, r);

		printf("0: %24.16e\n", r[0]);
		printf("1: %24.16e\n", r[1]);
		printf("2: %24.16e\n", r[2]);
		printf("3: %24.16e\n", r[3]);

		client.bye();
	}
	catch(char const* err)
	{
		fprintf(stderr, "Error: %s\n", err);
	}


	return 0;
}
