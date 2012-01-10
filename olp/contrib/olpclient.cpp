
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>

#include "olpclient.hpp"

olp::OLPClient::OLPClient(char* hostname, int port)
{
	int stat;
	this->_port = port;
	this->_hostname = strdup(hostname);
	this->_sock = -1;
	stat = this->connect();
	if (stat < 0) throw "Could not establish connection";
}

olp::OLPClient::OLPClient(const OLPClient& other)
{
	int stat;
	this->_port = other.getPort();
	this->_hostname = strdup(other.getHostname());
	this->_sock = -1;
	stat = this->connect();
	if (stat<0) throw "Could not establish connection";
}

int olp::OLPClient::connect(void)
{
	struct sockaddr_in sin;
	struct sockaddr_in pin;
	struct hostent *hp;
	int stat;

	hp = gethostbyname(this->_hostname);
	if (hp == NULL) return -1;

	memset(&pin, 0, sizeof(pin));
	pin.sin_family = AF_INET;
	pin.sin_addr.s_addr = ((struct in_addr *)(hp->h_addr))->s_addr;
	pin.sin_port = htons(this->_port);

	this->_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (this->_sock == -1) return -2;

	stat = ::connect(this->_sock, (struct sockaddr *)  &pin, sizeof(pin));
	if (stat == -1)
	{
		::close(this->_sock);
		this->_sock = -1;
		return -3;
	}

	return 0;
}

void olp::OLPClient::close(void)
{
	if (this->_sock >= 0) ::close(this->_sock);
	this->_sock = -1;
}

olp::OLPClient::~OLPClient(void)
{
	this->close();
	free(this->_hostname);
}

const char* olp::OLPClient::getHostname(void) const
{
	return this->_hostname;
}

int olp::OLPClient::getPort(void) const
{
	return this->_port;
}


char* olp::OLPClient::who(void) const
{
	char buff[128];
	int stat;

	strcpy(buff, "WHO");
	stat = this->send(buff, 128);
	if(stat != 200) return NULL;

	return strdup(buff);
}

int olp::OLPClient::bye(void) const
{
	char buff[128];
	int stat;

	strcpy(buff, "BYE");
	stat = this->send(buff, 128);
	return stat;
}

int olp::OLPClient::shutdown(void) const
{
	char buff[128];
	int stat;

	strcpy(buff, "SHUTDOWN");
	stat = this->send(buff, 128);
	return stat;
}

int olp::OLPClient::restart(void) const
{
	char buff[128];
	int stat;

	strcpy(buff, "RESTART");
	stat = this->send(buff, 128);
	return stat;
}

int olp::OLPClient::send(char* buffer, int buf_size) const
{
	int stat;
	char my_buffer[1024];

	if(this->_sock < 0) return -1;

	strncpy(my_buffer, buffer, 1022);
	strcat(my_buffer, "\n");
	stat = ::send(this->_sock, my_buffer, strlen(my_buffer), 0);
	if (stat == -1) return -1;

	stat = ::recv(this->_sock, my_buffer, 1023, 0);
	if (stat == -1) return -1;

	my_buffer[stat] = '\0';
	my_buffer[3] = '\0';

	stat = atoi(my_buffer);
	strncpy(buffer, &(my_buffer[4]), buf_size - 1);
	
	return stat;
}

int olp::OLPClient::setOption(const char* name, int value) const
{
	char buff[128];
	int stat;

	sprintf(buff, "OPTION %s=%d", name, value);
	stat = this->send(buff, 128);
	return stat;
}

int olp::OLPClient::setOption(const char* name, double value) const
{
	char buff[128];
	int stat;

	sprintf(buff, "OPTION %s=%24.16e", name, value);
	stat = this->send(buff, 128);
	return stat;
}

int olp::OLPClient::setOption(const char* name, double re, double im) const
{
	char buff[128];
	int stat;

	sprintf(buff, "OPTION %s=%24.16e,%24.16e", name, re, im);
	stat = this->send(buff, 128);
	return stat;
}

void olp::OLPClient::EvalSubProcess(int l,
			int num_momenta, const double* mom, double mu,
			int num_parameter, const double* par,
			double* r) const
{
	char buff[256];

	r[0] = 0.0;
	r[1] = 0.0;
	r[2] = 0.0;
	r[3] = -1.0;

	sprintf(buff, "EVENT %d %d", num_momenta, num_parameter);
	if(this->send(buff, 256) != 200) return;

	for(int i = 0; i < num_momenta; ++i)
	{
		sprintf(buff,
			"MOMENTUM %d %24.16e %24.16e %24.16e %24.16e %24.16e",
			i, mom[i*5+0], mom[i*5+1],
			mom[i*5+2], mom[i*5+3], mom[i*5+4]);
		if(this->send(buff, 256) != 200) return;
	}
	for(int i = 0; i < num_parameter; ++i)
	{
		sprintf(buff, "PARAMETER %d %24.16e", i, par[i]);
		if(this->send(buff, 256) != 200) return;
	}

	sprintf(buff, "SUBPROCESS %d %24.16e", l, mu);
	if(this->send(buff, 256) != 200) return;

	int i = 0;
	for(char* pch = strtok(buff, " "); pch != NULL; pch = strtok(NULL, " "))
	{
		if (strlen(pch) == 0) continue;
		r[i++] = atof(pch);
	}
}
