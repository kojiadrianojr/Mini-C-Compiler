%{
	#include"y.tab.h"
	#include<stdio.h>
	#include<string.h>
	int LineNo=1;
%}
identifier [a-zA-Z][_a-zA-Z0-9]*
number [0-9]+|([0-9]*\.[0-9]+)
%%

if return IF;
else return ELSE;
main\(\)  return MAIN;
(int|float|char) return TYPE;
{identifier} {strcpy(yylval.var,yytext); return ID;}
{number} {strcpy(yylval.var,yytext); return NUM;}
\<|\>|\>=|\<=|== { strcpy(yylval.var,yytext); return RELOP;}
[ \t] ;
\n LineNo++;
. return yytext[0];
%%
