%{
#include <string.h>
#include <sys/socket.h>
#include "olp_parser.h"
#include "olp_daemon.h"

void reset_scanner(void)
{
    ; YY_FLUSH_BUFFER;
}

#define YY_INPUT(buf,result,max_size) \
{ \
    if (bye_requested || shutdown_requested) \
       result = YY_NULL; \
    else if ((result = recv(clientsock, buf, max_size, 0)) < 0) { \
      die("Failed to receive bytes from client"); \
    } \
}

%}

%option noyywrap

%%

[ \t\f]+                              { /* skip */ }
[\r]?[\n]                             { return EOL; }
=                                     { return EQUALS; }
,                                     { return COMMA; }

WHO                                   { return WHO; }
SHUTDOWN                              { return SHUTDOWN; }
EVENT                                 { return EVENT; }
SUBPROCESS                            { return SUBPROCESS; }
PARAMETER                             { return PARAMETER; }
OPTION                                { return OPTION; }
MOMENTUM                              { return MOMENTUM; }
RESTART                               { return RESTART; }
BYE                                   { return BYE; }
[-+]?[0-9]+                           {
   yylval.integer_argument = atoi(yytext);
   return INTEGER;
}
[-+]?[0-9]*\.[0-9]*([eE][-+]?[0-9]+)? {
   yylval.double_argument = atof(yytext);
   return FLOAT;
}
[A-Za-z][A-Za-z0-9_]*                 {
   yylval.string_argument = strdup(yytext);
   return NAME;
}

.                                     { return ERROR; }
