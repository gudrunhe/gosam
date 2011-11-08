# vim: ts=3:sw=3

import socket

class OLPClientException(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return str(self.value)

class OLPClient:
	def __init__(self, hostname='127.0.0.1', port=7711):
		self._hostname = hostname
		self._port = port

		s = None
		for res in socket.getaddrinfo(self._hostname, self._port,
				socket.AF_UNSPEC, socket.SOCK_STREAM):
			af, socktype, proto, canonname, sa = res
			try:
			  	s = socket.socket(af, socktype, proto)
			except socket.error, msg:
				s = None
				continue
			try:
			 	s.connect(sa)
			except socket.error, msg:
				s.close()
				s = None
				continue
			break
		if s is None:
			raise OLPClientException, 'could not open socket'

		self._socket = s

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	def close(self):
		if self._socket is not None:
			self._socket.close()
			self._socket = None

	def bye(self):
		self.send("BYE\n", True)

	def shutdown(self):
		self.send("SHUTDOWN\n", True)

	def who(self):
		code, msg = self.send("WHO\n", True)
		return msg

	def option(self, name, value):
		if isinstance(value, complex):
			code, msg = self.send("OPTION %s=%24.16e,%24.16e\n"
					% (name, value.real, value.imag), True)
		elif isinstance(value, float):
			code, msg = self.send("OPTION %s=%24.16e\n" % (name, value), True)
		else:
			code, msg = self.send("OPTION %s=%s\n" % (name, value), True)

		return self

	def restart(self):
		code, msg = self.send("RESTART\n", True)

	def __setitem__(self, name, value):
		return self.option(name, value)

	def EvalSubProcess(self, label, momenta, mu, parameter):
		if len(momenta) % 5 != 0:
			raise OLPClientException, \
				"list of momenta must be of length which is a multiple of five."
		num_legs  = len(momenta) / 5
		num_param = len(parameter)
		self.send("EVENT %d %d\n" % (num_legs, num_param), True)
		for i in range(num_legs):
			mom = " ".join(map(lambda x: "%24.16e" % x, momenta[5*i:5*(i+1)]))
			self.send("MOMENTUM %d %s\n" % (i, mom), True)

		for i, p in enumerate(parameter):
			self.send("PARAMETER %d %24.16e\n" % (i, p), True)

		code, msg = self.send("SUBPROCESS %d %24.16e\n" % (label, mu), True)

		return map(float, filter(lambda s: len(s) > 0, msg.split(" ")))

	def send(self, line, check_error=False):
		if self._socket is None:
			raise OLPClientException, 'tried to send after socket has been closed'
		self._socket.send(line)
		data = self._socket.recv(1024)
		code, msg = data.split(" ", 1)
		if check_error:
			if int(code) != 200:
				raise OLPClientException, msg

		return int(code), msg.strip()


if __name__ == "__main__":

	olp = OLPClient()
	print olp.who()
	olp["samurai_scalar"] = 2
	res = olp.EvalSubProcess(0,
			[7.0,  0.0,  0.0,  7.0, 0.0,
			 7.0,  0.0,  0.0, -7.0, 0.0,
			 7.0,  5.6,  0.0,  4.2, 0.0,
			 7.0, -5.6,  0.0, -4.2, 0.0],
			2.7,
			[0.1183])

	print res[0]
	print res[1]
	print res[2]
	print res[3]

	olp.bye()
	#olp.shutdown()
	olp.close()
	print "Done"

