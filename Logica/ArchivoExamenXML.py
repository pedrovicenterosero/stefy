import xml.etree.ElementTree as ET
import os.path

class ArchivoExamenXML:
    # Estructura básica del archivo XML
    ELEMENTOSEXAMEN = ["NombreExamen", "Materia", "Grado", "ConjuntosCuestionarios", "NumeroPreguntas", "Respuestas", "CalificacionMinima", "CalificacionMaxima", "RangoCalculoMinimo", "RangoCalculoMaximo"]

    def __init__(self, nombre = None):
        self.__nombre = nombre
        self.__nombreExamen = ""
        self.__materia = ""
        self.__grado = ""
        self.__conjuntosCuestionarios = "1"
        self.__numeroPreguntas = "10"
        self.__calificacionMinima = "1"
        self.__calificacionMaxima = "5"
        self.__rangoCalculoMinimo = "0"
        self.__rangoCalculoMaximo = "5"
        self.__arbol = None
        self.__examen = None
        self.__cadenaXML = ""
        self.__errorArchivo = ""

    @property
    def nombre(self):
        return self.__nombre

    @property
    def nombreExamen(self):
        return self.__nombreExamen

    @nombreExamen.setter
    def nombreExamen(self, valor):
        self.__nombreExamen = valor

    @property
    def materia(self):
        return self.__materia

    @materia.setter
    def materia(self, valor):
        self.__materia = valor

    @property
    def grado(self):
        return self.__grado

    @grado.setter
    def grado(self, valor):
        self.__grado = valor

    @property
    def conjuntosCuestionarios(self):
        return self.__conjuntosCuestionarios

    @conjuntosCuestionarios.setter
    def conjuntosCuestionarios(self, valor):
        self.__conjuntosCuestionarios = valor
    @property
    def numeroPreguntas(self):
        return self.__numeroPreguntas

    @numeroPreguntas.setter
    def numeroPreguntas(self, valor):
        self.__numeroPreguntas = valor

    @property
    def calificacionMinima(self):
        return self.__calificacionMinima
    @calificacionMinima.setter
    def calificacionMinima(self, valor):
        self.__calificacionMinima = valor

    @property
    def calificacionMaxima(self):
        return self.__calificacionMaxima
    @calificacionMaxima.setter
    def calificacionMaxima(self, valor):
        self.__calificacionMaxima = valor

    @property
    def rangoCalculoMinimo(self):
        return self.__rangoCalculoMinimo
    @rangoCalculoMinimo.setter
    def rangoCalculoMinimo(self, valor):
        self.__rangoCalculoMinimo = valor

    @property
    def rangoCalculoMaximo(self):
        return self.__rangoCalculoMaximo

    @rangoCalculoMaximo.setter
    def rangoCalculoMaximo(self, valor):
        self.__rangoCalculoMaximo = valor

    @property
    def errorArchivo(self):
        return self.__errorArchivo

    @property
    def existenClaves(self):
        return self.__existenClavesRespuesta()

    # @existenClaves.setter
    # def existenClaves(self, valor):
    #     self.__existenClaves = valor

    def crearEstructura(self):
        # Crear el elemento raíz
        examen = ET.Element("Examen")
        # Crear subelementos y agregarlos al elemento raíz
        nombreExamen = ET.SubElement(examen, "NombreExamen")
        # nombreExamen.text = self.nombreExamen

        materia = ET.SubElement(examen, "Materia")
        # materia.text = self.__materia

        grado = ET.SubElement(examen, "Grado")
        # grado.text = self.__grado

        conjuntosCuestionarios = ET.SubElement(examen, "ConjuntosCuestionarios")
        # conjuntosCuestionarios.text = self.__conjuntosCuestionarios

        numeroPreguntas = ET.SubElement(examen, "NumeroPreguntas")
        # numeroPreguntas.text = self.__numeroPreguntas

        calificacionMinima = ET.SubElement(examen, "CalificacionMinima")
        # calificacionMinima.text = self.__calificacionMinima

        calificacionMaxima = ET.SubElement(examen, "CalificacionMaxima")
        # calificacionMaxima.text = self.__calificacionMaxima

        rangoCalculoMinimo = ET.SubElement(examen, "RangoCalculoMinimo")
        # rangoCalculoMinimo.text = self.__rangoCalculoMinimo

        rangoCalculoMaximo = ET.SubElement(examen, "RangoCalculoMaximo")
        # rangoCalculoMaximo.text = self.__rangoCalculoMaximo

        # Crear subelemento Respuestas y agregarlo al elemento raíz
        respuestas = ET.SubElement(examen, "Respuestas")
        print(f"Numero de cuestionarios -----> {self.__conjuntosCuestionarios}")
        for i in range(int(self.__conjuntosCuestionarios)):
            cuestionario = respuestas.find(f".//Cuestionario{str(i+1).zfill(2)}")
            if cuestionario is None:
                ET.SubElement(respuestas, f"Cuestionario{str(i+1).zfill(2)}")

        self.__examen = examen
        self.__arbol = ET.ElementTree(examen)
        print("Nueva estructura de archivo xml")
        return #self.__cadenaXML

    def actualizarValores(self):
        # nombreExamen = ET.SubElement(examen, "NombreExamen")
        nombreExamen = self.__examen.find(".//NombreExamen")
        nombreExamen.text = self.nombreExamen

        # materia = ET.SubElement(examen, "Materia")
        materia = self.__examen.find(".//Materia")
        materia.text = self.__materia

        # grado = ET.SubElement(examen, "Grado")
        grado = self.__examen.find(".//Grado")
        grado.text = self.__grado

        # conjuntosCuestionarios = ET.SubElement(examen, "ConjuntosCuestionarios")
        conjuntosCuestionarios = self.__examen.find(".//ConjuntosCuestionarios")
        conjuntosCuestionarios.text = self.__conjuntosCuestionarios

        # numeroPreguntas = ET.SubElement(examen, "NumeroPreguntas")
        numeroPreguntas = self.__examen.find(".//NumeroPreguntas")
        numeroPreguntas.text = self.__numeroPreguntas

        # calificacionMinima = ET.SubElement(examen, "CalificacionMinima")
        calificacionMinima = self.__examen.find(".//CalificacionMinima")
        calificacionMinima.text = self.__calificacionMinima

        # calificacionMaxima = ET.SubElement(examen, "CalificacionMaxima")
        calificacionMaxima = self.__examen.find(".//CalificacionMaxima")
        calificacionMaxima.text = self.__calificacionMaxima

        # rangoCalculoMinimo = ET.SubElement(examen, "RangoCalculoMinimo")
        rangoCalculoMinimo = self.__examen.find(".//RangoCalculoMinimo")
        rangoCalculoMinimo.text = self.__rangoCalculoMinimo

        # rangoCalculoMaximo = ET.SubElement(examen, "RangoCalculoMaximo")
        rangoCalculoMaximo = self.__examen.find(".//RangoCalculoMaximo")
        rangoCalculoMaximo.text = self.__rangoCalculoMaximo

    def agregarRespuestas(self, numeroCuestionario="1", diccionarioRespuestas={}):
        # raiz = ET.fromstring(self.__cadenaXML)
        respuestas = self.__arbol.find(".//Respuestas")

        etiquetaCuestionario = f".//Cuestionario{numeroCuestionario.zfill(2)}"
        cuestionario = respuestas.find(etiquetaCuestionario)
        if cuestionario is None:
            cuestionario = ET.SubElement(respuestas, f"Cuestionario{numeroCuestionario.zfill(2)}")

        # print(len(list(cuestionario)))

        # Agregar o modificar las respuestas existentes
        for claveItem, valorRespuesta in diccionarioRespuestas.items():
            claveItem = "P" + claveItem
            itemRespuesta = cuestionario.find(claveItem)
            if itemRespuesta is None:
                itemRespuesta = ET.SubElement(cuestionario, claveItem)
            itemRespuesta.text = valorRespuesta

        # Eliminar los subelementos que no están en el diccionario
        for itemRespuesta in list(cuestionario):
            nuevoTag = itemRespuesta.tag[1:]
            # if itemRespuesta.tag not in diccionarioRespuestas:
            #     cuestionario.remove(itemRespuesta)
            if nuevoTag not in diccionarioRespuestas:
                cuestionario.remove(itemRespuesta)

        # print(len(list(cuestionario)))

        raizExamen = self.__arbol.getroot()
        cadenaXML = ET.tostring(raizExamen, encoding="utf8").decode("utf8")
        return cadenaXML

    def devolverRespuestas(self, numeroCuestionario="1"):
        respuestas = self.__arbol.find(".//Respuestas")
        etiquetaCuestionario = f".//Cuestionario{numeroCuestionario.zfill(2)}"
        cuestionario = respuestas.find(etiquetaCuestionario)
        diccionarioClaves = {}
        if cuestionario is not None:
            for itemRespuesta in list(cuestionario):
                diccionarioClaves[itemRespuesta.tag[1:]] = itemRespuesta.text

        return diccionarioClaves

    def __existenClavesRespuesta(self):
        respuestas = self.__arbol.find(".//Respuestas")

        for i in range(int(self.__conjuntosCuestionarios)):
            etiquetaCuestionario = f".//Cuestionario{str(i + 1).zfill(2)}"
            cuestionario = respuestas.find(etiquetaCuestionario)
            if cuestionario is not None:
                if len(list(cuestionario)) > 0:
                    return True
        return False

    def eliminarExcesoCuestionarios(self, totalCuestionarios: int):
        """
        Cuando en el archivo XML existen mas cuestionarios registrados que los que se van a utilizar se eliminan los excedentes

        Args:
            totalCuestionarios: Número total de cuestionarios que deben quedar

        Returns:
            None
        """
        respuestas = self.__arbol.find(".//Respuestas")
        numeroCuestionarios = len(list(respuestas))
        if totalCuestionarios < numeroCuestionarios:
            for i in range(totalCuestionarios, numeroCuestionarios):
                etiqueteCuestionario = f".//Cuestionario{str(i + 1).zfill(2)}"
                cuestionario = respuestas.find(etiqueteCuestionario)
                respuestas.remove(cuestionario)

    def guardar(self, nuevoNombre=None):
        if nuevoNombre is not None:
            self.__nombre = nuevoNombre

        self.__arbol.write(self.__nombre, encoding="UTF-8", xml_declaration=True)

    def abrir(self):
        # Leer el contenido del archivo XML
        if not self.__archivoValido(self.__nombre):
            return False

        self.__arbol = ET.parse(self.__nombre)
        self.__examen = self.__arbol.getroot()
        self.__devolverValores()
        return True

    def __archivoValido(self, archivoXML):
        try:
            # Intenta analizar el archivo XML
            arbol = ET.parse(archivoXML)
            raiz = arbol.getroot()

            # Verifica si la raíz es 'Examen'
            if raiz.tag != 'Examen':
                raise ValueError("La raíz del XML no correponde a la de un archivo 'Examen'")

            elementosActuales = {elementoHijo.tag for elementoHijo in raiz}
            if elementosActuales != set(self.ELEMENTOSEXAMEN):
                raise ValueError("Los elementos encontrados en el archivo no corresponden a los elementos básicos del examen")

            # print(f"El archivo {os.path.basename(archivoXML)} tiene la estructura XML correcta.")
            return True
        except ET.ParseError as error:
            self.__errorArchivo = f"El archivo {os.path.basename(archivoXML)} no es un XML bien formado. {error}"
            print(f"Se produjo un error de tipo {type(error).__name__}: {str(error)}")
        except ValueError as e:
            self.__errorArchivo = f"El archivo {os.path.basename(archivoXML)} no tiene la estructura XML correcta: {e}"

        return False

    def __devolverValores(self):
        nombreExamen = self.__examen.find("NombreExamen")
        self.__nombreExamen = nombreExamen.text

        materia = self.__examen.find("Materia")
        self.__materia = materia.text

        grado = self.__examen.find("Grado")
        self.__grado = grado.text

        conjuntosCuestionarios = self.__examen.find("ConjuntosCuestionarios")
        self.__conjuntosCuestionarios = conjuntosCuestionarios.text

        numeroPreguntas = self.__examen.find("NumeroPreguntas")
        self.__numeroPreguntas = numeroPreguntas.text
