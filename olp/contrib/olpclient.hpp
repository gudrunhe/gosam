#ifndef __OLPCLIENT_HPP__
#define __OLPCLIENT_HPP__

#include <stdlib.h>

namespace olp
{

class OLPClient
{
public:
	OLPClient(char* hostname="localhost", int port=7711);
	OLPClient(const OLPClient& other);
	~OLPClient(void);

	const char* getHostname(void) const;
	int getPort(void) const;

	void close(void);

	/* buffer contains the message before the call and the response
	 * after the call. Its size musst be large enough to hold the
	 * response from the server
	 */
	int send(char* buffer, int buf_size) const;

	char* who(void) const;
	int bye(void) const;
	int shutdown(void) const;
	int restart(void) const;

	int setOption(const char* name, int value) const;
	int setOption(const char* name, double value) const;
	int setOption(const char* name, double re, double im) const;

	void EvalSubProcess(int l,
			int num_momenta, const double* mom, double mu,
			int num_parameter, const double* par,
			double* r) const;
	inline void operator() (int l,
			int num_momenta, const double* mom, double mu,
			int num_parameter, const double* par,
			double* r) const
	{
		this->EvalSubProcess(l, num_momenta, mom, mu,
				num_parameter, par, r);
	}

private:
	char* _hostname;
	int _port;
	int _sock;

	int connect(void);
};

} //namespace

#endif
