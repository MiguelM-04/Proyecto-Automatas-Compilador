lexer grammar PythonLexer;

options {
    superClass = LexerBase;
}

// palabras reservadas
CLASS: 'class';
IS: 'is';
DEF: 'def';
RETURN: 'return';
IF: 'if';
ELIF: 'elif';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
IN: 'in';
IMPORT: 'import';
FROM: 'from';
AS: 'as';
PASS: 'pass';
BREAK: 'break';
CONTINUE: 'continue';
AND: 'and';
OR: 'or';
NOT: 'not';
TRUE: 'True';
FALSE: 'False';
NONE: 'None';

// identificadores
IDENTIFICADOR: [a-zA-Z_][a-zA-Z_0-9]*;

// literales numericos
NUMERO_FLOTANTE: [0-9]+ '.' [0-9]+;
NUMERO_ENTERO: [0-9]+;

// error lexico identificador no puede empezar con digito
IDENTIFICADOR_MAL_FORMADO: [0-9]+ [a-zA-Z_] [a-zA-Z_0-9]*;

// f-strings se tratan como una cadena completa, sin analizar lo de adentro de las llaves
CADENA_F: [fF] ('"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'');

// literales de cadena comilla simple o doble, una sola linea
CADENA: '"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'';

// error lexico comun: cadena que nunca cierra comillas
CADENA_SIN_CERRAR: '"' ~["\r\n]* | '\'' ~['\r\n]*;

// comentario de bloque y de linea, los dos se ignoran
COMENTARIO_BLOQUE: '"""' .*? '"""' -> skip;
COMENTARIO: '#' ~[\r\n]* -> skip;

// operadores (los de dos caracteres van primero para que no haya problema con los de uno)
POTENCIA: '**';
IGUAL_IGUAL: '==';
DISTINTO: '!=';
MENOR_IGUAL: '<=';
MAYOR_IGUAL: '>=';
MAS_IGUAL: '+=';
MENOS_IGUAL: '-=';
POR_IGUAL: '*=';
ENTRE_IGUAL: '/=';
DOBLE_DIAGONAL: '//';
MAS: '+';
MENOS: '-';
POR: '*';
DIAGONAL: '/';
MODULO: '%';
IGUAL: '=';
MENOR: '<';
MAYOR: '>';

// delimitadores
PARENTESIS_IZQ: '(';
PARENTESIS_DER: ')';
CORCHETE_IZQ: '[';
CORCHETE_DER: ']';
LLAVE_IZQ: '{';
LLAVE_DER: '}';
DOS_PUNTOS: ':';
COMA: ',';
PUNTO: '.';
PUNTO_COMA: ';';

// LexerBase decide si mete INDENT/DEDENT
NEWLINE: ('\r'? '\n' [ \t]*)+;

// no salen de ninguna regla, los mete LexerBase directo
INDENT: '\u0002';
DEDENT: '\u0003';

// espacios dentro de la misma linea, no al inicio
WS: [ \t]+ -> skip;

// cualquier cosa que no se reconozca se marca error lexico
ERROR_LEXICO: . ;
