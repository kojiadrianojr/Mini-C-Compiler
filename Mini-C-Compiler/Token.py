import ply.lex as lex

reserved = {
   'while': 'WHILE'

}
keywords = {'true':'TRUE','false':'FALSE','return':'RETURN', 'if':'IF', 'then':'THEN','else':'ELSE','int':'INT','float':'FLOAT'}
# List of token names.   This is always required
'''
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)
'''
#literals = [ '{', '}' ]
literals=['(',')','=',';','}','{','+','-']
#literals="()=;}{+-/" #both are valid

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
    #we gotta make regex whixh accepts floats too!Did that :)
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

from ply.lex import lexer
def generateToken(data):
    tokens = []
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        tokens.append(tok)
    return tokens
