from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

class MetodosHojaPDF:
    @staticmethod
    def lineaBaseTexto(documentoPDF: canvas.Canvas, x, y, ancho=1):
        documentoPDF.line(x, y, x, y + 10)
        documentoPDF.line(x, y, x + ancho, y)
        documentoPDF.line(x + ancho, y, x + ancho, y + 10)

    @staticmethod
    def centrarTexto(cadenaTexto: str, documentoPDF: canvas.Canvas, posicionX: int, posicionY: int, tamanoFuente: int,
                     negrilla=False):
        # if negrilla:
        #     fuente = "Helvetica-Bold"
        # else:
        #     fuente = "Helvetica"
        # anchoTexto = stringWidth(cadenaTexto, fuente, tamanoFuente)
        anchoHoja = int(documentoPDF._pagesize[0] / 2)
        margenIzquierdo = posicionX % anchoHoja
        anchoHoja = anchoHoja - 2 * margenIzquierdo
        # xCentrada = int(posicionX + (anchoHoja - anchoTexto) / 2 - margenIzquierdo)  # - self.ALTOGUIA
        # texto = documentoPDF.beginText(xCentrada, posicionY)
        # texto.setFont(fuente, tamanoFuente)
        # texto.textLine(cadenaTexto)
        # documentoPDF.drawText(texto)

        MetodosHojaPDF.centrarTextoRegion(cadenaTexto, documentoPDF, posicionX , posicionY, tamanoFuente, negrilla, anchoRegion=anchoHoja)

    @staticmethod
    def centrarTextoRegion(cadenaTexto:str, documentoPDF:canvas.Canvas, posicionX, posicionY, tamanoFuente, negrilla=False, anchoRegion=0):
        if negrilla:
            fuente = "Helvetica-Bold"
        else:
            fuente = "Helvetica"
        anchoTexto = stringWidth(cadenaTexto, fuente, tamanoFuente)
        xCentrada = posicionX + int((anchoRegion - anchoTexto) / 2)
        texto = documentoPDF.beginText(xCentrada, posicionY)
        texto.setFont(fuente, tamanoFuente)
        texto.textLine(cadenaTexto)
        documentoPDF.drawText(texto)

    @staticmethod
    def partirTexto(cadenaTexto: str, anchoDisponible, tamanoFuente: int, negrilla=False):
        if negrilla:
            fuente = "Helvetica-Bold"
        else:
            fuente = "Helvetica"

        subcadenas = list()
        if len(cadenaTexto) > 0:
            palabras = cadenaTexto.split()
            palabraMaxima = max(palabras, key=len)
            anchoPalabraMaxima = stringWidth(palabraMaxima, fuente, tamanoFuente)
            if anchoPalabraMaxima >= anchoDisponible:
                subcadenas.append("<No se puede mostrar el texto por que contiene una palabra muy larga>")
                return subcadenas

        while len(cadenaTexto) > 0:
            indiceEspacio = 1
            subcadenaIzquierda = cadenaTexto
            anchoTexto = stringWidth(cadenaTexto, fuente, tamanoFuente)
            while anchoTexto > anchoDisponible:
                indiceEspacio = subcadenaIzquierda.rfind(" ")
                subcadenaIzquierda = cadenaTexto[0:indiceEspacio]
                anchoTexto = stringWidth(subcadenaIzquierda, fuente, tamanoFuente)
            subcadenas.append(subcadenaIzquierda)
            if len(subcadenaIzquierda) >= len(cadenaTexto):
                break
            cadenaTexto = cadenaTexto[indiceEspacio + 1:len(cadenaTexto)]
        return subcadenas

class HojaRespuestasPDF:
    def __init__(self, posicionX=35 , posicionY=555):
        self.__documentoPDF = None # canvas.Canvas(nombreArchivo, pagesize=landscape(letter))
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        self.__institucion = "(TITULO PRINCIPAL)"
        self.__area = "(TITULO 2)"
        self.__tema = "(TITULO 3)"
        self.__archivoLogo = ""
        self.__mensajeEncabezado = "RELLENE LOS CIRCULOS QUE CORRESPONDAN A LA OPCIÓN DE SU RESPUESTA CORRECTA UTILIZANDO LAPIZ DE COLOR NEGRO."
        self.__tituloIdentificacion = "DATOS DEL EVALUADO"
        self.__textoNombres = "NOMBRES Y APELLIDOS"
        self.__textoGrado = "CURSO"
        self.__tituloCodigo = "Rellene los circulos que correspondan a los dÍgitos de su código de identificación."
        self.__textoCodigo = "CODIGO"
        self.__tituloCuestionario = "CUESTIONARIO"
        self.__textoCuestionario = "ID CUESTIONARIO"
        self.__tituloRespuestas = "RESPUESTAS"
        self.__nombreArchivo = "Nuevo archivo"

    #region Propiedades
    @property
    def nombreArchivo(self):
        return self.__nombreArchivo

    @nombreArchivo.setter
    def nombreArchivo(self, valor):
        self.__nombreArchivo = valor

    @property
    def nombreInstitucion(self):
        return self.__institucion

    @nombreInstitucion.setter
    def nombreInstitucion(self, valor):
        self.__institucion = valor

    @property
    def nombreArea(self):
        return self.__area

    @nombreArea.setter
    def nombreArea(self, valor):
        self.__area = valor

    @property
    def nombreTema(self):
        return self.__tema

    @nombreTema.setter
    def nombreTema(self, valor):
        self.__tema = valor

    @property
    def archivoLogo(self):
        return self.__archivoLogo

    @archivoLogo.setter
    def archivoLogo(self, valor):
        self.__archivoLogo = valor

    @property
    def mensajeEncabezado(self):
        return self.__mensajeEncabezado

    @mensajeEncabezado.setter
    def mensajeEncabezado(self, valor):
        self.__mensajeEncabezado = valor

    @property
    def tituloIdentificacion(self):
        return self.__tituloIdentificacion

    @tituloIdentificacion.setter
    def tituloIdentificacion(self, valor):
        self.__tituloIdentificacion = valor

    @property
    def tituloCodigo(self):
        return self.__tituloCodigo

    @tituloCodigo.setter
    def tituloCodigo(self, valor):
        self.__tituloCodigo = valor

    @property
    def tituloCuestionario(self):
        return self.__tituloCuestionario

    @tituloCuestionario.setter
    def tituloCuestionario(self, valor):
        self.__tituloCuestionario = valor

    @property
    def textoCuestionario(self):
        return self.__textoCuestionario

    @textoCuestionario.setter
    def textoCuestionario(self, valor):
        self.__textoCuestionario = valor

    @property
    def textoNombres(self):
        return self.__textoNombres

    @textoNombres.setter
    def textoNombres(self, valor):
        self.__textoNombres = valor

    @property
    def textoGrado(self):
        return self.__textoGrado

    @textoGrado.setter
    def textoGrado(self, valor):
        self.__textoGrado = valor

    @property
    def textoCodigo(self):
        return self.__textoCodigo

    @textoCodigo.setter
    def textoCodigo(self, valor):
        self.__textoCodigo = valor

    @property
    def tituloRespuestas(self):
        return self.__tituloRespuestas

    @tituloRespuestas.setter
    def tituloRespuestas(self,valor):
        self.__tituloRespuestas = valor

    #endregion

    def dibujar(self):
        self.__documentoPDF = canvas.Canvas(self.__nombreArchivo, pagesize=landscape(letter))
        # Traza la linea de división de página para las dos hojas de respuesta
        imagenTijera = ImageReader('Gui/imagenes/tijera.jpg')
        self.__documentoPDF.drawImage(imagenTijera, self.__documentoPDF._pagesize[0] / 2 - 7, self.__documentoPDF._pagesize[1] - 16, height=14, width=14,
                      preserveAspectRatio=True)
        self.__documentoPDF.setDash(1, 4)
        self.__documentoPDF.line(self.__documentoPDF._pagesize[0] / 2, 0, self.__documentoPDF._pagesize[0] / 2, self.__documentoPDF._pagesize[1])
        self.__documentoPDF.setDash()
        separador = 5
        encabezadoI = Encabezado(self.__documentoPDF, self.__posicionX, self.__posicionY - separador, self.__institucion, self.__area, self.__tema, self.__mensajeEncabezado, logo=self.__archivoLogo)
        encabezadoI.dibujar()
        encabezadoD = Encabezado(self.__documentoPDF, self.__posicionX + self.__documentoPDF._pagesize[0] / 2, self.__posicionY - separador, self.__institucion, self.__area, self.__tema, self.__mensajeEncabezado, logo=self.__archivoLogo)
        encabezadoD.dibujar()
        separador += 85
        identificacionI = Identificacion(self.__documentoPDF, self.__posicionX, self.__posicionY - separador, titulo = self.__tituloIdentificacion)
        identificacionI.textoNombres = self.__textoNombres
        identificacionI.textoGrado = self.__textoGrado
        identificacionI.tituloCodigo = self.__tituloCodigo
        identificacionI.textoCodigo = self.__textoCodigo
        identificacionI.dibujar()
        identificacionD = Identificacion(self.__documentoPDF, self.__posicionX + self.__documentoPDF._pagesize[0] / 2, self.__posicionY - separador, titulo=self.__tituloIdentificacion)
        identificacionD.tituloCodigo = self.__tituloCodigo
        identificacionD.textoNombres = self.__textoNombres
        identificacionD.textoGrado = self.__textoGrado
        identificacionD.textoCodigo = self.__textoCodigo
        identificacionD.dibujar()
        separador += 45
        cuestionarioI = Cuestionario(self.__documentoPDF, self.__posicionX, self.__posicionY - separador, titulo=self.__tituloCuestionario)
        cuestionarioI.textoCuestionario = self.__textoCuestionario
        cuestionarioI.dibujar()
        cuestionarioD = Cuestionario(self.__documentoPDF, self.__posicionX + self.__documentoPDF._pagesize[0] / 2, self.__posicionY - separador, titulo=self.__tituloCuestionario)
        cuestionarioD.textoCuestionario = self.__textoCuestionario
        cuestionarioD.dibujar()
        separador += 55
        respuestasI = Respuestas(self.__documentoPDF, self.__posicionX, self.__posicionY - separador, titulo=self.__tituloRespuestas, cantidadBloques=2)
        respuestasI.dibujar()
        respuestasD = Respuestas(self.__documentoPDF, self.__posicionX + self.__documentoPDF._pagesize[0] / 2, self.__posicionY - separador, titulo=self.__tituloRespuestas, cantidadBloques=2)
        respuestasD.dibujar()
        separador += 325
        piepaginaI = PiePagina(self.__documentoPDF, self.__posicionX, self.__posicionY - separador)
        piepaginaD = PiePagina(self.__documentoPDF, self.__posicionX + self.__documentoPDF._pagesize[0] / 2, self.__posicionY - separador)

    def guardar(self):
        self.__documentoPDF.save()

class SeccionHoja:
    ALTOGUIA = 12
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, tipoGuia = 1, titulo=''):
        self.__altoGuia = self.ALTOGUIA / tipoGuia
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX #+ self.ALTOGUIA
        self.__posicionY = posicionY
        self.__tipoGuia = tipoGuia
        self.__titulo = titulo
        self.__marcaGuia()

    #region Propiedades
    @property
    def altoGuia(self):
        return self.__altoGuia
    #endregion

    def __marcaGuia(self):
        # Establecer el color del cuadro guia
        self.__documentoPDF.setFillColorRGB(0, 0, 0)
        # Dibujar el cuadrado relleno de color negro superior izquierdo
        self.__documentoPDF.rect(self.__posicionX, self.__posicionY + 5, self.__altoGuia,
                                 self.__altoGuia, fill=1)
        # Aquí se debe escribir el titulo de la seccion.....
        MetodosHojaPDF.centrarTexto(self.__titulo, self.__documentoPDF, self.__posicionX, self.__posicionY + self.__altoGuia, 9, True)
        # Dibujar el cuadrado relleno de color negro superior derecho para las guias primarias
        if self.__tipoGuia == 1:
            anchoHoja = self.__documentoPDF._pagesize[0] / 2
            self.__documentoPDF.rect(self.__posicionX + anchoHoja - 70 - 1 * self.__altoGuia, self.__posicionY + 5,
                                     self.__altoGuia, self.__altoGuia, fill=1)
class Encabezado(SeccionHoja):
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, institucion, area, tema, mensajeEncabezado="", logo=""):
        super().__init__(documentoPDF, posicionX, posicionY)
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX + super().ALTOGUIA
        self.__posicionY = posicionY
        self.__institucion = institucion
        self.__area = area
        self.__tema = tema
        self.__mensajeEncabezado = mensajeEncabezado
        self.__logo = logo

    def dibujar(self):
        sangriaTexto = 0
        # print(f"Archivo logo PDF{self.__logo}")
        # if len(self.__logo) > 0:
        if self.__logo is not None:
            sangriaTexto = 40
            imagenLogo = ImageReader(self.__logo)
            self.__documentoPDF.drawImage(imagenLogo,
                                          self.__posicionX,
                                          self.__posicionY - 36,
                                          width=36,
                                          height=36,
                                          preserveAspectRatio=True)
        textoInstitucion = self.__documentoPDF.beginText(self.__posicionX + sangriaTexto, self.__posicionY - 8)
        textoInstitucion.setFont('Helvetica-Bold', 9)
        textoInstitucion.textLine(self.__institucion)
        self.__documentoPDF.drawText(textoInstitucion)

        textoArea = self.__documentoPDF.beginText(self.__posicionX + sangriaTexto, self.__posicionY - 20)
        textoArea.setFont('Helvetica', 8)
        textoArea.textLine(self.__area)
        self.__documentoPDF.drawText(textoArea)

        textoTema = self.__documentoPDF.beginText(self.__posicionX + sangriaTexto, self.__posicionY - 32)
        textoTema.setFont('Helvetica', 8)
        textoTema.textLine(self.__tema)
        self.__documentoPDF.drawText(textoTema)

        anchoPagina = self.__documentoPDF._pagesize[0]
        margenIzquierdo = int(self.__posicionX - self.ALTOGUIA) % int(anchoPagina / 2)
        anchoDisponible = anchoPagina / 2 - 2 * (margenIzquierdo + self.ALTOGUIA)
        lineasTexto = MetodosHojaPDF.partirTexto(self.__mensajeEncabezado, anchoDisponible, 6)
        i = 0
        for linea in lineasTexto:
            MetodosHojaPDF.centrarTexto(linea, self.__documentoPDF, self.__posicionX, self.__posicionY - 50 - 8 * i, 6)
            i += 1

class Datos:
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, texto='NOMBRES'):
        self.__texto = texto
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY

    #region Propiedades
    @property
    def documentoPDF(self):
        return self.__documentoPDF

    @property
    def posicionX(self):
        return self.__posicionX

    @property
    def posicionY(self):
        return self.__posicionY
    #endregion

    def dibujar(self, ancho=30):
        MetodosHojaPDF.lineaBaseTexto(self.__documentoPDF, self.__posicionX, self.__posicionY, ancho=ancho)
        texto = self.__documentoPDF.beginText(self.__posicionX + 2, self.__posicionY + 5)
        texto.setFont('Helvetica', 6)
        texto.textLine(self.__texto)
        self.__documentoPDF.drawText(texto)

class Codigo:
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, titulo=''):
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX #+ self.ALTOGUIA
        self.__posicionY = posicionY
        self.__titulo = titulo
        self.__textoCodigo = ""

    #region Propiedades
    @property
    def textoCodigo(self):
        return self.__textoCodigo

    @textoCodigo.setter
    def textoCodigo(self, valor):
        self.__textoCodigo = valor
    #endregion
    def dibujar(self):
        SANGRIA = 40
        MetodosHojaPDF.centrarTexto(self.__titulo, self.__documentoPDF, self.__posicionX, self.__posicionY, 7)
        # texto = self.__documentoPDF.beginText(SANGRIA + self.__posicionX, self.__posicionY - 15)
        # texto.setFont('Helvetica', size=8)
        # texto.textLine(self.__textoCodigo)
        MetodosHojaPDF.centrarTextoRegion(self.__textoCodigo, self.__documentoPDF, SANGRIA + self.__posicionX + 1, self.__posicionY - 15, 7, anchoRegion=30)
        # self.__documentoPDF.drawText()

        ANCHOX = 18
        ALTOY = 16
        for i in range(10):
            texto = self.__documentoPDF.beginText(SANGRIA + 40 + self.__posicionX + i * ANCHOX, self.__posicionY - 15)
            texto.setFont('Helvetica', size=10)
            texto.textLine(str(i))
            self.__documentoPDF.drawText(texto)

        for i in range(6):
            MetodosHojaPDF.lineaBaseTexto(documentoPDF=self.__documentoPDF, x=SANGRIA + self.__posicionX + 1, y=-30 + self.__posicionY - i * ALTOY, ancho=30)
            for j in range(10):
                self.__documentoPDF.circle(SANGRIA + 40 + self.__posicionX + ANCHOX * j + 3, -30 + self.__posicionY - i * ALTOY + 5, 6)

class Identificacion(SeccionHoja):
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, titulo = 'DATOS DEL ESTUDIANTE'):
        super().__init__(documentoPDF, posicionX, posicionY, tipoGuia=2, titulo=titulo)
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        self.__titulo = titulo
        self.__textoCodigo = "CODIGO"
        self.__tituloCodigo = ""
        self.__textoNombre = 'NOMBRES'
        self.__textoGrado = 'GRADO'

    #region Propiedades
    @property
    def textoCodigo(self):
        return  self.__textoCodigo

    @textoCodigo.setter
    def textoCodigo(self, valor):
        self.__textoCodigo = valor

    @property
    def tituloCodigo(self):
        return self.__tituloCodigo

    @tituloCodigo.setter
    def tituloCodigo(self, valor):
        self.__tituloCodigo = valor

    @property
    def textoNombres(self):
        return self.__textoNombre

    @textoNombres.setter
    def textoNombres(self, valor):
        self.__textoNombre = valor

    @property
    def textoGrado(self):
        return self.__textoGrado

    @textoGrado.setter
    def textoGrado(self, valor):
        self.__textoGrado = valor
    #endregion
    def dibujar(self):
        SEPARACIONBLOQUE = 35
        # titulo = self.__textoTitulo
        # centrarTexto(titulo, self.__documentoPDF, self.__posicionX + super().altoGuia, self.__posicionY + self.altoGuia, 9, negrilla=True)
        nombre = Datos(self.__documentoPDF, self.__posicionX + 2 * super().altoGuia, self.__posicionY - 15, self.__textoNombre)
        nombre.dibujar(240)
        grado = Datos(self.__documentoPDF, self.__posicionX + 2 * super().altoGuia + 240, self.__posicionY - 15, self.__textoGrado)
        grado.dibujar(60)

        #Generar otra marca guia para el código
        # super().__init__(self.__documentoPDF, self.__posicionX, self.__posicionY - SEPARACIONBLOQUE, tipoGuia=2)
        # codigo = Codigo(self.__documentoPDF, self.__posicionX + 2 * self.altoGuia, self.__posicionY - SEPARACIONBLOQUE + self.altoGuia, titulo=self.__tituloCodigo)
        # codigo.textoCodigo = self.__textoCodigo
        # codigo.dibujar()

class Cuestionario(SeccionHoja):
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, titulo="CUESTIONARIO"):
        super().__init__(documentoPDF, posicionX, posicionY, tipoGuia=2)
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        self.__titulo = titulo
        self.__textoCuestionario = "ID CUESTIONARIO"

    #region Propiedades
    @property
    def textoCuestionario(self):
        return self.__textoCuestionario

    @textoCuestionario.setter
    def textoCuestionario(self, valor):
        self.__textoCuestionario = valor
    #endregion
    def dibujar(self):
        titulo = self.__titulo
        MetodosHojaPDF.centrarTexto(titulo, self.__documentoPDF, self.__posicionX + self.altoGuia, self.__posicionY + self.altoGuia, 9, True)
        datosCuestionario = Datos(self.__documentoPDF, self.__posicionX + 2 * self.altoGuia + 65, self.__posicionY - 25, self.__textoCuestionario)
        datosCuestionario. dibujar(165)
        for i in range(4):
            posicionX = self.__posicionX + 155 + i * 25
            texto = self.__documentoPDF.beginText(posicionX - 4, self.__posicionY - 7)
            texto.setFont("Helvetica", 7)
            texto.textLine(f"C{str(i + 1)}")
            self.__documentoPDF.circle(posicionX, self.__posicionY - 16, 7)
            self.__documentoPDF.drawText(texto)

class ItemRespuesta:
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, numeroItem=1, cantidadOpciones=4):
        self.__documentoPDF = documentoPDF
        self.__numeroItem = numeroItem
        self.__cantidadOpciones = cantidadOpciones
        self.__posicionX = posicionX
        self.__posicionY = posicionY

    def dibujar(self):
        # Se calcula el ancho de texto del numero de item para alinearlo a la derecha
        anchoNumeroItem = stringWidth(str(self.__numeroItem), 'Helvetica', 10)
        posicionX = self.__posicionX + 5 - anchoNumeroItem

        texto = self.__documentoPDF.beginText(posicionX, self.__posicionY - 3)
        texto.setFont('Helvetica', 10)
        texto.textLine(str(self.__numeroItem))
        self.__documentoPDF.drawText(texto)

        for i in range(self.__cantidadOpciones):
            self.__documentoPDF.circle(self.__posicionX + 20 + i * 25, self.__posicionY, 7)

class BloqueRespuestas:
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, cantidadItems, cantidadOpciones=4, numeroItemInicial = 1):
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        self.__cantidadItems = cantidadItems
        self.__cantidadOpciones = cantidadOpciones
        self.__numeroItemInicial = numeroItemInicial

    def dibujar(self):
        opciones = ['A', 'B', 'C', 'D', 'E', 'F']
        for i in range(self.__cantidadOpciones):
            texto = self.__documentoPDF.beginText(self.__posicionX + 16 + i * 25, self.__posicionY)
            texto.setFont('Helvetica-Bold', 10)
            texto.textLine(opciones[i])
            self.__documentoPDF.drawText(texto)

        for i in range(self.__cantidadItems):
            item = ItemRespuesta(self.__documentoPDF, self.__posicionX, self.__posicionY - 10 - i * 20, self.__numeroItemInicial + i, 4)
            item.dibujar()

class Respuestas(SeccionHoja):
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY, titulo="RESPUESTAS", cantidadBloques = 3):
        super().__init__(documentoPDF, posicionX, posicionY, tipoGuia=2, titulo=titulo)
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        # self.__titulo = titulo
        self.__cantidadBloques = cantidadBloques

    def dibujar(self):
        SANGRIA = 40
        SEPARACIONBLOQUES = 150

        for i in range(self.__cantidadBloques):
            bloqueRespuestas = BloqueRespuestas(self.__documentoPDF,
                                                self.__posicionX + SANGRIA + i * SEPARACIONBLOQUES,
                                                self.__posicionY - 10,
                                                15,
                                                4,
                                                numeroItemInicial= i * 15 + 1)
            bloqueRespuestas.dibujar()

class PiePagina(SeccionHoja):
    def __init__(self, documentoPDF:canvas.Canvas, posicionX, posicionY):
        super().__init__(documentoPDF, posicionX, posicionY, tipoGuia=1)
        self.__documentoPDF = documentoPDF
        self.__posicionX = posicionX
        self.__posicionY = posicionY
        self.agregarMarcasSecundarias()

    def agregarMarcasSecundarias(self):
        self.__documentoPDF.rect(self.__posicionX + 160, self.__posicionY + 5, self.altoGuia/2, self.altoGuia/2,
                                 fill=1)

        # self.__documentoPDF.rect(self.__posicionX + 200, self.__posicionY + 5, self.altoGuia/2, self.altoGuia/2,
        #                          fill=1)