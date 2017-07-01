#!/bin/bash

if [ $# -eq 0 ]
	then
		echo "Please Enter name of the Source file"
		exit
fi

echo "Lexical Analysis"
echo "---------------------------------------------------------------------------------------------------------------"
python remove_comments.py $1


sleep 1
echo "----------------------------------------------------------------------------------------------------------------"
echo "Symbol table"
python ConstructST.py $1
echo ""


sleep 2
echo "---------------------------------------------------------------------------------------------------------------"
echo "Syntax Analysis"
echo "Abstract Syntax Tree"
python GenerateToken.py $1


echo ""
sleep 2
echo "---------------------------------------------------------------------------------------------------------------"
echo "Three Address Code"
yacc -d yacc.y
lex lex.l
gcc -w y.tab.c lex.yy.c -std=c99 -o TAC
./TAC < $1

rm *.pyc
rm lex.yy.c
rm y.tab.*
rm TAC
rm parse*


