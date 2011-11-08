// vim:ts=3:sw=3


import java.io.*;
import java.net.*;

public class OLPClient
{

	public static class Response
	{
		private int code;
		private String message;

		private Response(int code, String message)
		{
			this.code = code;
			this.message = message;
		}

		public int getCode() { return this.code; }
		public String getMessage() { return this.message; }

		public String toString()
		{
			return Integer.toString(this.code) + " " + this.message;
		}
	}

	private final static int DEFAULT_PORT = 7711;

	private String inet_addr;
	private int port;
	private Socket socket;
	private PrintStream out;
 	private InputStream in;

	public OLPClient()
		throws UnknownHostException, IOException
	{
		this("127.0.0.1", DEFAULT_PORT);
	}

	public OLPClient(String inet_addr)
		throws UnknownHostException, IOException
	{
		this(inet_addr, DEFAULT_PORT);
	}

	public OLPClient(int port)
		throws UnknownHostException, IOException
	{
		this("127.0.0.1", port);
	}

	public OLPClient(String inet_addr, int port)
		throws UnknownHostException, IOException
	{
		this.inet_addr = inet_addr;
		this.port = port;

		this.socket = new Socket(inet_addr, port);
		this.in = this.socket.getInputStream();
		this.out = new PrintStream(this.socket.getOutputStream());

		this.out.flush();
	}

	public synchronized void close()
		throws IOException
	{
		if (this.in != null)
		{
			this.in.close();
			this.in = null;
		}
		if (this.out != null)
		{
			this.out.close();
			this.out = null;
		}
		if (this.socket != null)
		{
			this.socket.close();
			this.socket = null;
		}
	}

	public void finalize()
	{
		if (this.in != null)
		{
			try
			{
				this.in.close();
			}
			catch(IOException ex) { /* ignore it */ }

			this.in = null;
		}
		if (this.out != null)
		{
			this.out.close();
			this.out = null;
		}
		if (this.socket != null)
		{
			try
			{
				this.socket.close();
			}
			catch(IOException ex) { /* ignore it */ }

			this.socket = null;
		}
	}

	public Response send(String message)
		throws IOException
	{
		byte[] rcv_buf = new byte[1024];
		int bytes;
		int code;

		this.out.println(message);
		bytes = this.in.read(rcv_buf, 0, 1024);

		if (bytes >= 3)
		{
			code = 100 * (rcv_buf[0] - '0')
				+ 10 * (rcv_buf[1] - '0')
				+ rcv_buf[2] - '0';

			return new Response(code, new String(rcv_buf, 4, bytes - 4));
		}

		return null;
	}

	public String who()
		throws IOException
	{
		Response r = this.send("WHO");
		if(r.getCode() == 200)
			return r.getMessage();
		else
			return null;
	}

	public int bye()
		throws IOException
	{
		Response r = this.send("BYE");
		return r.getCode();
	}

	public int shutdown()
		throws IOException
	{
		Response r = this.send("SHUTDOWN");
		return r.getCode();
	}

	public int restart()
		throws IOException
	{
		Response r = this.send("RESTART");
		return r.getCode();
	}

	public int setOption(String name, int value)
		throws IOException
	{
		Response r = this.send("OPTION " + name + "=" + Integer.toString(value));
		return r.getCode();
	}

	public int setOption(String name, double value)
		throws IOException
	{
		Response r = this.send("OPTION " + name + "=" +
				Double.toString(value));
		return r.getCode();
	}

	public int setOption(String name, float value)
		throws IOException
	{
		Response r = this.send("OPTION " + name + "=" +
				Float.toString(value));
		return r.getCode();
	}

	public int setOption(String name, float re, float im)
		throws IOException
	{
		Response r = this.send("OPTION " + name + "=" +
				Float.toString(re) + "," + Float.toString(im));
		return r.getCode();
	}

	public int setOption(String name, double re, double im)
		throws IOException
	{
		Response r = this.send("OPTION " + name + "=" +
				Double.toString(re) + "," + Double.toString(im));
		return r.getCode();
	}

	public boolean EvalSubProcess(int label,
			double[] momenta, double mu, double[] parameter, double[] result)
		throws IOException
	{
		Response r;
		String line;
		int num_legs, num_parameter;

		if(momenta.length % 5 == 0)
			num_legs = momenta.length / 5;
		else
			throw new IllegalArgumentException(
					"length of momenta must be multiple of 5");
		num_parameter = parameter.length;

		r = this.send("EVENT " + num_legs + " " + num_parameter);
		if (r.getCode() != 200) return false;

		for(int i = 0; i < num_legs; ++i)
		{
			r = this.send(String.format(
						"MOMENTUM %d %24.16e %24.16e %24.16e %24.16e %24.16e",
						i, momenta[i*5+0], momenta[i*5+1], momenta[i*5+2],
						momenta[i*5+3], momenta[i*5+4]));
			if (r.getCode() != 200) return false;
		}

		for(int i = 0; i < num_parameter; ++i)
		{
			r = this.send(String.format("PARAMETER %d %24.16e", i, parameter[i]));
			if (r.getCode() != 200) return false;
		}
		
		r = this.send(String.format("SUBPROCESS %d %24.16e", label, mu));
		if (r.getCode() != 200) return false;
		line = r.getMessage();

		int i = 0;
		for (String token : line.split(" "))
		{
			if (token.length() == 0) continue;
			if (i >= result.length) return false;
			try
			{
				result[i++] = Double.parseDouble(token);
			}
			catch(NumberFormatException ex)
			{
				return false;
			}
		}
		return i == result.length;
	}

	public static void main(String[] args)
		throws IOException
	{
		double[] parameter = new double[1];
		double[] momenta = new double[20];
		double[] result = new double[4];

		OLPClient client = new OLPClient();
		System.out.println(client.who());

		client.setOption("samurai_scalar", 2);

		momenta[0] = 7.0;
		momenta[3] = 7.0;
		momenta[5] = 7.0;
		momenta[8] = -7.0;
		momenta[10] = 7.0;
		momenta[11] = 5.6;
		momenta[13] = 4.2;
		momenta[15] = 7.0;
		momenta[16] = -5.6;
		momenta[18] = -4.2;

		parameter[0] = 0.1183;

		client.EvalSubProcess(0, momenta, 2.7, parameter, result);

		System.out.println(result[0]);
		System.out.println(result[1]);
		System.out.println(result[2]);
		System.out.println(result[3]);

		client.bye();
		client.close();
	}
}

