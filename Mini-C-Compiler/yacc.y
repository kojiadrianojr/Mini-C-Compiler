%{
	#include <stdio.h>
	#include<string.h>
	#include<stdio.h>
	typedef struct quadraple {
		char op[20];
		char arg1[20];
		char arg2[20];
		char res[20];
	} quad;
	quad qd[100];
	int stack[100];
	int top;
	int ind=0,tind=0,StNo,Ind,tmpind;
%}
%union
{
char var[10];
}
%token <var> NUM ID RELOP
%token IF ELSE TYPE MAIN
%type <var> E A C IFST ELSEST
%left '-' '+'
%left '*' '/'
%%
P	:	MAIN '{' D S '}';
D	:	TYPE V D
		|
		;
V	:	X M;
M	:	',' X M 
		|';'
		;
X	:	ID {}
		|ID '=' E {strcpy(qd[ind].op,"");
					strcpy(qd[ind].arg1,$3);
					strcpy(qd[ind].arg2,"");
					strcpy(qd[ind].res,$1);
					strcpy($3,qd[ind++].res);
		}
		;
S	: 	IFST{ Ind=pop(); sprintf(qd[Ind].res,"%d",ind);	Ind=pop(); sprintf(qd[Ind].res,"%d",ind); }
		|
		IFST ELSEST
		;
IFST: 	IF '(' C ')' {
			char *xyz=malloc(50);
			sprintf(xyz,"if t%d==FALSE",tind-1);
			strcpy(qd[ind].op,xyz);
			strcpy(qd[ind].arg1,"");
			strcpy(qd[ind].arg2,"GOTO");
			strcpy(qd[ind].res,"-1");
			push(ind);
			ind++;
		}
		CODE {
			strcpy(qd[ind].op,"");
			strcpy(qd[ind].arg1,"");
			strcpy(qd[ind].arg2,"GOTO");
			strcpy(qd[ind].res,"-1");
			push(ind);
			ind++;
		}
		;
ELSEST: ELSE{
			tmpind=pop();
			Ind=pop();
			push(tmpind);
			sprintf(qd[Ind].res,"%d",ind);
		}
		CODE{
			Ind=pop();
			sprintf(qd[Ind].res,"%d",ind);
		}
		;
C: 	ID RELOP ID {add_record($2,$1,$3,$$); StNo=ind-1; }
	|
	ID RELOP NUM {add_record($2,$1,$3,$$); StNo=ind-1; }
	|
	NUM RELOP NUM {add_record($2,$1,$3,$$);	StNo=ind-1; }
	|
	ID
	|
	NUM
	;
CODE: '{' ST '}'
		;
ST: 	A ';'
		|
		S
		;
A	: 	ID '=' E{  
					strcpy(qd[ind].op,"");
					strcpy(qd[ind].arg1,$3);
					strcpy(qd[ind].arg2,"");
					strcpy(qd[ind].res,$1);
					strcpy($$,qd[ind++].res);
		}
		;
E	: 	E '+' E {add_record("+",$1,$3,$$);}
		|
		E '-' E {add_record("-",$1,$3,$$);}
		|
		E '*' E {add_record("*",$1,$3,$$);}
		|
		E '/' E {add_record("/",$1,$3,$$);}
		|
		ID
		|
		NUM
		;
%%

void push(int e){ top++; stack[top] = e; }
int pop(){ int e = stack[top--]; return e; }
void add_record(char op[20],char arg1[20],char arg2[20],char res[20]){
	strcpy(qd[ind].op,op);
	strcpy(qd[ind].arg1,arg1);
	strcpy(qd[ind].arg2,arg2);
	sprintf(qd[ind].res,"t%d",tind++);
	strcpy(res,qd[ind++].res);
}
int yyerror(){ printf("Error"); return 1; }    
int yywrap(){ return 1; }
int main(){
	yyparse();
	printf("      THREE ADDRESS CODE     \n");
	for(int i=0;i<ind;i++)
	{
		if(strcmp(qd[i].arg2,"GOTO")==0)
		{
				printf("%10d  %s %s %s\n",i,qd[i].op,qd[i].arg2,qd[i].res);
		}
		else
		printf("%10d%5s = %s %s %s\n",i,qd[i].res,qd[i].arg1,qd[i].op,qd[i].arg2);
	}
	return 0;
}
