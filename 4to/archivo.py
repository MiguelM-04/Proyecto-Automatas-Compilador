# Creamos la clase Archivo adaptada para Streamlit y archivos .py
class Archivo:

    # Constructor de la clase
    def __init__(self, archivo_subido):
        # Guardamos el objeto que nos da Streamlit en memoria
        self.archivo_subido = archivo_subido

    # Metodo para saber si el archivo existe
    def existe(self):
        return self.archivo_subido is not None

    # Metodo para obtener la extension del archivo
    def extension(self):
        nombre_archivo = self.archivo_subido.name
        if "." in nombre_archivo:
            return "." + nombre_archivo.rsplit(".", 1)[1]
        return ""

    # Metodo para validar si el archivo es .py
    def es_el_tipo_correcto(self):
        return self.extension() == ".py"

    # Metodo para leer el contenido del archivo
    def leer(self):
        return self.archivo_subido.getvalue().decode("utf-8")

    # Metodo para obtener el desglose de informacion del archivo
    def obtener_info(self):
        nombre_archivo = self.archivo_subido.name
        if "." in nombre_archivo:
            nombre, ext = nombre_archivo.rsplit(".", 1)
            ext = "." + ext
        else:
            nombre, ext = nombre_archivo, ""

        return {
            "nombre": nombre,
            "extension": ext
        }

    # aqui checamos rasgos que Python no usa pero otros lenguajes si
    def contenido_parece_python(self, codigo):
        lineas = codigo.count("\n") + 1

        llaves = codigo.count("{") + codigo.count("}")
        punto_y_coma = codigo.count(";")

        # java, c, js, etc usan muchas llaves y punto y coma por linea, python no
        if llaves > lineas * 0.3:
            return False
        if punto_y_coma > lineas * 0.5:
            return False

        return True
