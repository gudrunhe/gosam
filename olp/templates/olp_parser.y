/* vim: ts=3:sw=3:expandtab
 */
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include "olp_daemon.h"
#include "olp.h"

static char string_buffer[257];
static double amp[4];
static int  flag, idx;

extern void reset_scanner(void);

void yyerror(const char *str)
{
   send_message(400, str);
}
 
%}

%token WHO SHUTDOWN EVENT SUBPROCESS PARAMETER OPTION MOMENTUM BYE RESTART
%token EQUALS COMMA EOL ERROR
%token <integer_argument> INTEGER
%token <double_argument> FLOAT
%token <string_argument> NAME

%union {
   int      integer_argument;
   double   double_argument;
   char*    string_argument;
};

%%

commands: /* empty */
   | commands command
   ;

command:
     command_bye
   | command_who
   | command_shutdown
   | command_event
   | command_subprocess
   | command_parameter
   | command_option
   | command_momentum
   | command_restart
   | error EOL
     {
      yyerrok;
     }
   ;

command_bye:
   BYE EOL
   {
      send_message(200, "OK closing connection");
      bye_requested = 1;
   }
   ;

command_who:
   WHO EOL
   {
      sprintf(string_buffer, "%s/%s", PROGNAME, PROGVER);
      send_message(200, string_buffer);
   }
   ;

command_shutdown:
   SHUTDOWN EOL
   {
      if(shutdown_allowed) {
         send_message(200, "OK quitting server");
         shutdown_requested = 1;
      }
      else
      {
         send_message(406, "method not allowed");
      }
   }
   ;

command_restart:
   RESTART EOL
   {
      if(restart_allowed) {
#ifdef GOLEMEXTENSIONS
         OLP_Finalize();
#endif
         OLP_Start(file_name, &flag);
         if(flag == 1)
            send_message(200, "OK");
         else
            send_message(500, "could not initialize OLP");
      }
      else
      {
         send_message(406, "method not allowed");
      }
   }

command_event:
   EVENT INTEGER INTEGER EOL
   {
      evt.num_legs = $2;
      evt.num_parameter = $3;

      flag = 0;

      if((evt.num_legs < 0) || (evt.num_legs > MAX_LEGS))
      {
         flag = 1;
         evt.num_legs = 0;
      }
      if((evt.num_parameter < 0) || (evt.num_parameter > MAX_PARAMETER))
      {
         flag = 1;
         evt.num_parameter = 0;
      }

      if(flag)
         send_message(406, "argument out of bounds");
      else
         send_message(200, "OK");

      for(idx=0; idx < evt.num_legs; ++idx)
      {
         evt.momenta[idx*5+0] = 0.0;
         evt.momenta[idx*5+1] = 0.0;
         evt.momenta[idx*5+2] = 0.0;
         evt.momenta[idx*5+3] = 0.0;
         evt.momenta[idx*5+4] = 0.0;
      }
      for(idx=0; idx < evt.num_parameter; ++idx)
      {
         evt.parameter[idx] = 0.0;
      }
   }
   ;

command_subprocess:
   SUBPROCESS INTEGER FLOAT EOL
   {
      OLP_EvalSubProcess($2, evt.momenta, $3, evt.parameter, amp);
      sprintf(string_buffer, "%24.16e %24.16e %24.16e %24.16e",
         amp[0], amp[1], amp[2], amp[3]);
      send_message(200, string_buffer);
   }
   ;

command_parameter:
   PARAMETER INTEGER FLOAT EOL
   {
      if(($2 >= 0) && ($2 < evt.num_parameter))
      {
         evt.parameter[$2] = $3;
         send_message(200, "OK");
      }
      else
         send_message(406, "argument out of bounds");
   }
   ;

command_option:
   OPTION NAME EQUALS INTEGER EOL
   {
   #ifdef GOLEMEXTENSIONS
      sprintf(string_buffer, "%s=%d", $2, $4);
      OLP_Option(string_buffer, &flag); 
      if (flag)
         send_message(200, "OK");
      else
         send_message(400, "Could not set option");
   #else
      send_message(406, "method not allowed");
   #endif
      free($2);
   }
 | OPTION NAME EQUALS FLOAT EOL
   {
   #ifdef GOLEMEXTENSIONS
      sprintf(string_buffer, "%s=%24.16e", $2, $4);
      OLP_Option(string_buffer, &flag); 
      if (flag)
         send_message(200, "OK");
      else
         send_message(400, "Could not set option");
   #else
      send_message(406, "method not allowed");
   #endif
      free($2);
   }
 | OPTION NAME EQUALS FLOAT COMMA FLOAT EOL
   {
   #ifdef GOLEMEXTENSIONS
      sprintf(string_buffer, "%s=%24.16e, %24.16e", $2, $4, $6);
      OLP_Option(string_buffer, &flag); 
      if (flag)
         send_message(200, "OK");
      else
         send_message(400, "Could not set option");
   #else
      send_message(406, "method not allowed");
   #endif
      free($2);
   }
   ;

command_momentum:
   MOMENTUM INTEGER FLOAT FLOAT FLOAT FLOAT FLOAT EOL
   {
      if(($2 >= 0) && ($2 < evt.num_legs))
      {
         evt.momenta[5*$2+0] = $3;
         evt.momenta[5*$2+1] = $4;
         evt.momenta[5*$2+2] = $5;
         evt.momenta[5*$2+3] = $6;
         evt.momenta[5*$2+4] = $7;
         send_message(200, "OK");
      }
      else
         send_message(406, "argument out of bounds");
   }
   ;

%%

int main(int argc, char** argv)
{
   int keep_running = 1;
   int on = 1;
   char str_buf[64];

   startup(argc, argv);

   while (keep_running) {
      unsigned int clientlen = sizeof(client);

      /* Wait for client connection */
      if ((clientsock = accept(serversock, (struct sockaddr *) &client,
                &clientlen)) < 0) {
         die("Failed to accept client connection");
      }


      #ifdef SO_NOSIGPIPE
      setsockopt(clientsock, SOL_SOCKET, SO_NOSIGPIPE, (void *)&on, sizeof(on));
      #endif

      sprintf(str_buf, "Started session with %s\n", inet_ntoa(client.sin_addr));
      log_message(str_buf);

      bye_requested = 0;
      shutdown_requested = 0;

      evt.num_legs = 0;
      evt.num_parameter = 0;

      reset_scanner();
      yyparse();

      keep_running = ! (shutdown_requested && shutdown_allowed);

      close(clientsock);
      clientsock = -1;
      log_message("Finished session\n");
   }

   cleanup();
   return 0;
} 

