/* vim: ts=3:sw=3:expandtab
 */
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <signal.h>
#include <fcntl.h>

#include "olp_daemon.h"
#include "olp.h"

int serversock, clientsock;
struct sockaddr_in server, client;
int bye_requested, shutdown_requested;
int restart_allowed, shutdown_allowed;
int port;

char* log_file_name;
char* file_name;

event_type evt;

void log_message(char* message)
{
   FILE *logfile;

   if (log_file_name == NULL) {
      fprintf(stderr, "%s", message);
   }
   else
   {
   	logfile=fopen(log_file_name, "a");
	   if(!logfile) return;
   	fprintf(logfile,"%s\n", message);
	   fclose(logfile);
   }
}

/* Clean up everything before we quit */
void cleanup(void)
{
   if(serversock>=0) close(serversock);
   if(clientsock>=0) close(clientsock);
#ifdef GOLEMEXTENSIONS
   OLP_Finalize();
#endif
}


/* An easy way of quitting the program. */
void die(char *mess)
{
   cleanup();
   log_message(mess);
   exit(1);
}

/* This handler will be installed to ensure we clean up
 * when some one sends us SIGINT (e.g. pressing CTRL-C)
 */
void ctrl_c_handler(int sig)
{
   cleanup();
   exit(0);
}

void print_usage(void)
{
   puts("usage: olp_daemon [-p port] [-s|-S] [-f] file_name");
   puts("  -f file_name      name of a contract file");
   puts("  -p port           port at which the program accepts connections");
   puts("  -s                disallow SHUTDOWN command");
   puts("  -S                allow SHUTDOWN command [default]");
   puts("  -r                disallow RESTART command");
   puts("  -R                allow RESTART command [default]");
   puts("  -d                detach from terminal (run as daemon)");
}

void daemon_signal_handler(int sig)
{
   switch(sig)
   {
   case SIGHUP:
      log_message("hangup signal catched");
      break;
   case SIGTERM:
      log_message("terminate signal catched");
      cleanup();
      exit(0);
      break;
   }
}


void daemonize(void)
{
   int i,lfp, fd_stdout, fd_stderr;
   char str[128];

	if(getppid() == 1)
      return; /* already a daemon */
	i = fork();
	if (i < 0) exit(1); /* fork error */
	if (i > 0) exit(0); /* parent exits */
	/* child (daemon) continues */

	setsid(); /* obtain a new process group */
	for (i = getdtablesize(); i >= 0; --i)
      close(i); /* close all descriptors */

	i = open("/dev/null",O_RDWR);
   fd_stdout = dup(i);
   fd_stderr = dup(i);
	umask(027); /* set newly created file permissions */
	i = chdir(DAEMON_RUNDIR); /* change running directory */
   sprintf(str, "%s.%d.log", PROGNAME, port);
   log_file_name = strdup(str);

   sprintf(str, "%s.%d.lock", PROGNAME, port);
	lfp = open(str, O_RDWR | O_CREAT, 0640);
	if (lfp < 0)
   {
      sprintf(str, "Cannot open lock file %s.%d.lock\n", PROGNAME, port);
      die(str);
   }

	if (lockf(lfp, F_TLOCK, 0) < 0)
   {
      sprintf(str, "Cannot obtain lock for %s.%d.lock\n", PROGNAME, port);
      die(str);
   }

	/* first instance continues */
	sprintf(str, "%d\n", getpid());
	i = write(lfp, str, strlen(str)); /* record pid to lockfile */

	signal(SIGCHLD,SIG_IGN); /* ignore child */
	signal(SIGTSTP,SIG_IGN); /* ignore tty signals */
	signal(SIGTTOU,SIG_IGN);
	signal(SIGTTIN,SIG_IGN);
	signal(SIGHUP, daemon_signal_handler); /* catch hangup signal */
	signal(SIGTERM, daemon_signal_handler); /* catch kill signal */
}

void send_message(int response_code, const char* message)
{
   char send_buffer[256+6];
   int l;
      
   sprintf(send_buffer, "%03d ", response_code);
   strncat(send_buffer, message, 256);
   strcat(send_buffer, "\n");
   l = strlen(send_buffer);

   #ifdef MSG_NOSIGNAL
   if (send(clientsock, send_buffer, l, MSG_NOSIGNAL) != l) {
   #else
   if (send(clientsock, send_buffer, l, 0) != l) {
   #endif
      if(! bye_requested)
      {
         log_message("Failed to send bytes to client\n");
         bye_requested = 1;
      }
   }
}

void startup(int argc, char** argv)
{
   int ierr;
   int port_flg, shut_flg, rest_flg, file_flg, daemon_flg, errflg;
   char c;
   char str_buf[64];

   extern char *optarg;
   extern int optind, optopt;

   log_file_name = NULL;

   port_flg = 0;
   shut_flg = 0;
   rest_flg = 0;
   file_flg = 0;
   daemon_flg = 0;

   errflg = 0;

   shutdown_allowed = DEFAULT_ALLOW_SHUTDOWN;
   restart_allowed = DEFAULT_ALLOW_RESTART;
   port = DEFAULT_PORT;
   file_name = NULL;

   /* Read command line options */
   while ((c = getopt(argc, argv, ":p:f:sSdhrR")) != -1)
   {
      switch(c) {
      case 'd':
         if(daemon_flg)
            errflg++;
         else
            daemon_flg++;
         break;
      case 'h':
         print_usage();
         exit(0);
      case 'r':
         if (rest_flg)
            errflg++;
         else
         {
            rest_flg++;
            restart_allowed = 0;
         }
         break;
      case 'R':
         if (rest_flg)
            errflg++;
         else
         {
            rest_flg++;
            restart_allowed = 1;
         }
         break;
      case 's':
         if (shut_flg)
            errflg++;
         else
         {
            shut_flg++;
            shutdown_allowed = 0;
         }
         break;
      case 'S':
         if (shut_flg)
            errflg++;
         else
         {
            shut_flg++;
            shutdown_allowed = 1;
         }
         break;
      case 'p':
         if (port_flg)
            errflg++;
         else
         {
            port_flg++;
            port = atoi(optarg);
         }
         break;
      case 'f':
         if (file_flg)
            errflg++;
         else
         {
            file_flg++;
            file_name = optarg;
         }
         break;
      case ':': 
         fprintf(stderr,
            "Option -%c requires an operand\n", optopt);
         errflg++;
         break;
      case '?':
         fprintf(stderr,
            "Unrecognized option: -%c\n", optopt);
         errflg++;
      }
   }
   for ( ; optind < argc; optind++)
   {
      if (file_flg)
         errflg++;
      else
      {
         file_flg++;
         file_name = argv[optind];
      }
   }

   if (errflg > 0 || file_flg == 0) {
      print_usage();
      exit(2);
   }

   serversock = -1;
   clientsock = -1;

   if (daemon_flg)
   {
      daemonize();
   }
   else
   {
      signal(SIGINT, ctrl_c_handler);
   }

   sprintf(str_buf, "%s (%s)\n", PROGNAME, PROGVER);
   puts(str_buf);

   sprintf(str_buf, "Listening to port %d.\n", port);
   log_message(str_buf);

   OLP_Start(file_name, &ierr);

   if(ierr != 1)
   {
      die("One-loop program could not be initialized.\n");
   }

   /* Create the TCP socket */
   if ((serversock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
      die("Failed to create socket");
   }
   /* Construct the server sockaddr_in structure */
   memset(&server, 0, sizeof(server));           /* Clear struct */
   server.sin_family = AF_INET;                  /* Internet/IP */
   server.sin_addr.s_addr = htonl(INADDR_ANY);   /* Incoming addr */
   server.sin_port = htons(port);                /* server port */


   /* Bind the server socket */
   if (bind(serversock, (struct sockaddr *) &server,
           sizeof(server)) < 0) {
      die("Failed to bind the server socket");
   }
   /* Listen on the server socket */
   if (listen(serversock, MAXPENDING) < 0) {
      die("Failed to listen on server socket");
   }
}
