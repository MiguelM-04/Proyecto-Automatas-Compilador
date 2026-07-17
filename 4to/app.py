import streamlit as st
from archivo import Archivo
from analizador_lexico import AnalizadorLexico
from analizador_sintactico import AnalizadorSintactico
from analizador_semantico import AnalizadorSemantico


class App:

    def __init__(self):
        st.set_page_config(page_title="Analizador Python", layout="wide")
        self.lexico = AnalizadorLexico()
        self.sintactico = AnalizadorSintactico()
        self.semantico = AnalizadorSemantico()

    def ejecutar(self):
        st.title("Analizador de Python con ANTLR y Streamlit")
        st.write("Sube un archivo `.py` para ver tokens, errores lexicos, sintacticos y semanticos.")

        # Configuramos el cargador para que solo acepte extension .py
        archivo_subido = st.file_uploader("Selecciona tu archivo", type=["py"])

        if archivo_subido is None:
            st.info("Primero sube un archivo .py")
            return

        archivo = Archivo(archivo_subido)

        if not archivo.es_el_tipo_correcto():
            st.error("El archivo debe ser .py")
            return

        codigo = archivo.leer()
        info = archivo.obtener_info()

        if not archivo.contenido_parece_python(codigo):
            st.warning("El contenido no tiene pinta de ser codigo Python (muchas llaves o punto y coma), revisalo antes de confiar en el analisis")

        st.subheader("Informacion del archivo")
        st.write("Nombre:", info["nombre"])
        st.write("Extension:", info["extension"])

        st.subheader("Codigo original")
        st.code(codigo, language="python")

        # fase lexica
        self.lexico.analizar(codigo)
        tokens = self.lexico.obtener_tokens()
        errores_lexicos = self.lexico.obtener_errores()

        st.subheader("Tokens")
        if len(tokens) == 0:
            st.warning("No se encontraron tokens")
        else:
            st.dataframe(tokens, use_container_width=True)

        st.subheader("Errores lexicos")
        if len(errores_lexicos) == 0:
            st.success("No hay errores lexicos")
        else:
            st.dataframe(errores_lexicos, use_container_width=True)

        # fase sintactica, usa el mismo flujo de tokens que ya lleno el lexico
        self.sintactico.analizar(self.lexico.tokens)
        errores_sintacticos = self.sintactico.obtener_errores()

        st.subheader("Errores sintacticos")
        if len(errores_sintacticos) == 0:
            st.success("El codigo es sintacticamente correcto")
        else:
            st.dataframe(errores_sintacticos, use_container_width=True)

        with st.expander("Ver arbol sintactico"):
            st.text(self.sintactico.obtener_arbol_texto())

        # fase semantica, solo tiene sentido revisarla si la sintaxis quedo bien
        st.subheader("Errores semanticos")
        if self.sintactico.es_valido():
            self.semantico.analizar(self.sintactico.arbol, self.sintactico.parser)
            errores_semanticos = self.semantico.obtener_errores()

            if len(errores_semanticos) == 0:
                st.success("No se encontraron errores semanticos")
            else:
                st.dataframe(errores_semanticos, use_container_width=True)
        else:
            st.info("Se omite el analisis semantico porque hay errores sintacticos primero")


if __name__ == "__main__":
    app = App()
    app.ejecutar()
