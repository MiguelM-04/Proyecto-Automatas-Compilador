from antlr4 import ParseTreeWalker

from PythonParserListener import PythonParserListener

funciones_base = {
    "print", "len", "range", "str", "int", "float", "input",
    "type", "sum", "min", "max", "sorted", "list", "dict",
    "set", "tuple", "abs", "round", "__name__"
}

class ListenerSemantico(PythonParserListener):

    def __init__(self):
        self.declaradas = set(funciones_base)
        self.errores = []
        self.hay_import_estrella = False

    def enterSentencia_import(self, ctx):
        if ctx.POR() is not None:
            self.hay_import_estrella = True

    def enterModulo(self, ctx):
        identificadores = ctx.IDENTIFICADOR()
        if ctx.AS():
            self.declaradas.add(identificadores[-1].getText())
        else:
            self.declaradas.add(identificadores[0].getText())

    def enterImportado(self, ctx):
        identificadores = ctx.IDENTIFICADOR()
        if ctx.AS():
            self.declaradas.add(identificadores[-1].getText())
        else:
            self.declaradas.add(identificadores[0].getText())

    def enterDefinicion_clase(self, ctx):
        self.declaradas.add(ctx.IDENTIFICADOR(0).getText())

    def enterDefinicion_funcion(self, ctx):
        self.declaradas.add(ctx.IDENTIFICADOR().getText())
        if ctx.parametros():
            for parametro in ctx.parametros().IDENTIFICADOR():
                self.declaradas.add(parametro.getText())

    def enterSentencia_for(self, ctx):
        self.declaradas.add(ctx.IDENTIFICADOR().getText())

    def enterSentencia_expresion(self, ctx):
        if ctx.operador_asignacion() is not None:
            for prueba in ctx.lista_pruebas(0).prueba():
                nombre = prueba.getText()
                if nombre.isidentifier():
                    self.declaradas.add(nombre)

    def exitAtomo(self, ctx):
        if self.hay_import_estrella:
            return
        if ctx.IDENTIFICADOR() is not None:
            nombre = ctx.IDENTIFICADOR().getText()
            if nombre not in self.declaradas:
                self.errores.append({
                    "linea": ctx.start.line,
                    "columna": ctx.start.column,
                    "mensaje": f"la variable '{nombre}' se usa pero nunca fue declarada"
                })

    def exitTermino(self, ctx):
        hijos = list(ctx.children)
        for i, hijo in enumerate(hijos):
            if hijo.getText() in ("/", "//", "%") and i + 1 < len(hijos):
                divisor = hijos[i + 1].getText()
                if divisor in ("0", "0.0"):
                    self.errores.append({
                        "linea": ctx.start.line,
                        "columna": ctx.start.column,
                        "mensaje": "division entre cero"
                    })

class AnalizadorSemantico:

    def __init__(self):
        self.listener = None

    def analizar(self, arbol, parser):
        self.listener = ListenerSemantico()
        caminante = ParseTreeWalker()
        caminante.walk(self.listener, arbol)

    def obtener_errores(self):
        if self.listener is None:
            return []
        return self.listener.errores