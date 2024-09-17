import xml.etree.ElementTree as ET
import os.path

class Configuracion:
    ELEMENTOSCONFIGURACION = ["PuntosGuiaPrincipales", "PuntosGuiaSecundarios", "OpcionRespuesta"]

    def __init__(self, nombreArchivo):
        self.__nombreArchivo = nombreArchivo
        self.__umbralColorPuntosGuiaPrincipales = 60
        self.__umbralColorPuntosGuiaSecundarios = 60
        self.__umbralColorOpcionMarcada = 127

        self.__arbol = None
        self.__configuracion = None
        self.__cadenaXML = ""
        self.__errorArchivo = ""

    @property
    def nombreArchivo(self):
        return self.__nombreArchivo

    @nombreArchivo.setter
    def nombreArchivo(self, valor):
        self.nombreArchivo = valor

    @property
    def umbralColorPuntosGuiaPrincipales(self):
        return self.__umbralColorPuntosGuiaPrincipales

    @umbralColorPuntosGuiaPrincipales.setter
    def umbralColorPuntosGuiaPrincipales(self, valor):
        self.__umbralColorPuntosGuiaSecundarios = valor

    @property
    def umbralColorPuntosGuiaSecundarios(self):
        return self.__umbralColorPuntosGuiaSecundarios

    @umbralColorPuntosGuiaSecundarios.setter
    def umbralColorPuntosGuiaSecundarios(self, valor):
        self.__umbralColorPuntosGuiaSecundarios = valor

    @property
    def umbralColorOpcionMarcada(self):
        return self.__umbralColorOpcionMarcada

    @umbralColorOpcionMarcada.setter
    def umbralColorOpcionMarcada(self, valor):
        self.__umbralColorOpcionMarcada = valor

    @property
    def configuracion(self):
        return self.__configuracion

    def crearEstructura(self):
        # Elemento raiz
        configuracion = ET.Element("Configuracion")
        puntosGuiaPrincipales = ET.SubElement(configuracion, "PuntosGuiaPrincipales")
        umbralColorPGP = ET.SubElement(puntosGuiaPrincipales, "UmbralColor")
        umbralColorPGP.text = "60"

        puntosGuiaSecundarios = ET.SubElement(configuracion, "PuntosGuiaSecundarios")
        umbralColorPGS = ET.SubElement(puntosGuiaSecundarios, "UmbralColor")
        umbralColorPGS.text = "60"

        opcionRespuesta = ET.SubElement(configuracion, "OpcionRespuesta")
        umbralColorMarcada = ET.SubElement(opcionRespuesta, "UmbralColorMarcada")
        umbralColorMarcada.text = "127"

        self.__configuracion = configuracion
        self.__arbol = ET.ElementTree(configuracion)

        # raizConfiguracion = self.__arbol.getroot()
        # cadenaXML = ET.tostring(raizConfiguracion, encoding="utf8").decode("utf8")
        # print(cadenaXML)
        # print("Estructura de configuración creada...")


    def actualizarValores(self):
        puntosGuiaPrincipales = self.__arbol.find(".//PuntosGuiaPrincipales")
        umbralColorPGP = puntosGuiaPrincipales.find(".//UmbralColor")
        umbralColorPGP.text = self.__umbralColorPuntosGuiaPrincipales
        # print("Actualizando...1")
        puntosGuiaSecundarios = self.__arbol.find(".//PuntosGuiaSecundarios")
        umbralColorPGS = puntosGuiaSecundarios.find(".//UmbralColor")
        umbralColorPGS.text = self.__umbralColorPuntosGuiaSecundarios
        # print("Actualizando...2")
        opcionRespuesta = self.__arbol.find(".//OpcionRespuesta")
        umbralColorMarcada = opcionRespuesta.find(".//UmbralColorMarcada")
        umbralColorMarcada.text = self.__umbralColorOpcionMarcada
        # print("Actualizando...3")
        # raizConfiguracion = self.__arbol.getroot()
        # cadenaXML = ET.tostring(raizConfiguracion, encoding="utf8").decode("utf8")
        # print("Actualizando...4")
        # print(cadenaXML)
        # return cadenaXML

    def __devolverValores(self):
        puntosGuiaPrincipales = self.__arbol.find(".//PuntosGuiaPrincipales")
        umbralColorPGP = puntosGuiaPrincipales.find(".//UmbralColor")
        self.__umbralColorPuntosGuiaPrincipales = umbralColorPGP.text

        puntosGuiaSecundarios = self.__arbol.find(".//PuntosGuiaSecundarios")
        umbralColorPGS = puntosGuiaSecundarios.find(".//UmbralColor")
        self.__umbralColorPuntosGuiaSecundarios = umbralColorPGS.text

        opcionRespuesta = self.__arbol.find(".//OpcionRespuesta")
        umbralColorMarcada = opcionRespuesta.find(".//UmbralColorMarcada")
        self.__umbralColorOpcionMarcada = umbralColorMarcada.text

    def guardar(self, nuevoNombre=None):
        if nuevoNombre is not None:
            self.__nombre = nuevoNombre

        self.__arbol.write(self.__nombre)

    def abrir(self):
        if not os.path.exists(self.__nombreArchivo):
            return False

        # Leer el contenido del archivo XML
        if not self.__archivoValido(self.__nombreArchivo):
            return False

        self.__arbol = ET.parse(self.__nombreArchivo)
        self.__configuracion = self.__arbol.getroot()
        self.__devolverValores()
        return True

    def __archivoValido(self, archivoXML):
        try:
            # Intenta analizar el archivo XML
            arbol = ET.parse(archivoXML)
            raiz = arbol.getroot()

            # Verifica si la raíz es 'Configuracion'
            if raiz.tag != 'Configuracion':
                raise ValueError("La raíz del archivo XML no correponde a la de un archivo de configuración")

            elementosActuales = {elementoHijo.tag for elementoHijo in raiz}
            if elementosActuales != set(self.ELEMENTOSCONFIGURACION):
                raise ValueError("Los elementos encontrados en el archivo no corresponden a los elementos básicos de la configuración")

            # print(f"El archivo {os.path.basename(archivoXML)} tiene la estructura XML correcta.")
            return True
        except ET.ParseError as error:
            self.__errorArchivo = f"El archivo {os.path.basename(archivoXML)} no es un XML bien formado. {error}"
            print(f"Se produjo un error de tipo {type(error).__name__}: {str(error)}")
        except ValueError as e:
            self.__errorArchivo = f"El archivo {os.path.basename(archivoXML)} no tiene la estructura XML correcta: {e}"

        return False