import sys
import Node
import ply.lex as lex
import ply.yacc as yacc

reserved = {
   'while': 'WHILE'

}
keywords = {'true':'TRUE','false':'FALSE','return':'RETURN', 'if':'IF', 'then':'THEN','else':'ELSE','int':'INT','float':'FLOAT'}
literals=['(',')','=',';','}','{','+','-']

lit=['LBRACE','RBRACE']
comparators=['LESSTHAN','GREATERTHAN','EQUALS','NOTEQUALS','LESSTHANOREQUAL','GREATERTHANOREQUAL']
unary=['DECREMENT','INCREMENT']


tokens = ['UNARY','COMPARATORS','LBRACE','RBRACE','AND','OR','RSQUARE','LSQUARE','LITERALSTRING','LPAREN','RPAREN','NUMBER','PLUS',
		  'MINUS','TIMES','DIVIDE','SEMICOLON','ID','ASSIGNMENT','HASH','DOT'] + list(reserved.values()) + list(keywords.values())

# Regular expression rules for simple tokens
t_PLUS= r'\+'
t_MINUS= r'-'
t_TIMES= r'\*'
t_DIVIDE= r'/'
t_LPAREN= r'\('
t_RPAREN= r'\)'
t_SEMICOLON=r';'
t_ASSIGNMENT=r'='
#t_DECREMENT=r'--'
#t_INCREMENT=r'\+\+'
t_LBRACE=r'\{' #remove names from tokens when this is commented
t_RBRACE=r'\}' #add when uncommented #better use another list like we have used lit[]
t_LITERALSTRING=r'\".*\"'
#t_LESSTHAN=r'<'
#t_GREATERTHAN=r'>'
t_AND=r'&&'
t_OR=r'\|\|'
#t_EQUALS=r'=='
#t_NOTEQUALS=r'!='
t_RSQUARE=r'\]'
t_LSQUARE=r'\['
t_HASH=r'\#'
t_DOT=r'\.'
# A regular expression rule with some action code

precedence = (
	('left','PLUS','MINUS'),
	('left','TIMES','DIVIDE'),
	)


def t_UNARY(t):
	r'( \+\+ | -- )'
	t.type='UNARY'    #this return type should match names from tokens[] list!important
	return t

def t_COMPARATORS(t):
	r'( < | > | >= | <= | == | != )'
	t.type = 'COMPARATORS'
	return t


def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	t.type = keywords.get(t.value,'ID')
	return t


def t_NUMBER(t):
	r'(\d+.\d+)|(\d+)'
	if '.' in t.value :#check for float then set value as float else set as int
		t.value = float(t.value)
	else :
		t.value= int(t.value)
	return t

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Build the lexer
#lexer = lex.lex()

lex.lex()

# Test it out
'''
3 + 4 * 10
  + -20 *2 if==(=)else{--};
'''

# Give the lexer some input
#lexer.input(data)

'''
def generateToken(data):
	tokens = []
	lexer.input(data)
	while True:
		tok = lexer.token()
		if not tok:
			break      # No more input
		#print(tok,"\t",tok.value,"\t",tok.type)
		tokens.append(tok)
		#print(tok)
	return tokens
'''
#try with undeclared variables and see the o/p!
'''
f1 = open('in1.c', 'r+');
data1=f1.read()
'''

names={ }
types={ }

def p_P(p):
	'P : K S'
	print("-------------------------------------\nVALID")
	# just for checking the values of variables at the end of the program!
	print("-------------------------------------\nNames:\nvariable  value")
	for keys in names:
		print(keys,"\t\t  ", names[keys])
	print("-------------------------------------\nTypes:\nVariable  type")
	for keys in types:
		print(keys,"\t\t  ", types[keys])

def p_K(p):
	'''K : INT
		|'''
	#1st line: for int main()
	#2nd line: for just main(), no int specified


def p_S_main(p):
	'''S : ID LPAREN RPAREN LBRACE  T RBRACE'''


def p_T_assig(p):
	'''T : TYPE_NAME_STORE SEMICOLON T'''
	# print(p[0],p[1],p[2],p[3],p[4]) #o/p: None int a = 10
	# names[p[2]] = p[4]
	# types[p[2]] = p[1]

def p_STORE_int(p):
	'''TYPE_NAME_STORE : INT ID ASSIGNMENT E1'''
	if type(p[4][0]) == int:
		names[p[2][0]] = p[4][0]
		types[p[2][0]] = int
	else:
		print("SEMANTIC ERROR:LHS type:'int' RHS type:",type(p[4]))
		raise SyntaxError

def p_STORE_float(p):
	'''TYPE_NAME_STORE : FLOAT ID ASSIGNMENT E1'''
	if type(p[4][0]) == float:
		names[p[2][0]] = p[4][0]
		types[p[2][0]] = float
	else:
		print("SEMANTIC ERROR:LHS type:'float' RHS type:",type(p[4]))
		raise SyntaxError

def p_E1_Number(p):
	'''E1 : NUMBER'''
	p[0] = list()
	p[0].append(p[1])
	p[0].append(Node.Node('Num',[],p[1]))
	#print('E1',p[1]) #10

def p_E1_ID(p):
	'''E1 : ID'''
	# print(p[1]) #a b u k a
	if p[1][0] in names :
		pass
	else :
		print(p[1], "Syntax error, variable '",p[1],"' not declared", p.lineno(1))


def p_T_if(p):
	'''T : F'''


def p_F(p):
	'''F : IF LPAREN B RPAREN LBRACE F RBRACE ELSE LBRACE F RBRACE
		| IF LPAREN B RPAREN LBRACE F RBRACE
		| AssignExpr'''


def p_AssignExpr(p):
	'AssignExpr : ID ASSIGNMENT E SEMICOLON'
	# print(p[0],p[1],p[2],p[3])
	if types[p[1][0]] == type(p[3][0]) :
		names[p[1][0]] = p[3][0] #store value of a in p[0] only if a is declared
		p[0] = list()
		p[0].append(p[3][0])
		p[1] = [ p[1] ] #list which has p[1]
		p[1].append(Node.Node('ID',[],p[1][0]))
		p[0].append(Node.Node('Assign',[p[1],p[3]],p[2]))
		#print('Assign',p[1],p[3])
		print(p[0][1].disp())
	#print('Assign',p[0][1].leaf,p[0][1].children)
		#print("names[p[0]]",p[0])
	else:
		print("SEMANTIC ERROR at line ",p.lineno(1),", The type of LHS i.e ",p[1],"'s type:",types[p[1]]," and that of RHS whose  type is ",type(p[3][0]),"are not compatible")
		raise SyntaxError


def p_B_or(p):
	'''B : E OR E'''
	p[0] = list()
	p[0].append(p[1][0] or p[3][0])
	p[0].append(Node.Node('Logop',[p[1],p[3]],p[2]))
	print(p[0][1].disp())

def p_B_and(p):
	'''B : E AND E'''
	p[0] = list()
	p[0].append(p[1][0] and p[3][0])
	p[0].append(Node.Node('Logop',[p[1],p[3]],p[2]))
	print(p[0][1].disp())

def p_B_comparators(p):
	'''B : E COMPARATORS E'''
	if(p[2] == '<' ):
		p[0] = list()
		p[0].append(p[1][0] < p[3][0])
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	elif(p[2] == '>' ):
		p[0] = list()
		p[0].append(p[1][0] > p[3][0])
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	elif(p[2] == '<=' ):
		p[0] = list()
		p[0].append(p[1][0] <= p[3][0])
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	elif(p[2] == '>=' ):
		p[0] = list()
		p[0].append(p[1][0] >= p[3][0])
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	elif(p[2] == '==' ):
		p[0] = list()
		p[0].append(p[1][0] == p[3][0])
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	elif(p[2] == '!=' ):
		p[0] = list()
		p[0].append(int(p[1][0]) != int(p[3][0]))
		p[0].append(Node.Node('Relop',[p[1],p[3]],p[2]))
	print(p[0][1].disp())

def p_B_number(p):
	'''B : NUMBER'''
	p[0] = p[1]

def p_B_id(p):
	'''B : ID'''
	p[0] = p[1]
	#print('B_id',p[1])
	#p[0] = p[1]

def p_B_true(p):
	'''B : TRUE'''
	p[0] = list()
	p[0].append(True)
	p[0].append(Node.Node('Bool',[],True))
	#print(p[0][1].disp())

def p_B_false(p):
	'''B : FALSE'''
	p[0] = list()
	p[0].append(False)
	p[0].append(Node.Node('Bool',[],False))
	#print(p[0][1].disp())

def p_E_PLUS(p):
	'''E : E PLUS E'''
	p[0] = list()
	p[0].append((p[1][0] + p[3][0]))
	p[0].append(Node.Node('Binop_plus',[p[1],p[3]],p[2]))
	print(p[0][1].disp())
	#print("parsed E in PLUS:",p[0],p[1],p[2],p[3])

def p_E_MINUS(p):
	'''E : E MINUS E'''
	p[0] = list()
	p[0].append(p[1][0] - p[3][0])
	p[0].append(Node.Node('Binop_minus',[p[1],p[3]],p[2]))
	print(p[0][1].disp())
	# print("parsed E in MINUS:",p[1],p[2],p[3])


def p_E_NUMBER(p):
	'''E : NUMBER'''
	p[0] = list()
	p[0].append(p[1])
	p[0].append(Node.Node('Num',[],p[1]))
	#print(p[0][1].disp())
	# print("parsed E:",p[1])

def p_E_ID(p):
	'''E : ID'''
	#print(p[1]) #o/p: a ,ie variable names
	# print("a type:",types[p[1]])
	# print("result type:",type(names[p[1]]))
	# print("p[1]:",names[p[1]])
	if p[1] in names :
		p[0] = list()
		p[0].append(names[p[1]])
		p[0].append(Node.Node('ID',[],p[1]))
		#print(p[0][1].disp())
	else:
		print(p[1]," is not defined, at line", p.lineno(1))
		raise SyntaxError
	#print("parsed E:",p[1],len(p))



def p_error(p):
	print("Syntax error in input!")

yacc.yacc()

#while True:
'''try:
	   s = data
   except EOFError:
	   break
   if not s: continue
'''
#print(tokens)
#s=input()
#yacc.parse("if(a){c=a+b;}else{if(c<d){c=0;}}")
if len(sys.argv) < 2:
	print("Please Enter the name of the Source file")
	exit(0)

'''f1 = open('in1.c', 'r+');
data1=f1.read()
yacc.parse(data1)'''
#print(result)

with open(sys.argv[1], 'r+') as f:
	yacc.parse(f.read())