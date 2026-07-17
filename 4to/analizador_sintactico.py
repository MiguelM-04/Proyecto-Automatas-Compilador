# clase utilitaria para la fase sintactica, recibe los tokens que ya saco
# el AnalizadorLexico y valida que sigan la gramatica de Python

from antlr4 import CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from PythonParser import PythonParser


# Clase para guardar errores sintacticos (mismo patron que ErroresLexicos)
class ErroresSintacticos(ErrorListener):

    def __init__(self):
        self.lista = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.lista.append([line, column, msg])


class AnalizadorSintactico:

    def __init__(self):
        self.parser = None
        self.arbol = None
        self.errores = ErroresSintacticos()

    # recibe el CommonTokenStream que ya lleno el AnalizadorLexico
    def analizar(self, tokens):
        self.errores.lista = []

        # regresamos el flujo al inicio, el lexico ya lo habia recorrido completo
        tokens.reset()

        self.parser = PythonParser(tokens)
        self.parser.removeErrorListeners()
        self.parser.addErrorListener(self.errores)

        # "programa" es la regla inicial de la gramatica (equivalente a "root")
        self.arbol = self.parser.programa()

    def obtener_errores(self):
        lista_errores = []
        for error in self.errores.lista:
            lista_errores.append({
                "linea": error[0],
                "columna": error[1],
                "mensaje": error[2]
            })
        return lista_errores

    def es_valido(self):
        return len(self.errores.lista) == 0

    def obtener_arbol_texto(self):
        if self.arbol is None:
            return ""
        return self.arbol.toStringTree(recog=self.parser)
