parser grammar PythonParser;

options {
    tokenVocab = PythonLexer;
}

programa: sentencia* EOF;

sentencia: NEWLINE* sentencia_simple NEWLINE | NEWLINE* sentencia_compuesta;

sentencia_simple: sentencia_pequenia (PUNTO_COMA sentencia_pequenia)* PUNTO_COMA?;

sentencia_pequenia
    : sentencia_expresion
    | PASS
    | BREAK
    | CONTINUE
    | sentencia_return
    | sentencia_import
    ;

sentencia_expresion: lista_pruebas (operador_asignacion lista_pruebas)?;

operador_asignacion: IGUAL | MAS_IGUAL | MENOS_IGUAL | POR_IGUAL | ENTRE_IGUAL;

sentencia_return: RETURN lista_pruebas?;

sentencia_import
    : IMPORT modulo (COMA modulo)*
    | FROM IDENTIFICADOR (PUNTO IDENTIFICADOR)* IMPORT (POR | importado (COMA importado)*)
    ;

modulo: IDENTIFICADOR (PUNTO IDENTIFICADOR)* (AS IDENTIFICADOR)?;
importado: IDENTIFICADOR (AS IDENTIFICADOR)?;

sentencia_compuesta: sentencia_if | sentencia_while | sentencia_for | definicion_funcion | definicion_clase;

definicion_clase:
    CLASS IDENTIFICADOR (PARENTESIS_IZQ IDENTIFICADOR PARENTESIS_DER)? DOS_PUNTOS bloque;

sentencia_if:
    IF prueba DOS_PUNTOS bloque
    (ELIF prueba DOS_PUNTOS bloque)*
    (ELSE DOS_PUNTOS bloque)?;

sentencia_while: WHILE prueba DOS_PUNTOS bloque;

sentencia_for: FOR IDENTIFICADOR IN lista_pruebas DOS_PUNTOS bloque;

definicion_funcion:
    DEF IDENTIFICADOR PARENTESIS_IZQ parametros? PARENTESIS_DER DOS_PUNTOS bloque;

parametros: IDENTIFICADOR (COMA IDENTIFICADOR)*;

// un bloque puede ser una sola linea o con indentacion real
bloque: sentencia_simple NEWLINE | NEWLINE INDENT sentencia+ DEDENT;

prueba: prueba_or;
prueba_or: prueba_and (OR prueba_and)*;
prueba_and: prueba_not (AND prueba_not)*;
prueba_not: NOT prueba_not | comparacion;

comparacion: expr_aritmetica (comparador expr_aritmetica)*;

// aparte de == < >, python usa "in" y "is" para comparar
comparador
    : operador_comparacion
    | IN
    | NOT IN
    | IS
    | IS NOT
    ;

operador_comparacion: IGUAL_IGUAL | DISTINTO | MENOR | MAYOR | MENOR_IGUAL | MAYOR_IGUAL;

expr_aritmetica: termino ((MAS | MENOS) termino)*;
termino: factor ((POR | DIAGONAL | DOBLE_DIAGONAL | MODULO) factor)*;
factor: (MAS | MENOS) factor | potencia;
potencia: atomo_con_sufijos (POTENCIA factor)?;
atomo_con_sufijos: atomo sufijo*;

sufijo
    : PARENTESIS_IZQ argumentos? PARENTESIS_DER
    | CORCHETE_IZQ prueba CORCHETE_DER
    | PUNTO IDENTIFICADOR
    ;

// argumento puede ser normal o con nombre
argumentos: argumento (COMA argumento)*;
argumento: (IDENTIFICADOR IGUAL)? prueba;

atomo
    : IDENTIFICADOR
    | NUMERO_ENTERO
    | NUMERO_FLOTANTE
    | CADENA
    | CADENA_F
    | TRUE
    | FALSE
    | NONE
    | PARENTESIS_IZQ lista_pruebas PARENTESIS_DER
    | CORCHETE_IZQ lista_pruebas? CORCHETE_DER
    | LLAVE_IZQ (par_clave_valor (COMA par_clave_valor)*)? LLAVE_DER  // diccionario {clave: valor}
    ;

par_clave_valor: prueba DOS_PUNTOS prueba;

lista_pruebas: prueba (COMA prueba)*;