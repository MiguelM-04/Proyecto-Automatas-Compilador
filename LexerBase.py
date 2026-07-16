from antlr4 import Lexer, Token
from antlr4.Token import CommonToken



class LexerBase(Lexer):

    def __init__(self, input, output=None):
        super().__init__(input, output)
        self.pila = [0]
        self.cola = []
        self.nivel_parentesis = 0
        self.tipo_anterior = None
        self.ya_acabo = False

    def nextToken(self):

        if self.cola:
            return self.cola.pop(0)

        tk = super().nextToken()

        if tk.type != Token.EOF:
            self.tipo_anterior = tk.type

        # dentro de parentesis, corchetes o llaves los saltos de linea no cuentan
        if tk.type in (self.PARENTESIS_IZQ, self.CORCHETE_IZQ, self.LLAVE_IZQ):
            self.nivel_parentesis += 1
        elif tk.type in (self.PARENTESIS_DER, self.CORCHETE_DER, self.LLAVE_DER):
            self.nivel_parentesis -= 1

        if tk.type == self.NEWLINE and self.nivel_parentesis > 0:
            return self.nextToken()

        if tk.type == self.NEWLINE and self.nivel_parentesis == 0:
            self.procesar_newline(tk)
            return self.cola.pop(0)

        if tk.type == Token.EOF and not self.ya_acabo:
            self.ya_acabo = True

            # si el archivo no termina en salto de linea, agregamos uno
            if self.tipo_anterior not in (self.NEWLINE, None):
                self.cola.append(self.hacer_token(tk, self.NEWLINE, ""))

            while len(self.pila) > 1:
                self.pila.pop()
                self.cola.append(self.hacer_token(tk, self.DEDENT, ""))

            self.cola.append(tk)
            return self.cola.pop(0)

        return tk

    def procesar_newline(self, tk):
        espacios = tk.text.split("\n")[-1].replace("\t", "    ")
        nivel_nuevo = len(espacios)

        self.cola.append(tk)

        if nivel_nuevo > self.pila[-1]:
            self.pila.append(nivel_nuevo)
            self.cola.append(self.hacer_token(tk, self.INDENT, ""))
        else:
            while nivel_nuevo < self.pila[-1]:
                self.pila.pop()
                self.cola.append(self.hacer_token(tk, self.DEDENT, ""))

    def hacer_token(self, referencia, tipo, texto):
        token = CommonToken(referencia.source, tipo, referencia.channel, referencia.start, referencia.stop)
        token.text = texto
        token.line = referencia.line
        token.column = referencia.column
        return token