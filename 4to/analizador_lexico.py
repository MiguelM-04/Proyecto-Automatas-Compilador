# Importamos las clases principales de ANTLR
from antlr4 import *

# Importamos ErrorListener para capturar errores lexicos
from antlr4.error.ErrorListener import ErrorListener

# Importamos el lexer generado por ANTLR
from PythonLexer import PythonLexer


# Clase para guardar errores lexicos
class ErroresLexicos(ErrorListener):

    # Constructor de la clase
    def __init__(self):
        # Creamos una lista vacia para guardar errores
        self.lista = []

    # Metodo que ANTLR ejecuta cuando encuentra un error
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Guardamos el error en la lista
        self.lista.append([line, column, msg])


# Clase principal del analizador lexico
class AnalizadorLexico:

    # Constructor de la clase
    def __init__(self):
        # Variable para guardar el lexer
        self.lexer = None
        # Variable para guardar los tokens
        self.tokens = None
        # Creamos el manejador de errores lexicos
        self.errores = ErroresLexicos()

    # Metodo para analizar el codigo
    def analizar(self, codigo):
        # MUY IMPORTANTE: Limpiamos los errores de lecturas anteriores
        self.errores.lista = []

        # Convertimos el texto en entrada para ANTLR
        entrada = InputStream(codigo)

        # Creamos el lexer usando la entrada
        self.lexer = PythonLexer(entrada)

        # Quitamos los errores normales de ANTLR
        self.lexer.removeErrorListeners()

        # Agregamos nuestro propio manejador de errores
        self.lexer.addErrorListener(self.errores)

        # Creamos el flujo de tokens
        self.tokens = CommonTokenStream(self.lexer)

        # Leemos todos los tokens
        self.tokens.fill()

        # los tokens de error lexico propios
        for token in self.tokens.tokens:
            if token.type in (self.lexer.ERROR_LEXICO, self.lexer.IDENTIFICADOR_MAL_FORMADO, self.lexer.CADENA_SIN_CERRAR):
                self.errores.lista.append([token.line, token.column, f"token invalido: '{token.text}'"])

    def obtener_tokens(self):
        lista_tokens = []
        if self.tokens is None:
            return lista_tokens

        # Recorremos todos los tokens encontrados
        for token in self.tokens.tokens:
            # Saltamos el token final EOF
            if token.type == Token.EOF:
                continue

            # Obtenemos el nombre del token
            nombre = self.lexer.symbolicNames[token.type]

            # Lo guardamos como diccionario para la tabla de Streamlit
            lista_tokens.append({
                "lexema": token.text,
                "token": nombre,
                "tipo": token.type,
                "linea": token.line,
                "columna": token.column
            })

        return lista_tokens

    def obtener_errores(self):
        lista_errores = []
        # Recorremos la lista de errores guardada
        for error in self.errores.lista:
            # Lo guardamos como diccionario para la tabla de Streamlit
            lista_errores.append({
                "linea": error[0],
                "columna": error[1],
                "mensaje": error[2]
            })

        return lista_errores

    # Metodo para imprimir los tokens
    def imprimir_tokens(self):
        # Imprimimos titulo
        print("\nTOKENS")
        print("-" * 70)
        # Imprimimos encabezados de la tabla
        print(f"{'LEXEMA':<15} {'TOKEN':<15} {'TIPO':<6} {'LINEA':<6} {'COLUMNA':<8}")
        print("-" * 70)

        # Recorremos todos los tokens encontrados
        for token in self.tokens.tokens:
            # Saltamos el token final EOF
            if token.type == Token.EOF:
                continue

            # Obtenemos el nombre del token
            nombre = self.lexer.symbolicNames[token.type]

            # Imprimimos los datos del token
            print(f"{token.text:<15} {nombre:<15} {token.type:<6} {token.line:<6} {token.column:<8}")

    # Metodo para imprimir errores lexicos
    def imprimir_errores(self):
        # Imprimimos titulo
        print("\nERRORES LEXICOS")
        print("-" * 40)

        # Validamos si no hay errores
        if len(self.errores.lista) == 0:
            print("No hay errores lexicos")
        else:
            # Recorremos la lista de errores
            for error in self.errores.lista:
                print(f"Linea {error[0]}, columna {error[1]}: {error[2]}")
