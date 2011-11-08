#ifndef __OLP_DAEMON_H__
#define __OLP_DAEMON_H__

#define GOLEMEXTENSIONS 1

#define PROGNAME "olp-daemon"
#define PROGVER  "1.0"

#define MAX_LEGS      20
#define MAX_PARAMETER 50

#define MAXPENDING 5    /* Max connection requests */

#define DEFAULT_PORT 7711
#define DEFAULT_ALLOW_SHUTDOWN 1
#define DEFAULT_ALLOW_RESTART 1

#define DAEMON_RUNDIR "/tmp"

typedef struct {
   int num_legs;
   int num_parameter;

   double parameter[MAX_PARAMETER];
   double momenta[5*MAX_LEGS];
} event_type;

extern event_type evt;
extern int serversock, clientsock;
extern struct sockaddr_in server, client;
extern int bye_requested, shutdown_requested;
extern int shutdown_allowed, restart_allowed;
extern char* file_name;

void send_message(int response_code, const char* message);
void die(char *mess);

#endif
