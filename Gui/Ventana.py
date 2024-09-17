import os.path
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QSize, QRect, QTimer, QEvent
from PyQt6.QtWidgets import (QMainWindow, QWidget, QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout, QInputDialog,
                             QSpacerItem, QSizePolicy, QFrame, QLabel, QLayout)
from PyQt6.QtGui import QImage, QPixmap, QIcon, QDoubleValidator
# from PyQt6.QtMultimedia import QCamera #QMediaDevices

from Logica.ArchivoExamenXML import ArchivoExamenXML
from Gui.ItemOpciones import ItemRespuesta
from Logica.HojaRespuestas import HojaRespuestas
from Logica.Evaluador import Evaluador
from Logica.Seleccion import *
from Logica.HojaRespuestasPDF import HojaRespuestasPDF
from Logica.ConfiguracionXML import Configuracion
from Gui.VentanaAjustes import VentanaAjustes

class Ventana(QMainWindow):
    def __init__(self):
        super(Ventana, self).__init__()
        self.__archivoExamenXML = None
        self.__itemsOpciones = []
        self.__itemsOpcionesVista = []
        self.__diccionarioClavesNuevo = {}
        self.__diccionarioClaves = {}
        self.__itemAnterior = "1"
        self.__nuevasClaves = True
        self.__numeroPreguntasAnterior = 0
        self.__desdeButtonClaves = True
        self.__archivoGuardado = True
        self.__directorioApp = ""
        self.__logoHojaRespuestasPDF = None
        self.__configuracion = None
        self.__archivoConfiguracion = "Configuracion/configuracion.xml"
        # self.__camaras = QMediaDevices.videoInputs()
        # Carga el archivo de diseño de la ventana
        if getattr(sys, 'frozen', False):
            # Ejecutable generado por PyInstaller
            direccionGui = os.path.dirname(sys.executable)
            direccionGui += '/_internal/Gui/'
        else:
            # Ejecución en modo de script (por ejemplo, 'python mi_app.py')
            direccionGui = os.path.dirname(os.path.abspath(__file__))

        self.__directorioGui = direccionGui

        archivoUI = os.path.join(direccionGui, 'disenoventana.ui')
        uic.loadUi(archivoUI, self)
        iconoVentana = QIcon(direccionGui + "/imagenes/logoStefy.png")
        self.setWindowIcon(iconoVentana)

        # Temporizador para controlar la captura
        self.temporizador = QTimer()

        self.stackedContenido.setCurrentIndex(0)
        self.labelTituloEncabezado.setText("Inicio")
        self.buttonNuevo.clicked.connect(self.buttonNuevoClicked)
        self.buttonCargar.clicked.connect(self.buttonCargarClicked)
        self.buttonGuardar.clicked.connect(self.buttonGuardarClicked)
        self.buttonClaves.clicked.connect(self.buttonClavesClicked)
        self.buttonAceptar.clicked.connect(self.buttonAceptarClicked)
        self.buttonCancelar.clicked.connect(self.buttonCancelarClicked)
        self.buttonCerrar.clicked.connect(self.buttonCerrarClicked)
        self.buttonEvaluar.clicked.connect(self.buttonEvaluarClicked)
        self.buttonHojaRespuestas.clicked.connect(self.buttonHojaRespuestasClicked)
        self.buttonAjustes.clicked.connect(self.buttonAjustesClicked)
        self.buttonAyuda.clicked.connect(self.buttonAyudaClicked)
        self.temporizador.timeout.connect(self.temporizadorTimeout)
        self.buttonLogo.clicked.connect(self.buttonLogoClicked)
        self.tamanoLabelCamara = self.labelCamara.size()

        self.__inicializarVentana()
        self.__hojaRespuestas = None
        self.__calificador = None

        self.show()

    def __inicializarVentana(self):
        if not os.path.exists("Configuracion"):
            os.makedirs("Configuracion")
            print("Directorio de configuracion creado")

        archivoConfiguracion = self.__archivoConfiguracion
        configuracion = Configuracion(archivoConfiguracion)
        archivoCorrecto = configuracion.abrir()
        while not archivoCorrecto:
            configuracion.crearEstructura()
            configuracion.guardar(archivoConfiguracion)
            archivoCorrecto = configuracion.abrir()
            print("Archivo de configuración creado")
        self.__configuracion = configuracion

        print(f"Umbral PGP: {configuracion.umbralColorPuntosGuiaPrincipales}")
        print(f"Umbral PGS: {configuracion.umbralColorPuntosGuiaSecundarios}")
        print(f"Umbral opción marcada: {configuracion.umbralColorOpcionMarcada}")

        # iconoVentana = QIcon(self.__directorioGui + "imagenes/logoStefy.png")
        # self.setWindowIcon(iconoVentana)

        self.buttonClaves.setEnabled(False)
        #self.buttonClaves.setCursor(Qt.PointingHandCursor)
        self.buttonClaves.setCursor(Qt.CursorShape.PointingHandCursor)
        self.buttonEvaluar.setEnabled(False)
        self.buttonEvaluar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonGuardar.setEnabled(False)
        self.buttonGuardar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonCargar.setEnabled(True)
        self.buttonCargar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonAceptar.setEnabled(False)
        self.buttonAceptar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonCancelar.setEnabled(False)
        self.buttonCancelar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonHojaRespuestas.setEnabled(False)
        self.buttonHojaRespuestas.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonAjustes.setEnabled(True)
        self.buttonAjustes.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonAyuda.setEnabled(True)
        self.buttonAyuda.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonCerrar.setCursor(Qt.CursorShape.PointingHandCursor)

        self.buttonNuevo.setCursor(Qt.CursorShape.PointingHandCursor)

        self.editNombreExamen.textChanged.connect(self.__editTextoCambiado)
        self.editMateria.textChanged.connect(self.__editTextoCambiado)
        self.editGrado.textChanged.connect(self.__editTextoCambiado)
        self.spinConjuntosCuestionarios.textChanged.connect(self.__editTextoCambiado)
        self.spinNumeroPreguntas.textChanged.connect(self.__editTextoCambiado)

        self.editCalificacionMinima.setValidator(QDoubleValidator(0, 100, 1, self))
        self.editCalificacionMinima.textChanged.connect(self.__editTextoCambiado)

        self.editCalificacionMaxima.textChanged.connect(self.__editTextoCambiado)
        self.editCalificacionMaxima.setValidator(QDoubleValidator(0, 100, 1, self.editCalificacionMaxima))

        self.editRangoMinimo.textChanged.connect(self.__editTextoCambiado)
        self.editRangoMinimo.setValidator(QDoubleValidator(0, 100, 1, self.editRangoMinimo))

        self.stackedContenido.setCurrentIndex(0)
        self.stackedContenido.currentChanged.connect(self.__stackedContenidoCurrentChanged)

        self.comboCamara.setVisible(False)
        self.labelPuertoCamara.setVisible(False)

        self.__limpiarWidget(self.frameItemsRespuesta.layout())
        self.__limpiarWidget(self.frameClavesRespuesta.layout())
        self.tamanoLabelCamara = self.labelCamara.size()

    # def __limpiarWidget(self, widget):
    #     layout = widget.layout()
    #     if layout is not None:
    #         while layout.count():
    #             item = layout.takeAt(0)
    #             widget = item.widget()
    #             if widget is not None:
    #                 widget.setParent(None)
    #             else:
    #                 self.__limpiarWidget(item.layout())
    #         widget.setLayout(None)

    def __limpiarWidget(self, layout):
        if layout is not None:
            while layout.count():
                hijo = layout.takeAt(0)
                if hijo.widget():
                    hijo.widget().deleteLater()


    def buttonNuevoClicked(self):
        if not self.__archivoGuardado:
            textoMensaje = "Los datos actuales aún no se han guardado. Si continúa se perderán. ¿Desea continuar?"
            # mensaje = QMessageBox()
            resultado = QMessageBox.question(self, "Nuevo archivo", textoMensaje,
                                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                                 QMessageBox.StandardButton.NoButton)
            # mensaje.setText("Los datos actuales aún no se han guardado. Si continúa se perderán. ¿Desea continuar?")
            # mensaje.setWindowTitle("Nuevo archivo")
            # mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            # mensaje.button(QMessageBox.Yes).setText('Sí')
            # mensaje.button(QMessageBox.No).setText('No')
            # resultado = mensaje.exec_()

            if resultado == QMessageBox.StandardButton.No:
                return
        archivo = "NuevoExamen.xml"
        self.labelTituloEncabezado.setText(archivo)
        # print(archivo)
        self.__archivoExamenXML = ArchivoExamenXML(archivo)
        self.__archivoExamenXML.nombreExamen = "Nuevo examen"
        self.__archivoExamenXML.crearEstructura()

        self.__mostrarDatosArchivo(archivo)
        self.stackedContenido.setCurrentIndex(1)
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.__archivoGuardado = False

    def buttonCargarClicked(self):
        nombreArchivo,_ = QFileDialog.getOpenFileName(None, "Seleccione un archivo XML", "", "Archivos XML (*.xml)")
        # Si el usuario no selecciono un archivo o dio en Cancelar
        if len(nombreArchivo) < 5:
            return

        self.__archivoExamenXML = ArchivoExamenXML(nombreArchivo)
        if not self.__archivoExamenXML.abrir():
            cajaMensajes = QMessageBox(self)
            cajaMensajes.setText(f"El archivo que intenta cargar presenta un error. {self.__archivoExamenXML.errorArchivo}")
            cajaMensajes.setIcon(QMessageBox.Information)
            cajaMensajes.show()
            return

        # print(nombreArchivo)
        archivo = os.path.basename(nombreArchivo)
        self.__mostrarDatosArchivo(archivo)
        self.buttonClaves.setEnabled(True)
        self.__archivoGuardado = True
        self.__estadoBotonesMenu(True, True, True, True, True)
        self.stackedContenido.setCurrentIndex(1)

    def buttonGuardarClicked(self):
        """Guarda los datos en un archivo"""
        nombreEventual = ""
        if self.__archivoExamenXML.nombreExamen == "Nuevo examen":
            nombreEventual = self.__archivoExamenXML.nombreExamen
        else:
            nombreEventual = self.__archivoExamenXML.nombre
        nombreArchivo, _ = QFileDialog.getSaveFileName(None, "Guardar como", f"{nombreEventual}", "Archivos XML (*.xml)")
        if nombreArchivo:
            try:
                self.__archivoExamenXML.guardar(nombreArchivo)
            except ValueError as error:
                mensajeBox = QMessageBox()
                mensajeBox.setIcon(QMessageBox.Warning)
                mensajeBox.setText(f"Se presentó un error al intentar guardar el archivo. {type(error).__name__}: {str(error)}")
                mensajeBox.setWindowTitle("Guardar archivo")
                mensajeBox.show()
                return
            self.__archivoGuardado = True

    def buttonClavesClicked(self):
        """Muestra el formulario de claves de respuesta"""
        numeroPreguntas = int(self.__archivoExamenXML.numeroPreguntas)
        if self.__numeroPreguntasAnterior != numeroPreguntas:
            self.__agregarItemsRespuestas(numeroPreguntas)

        k = self.comboNumeroCuestionario.count()
        h = int(self.__archivoExamenXML.conjuntosCuestionarios)
        # print(f"k = {k}")
        # print(f"h = {h}")
        if k < h:
            for i in range(k, h):
                self.__diccionarioClavesNuevo[str(i + 1)] = self.__archivoExamenXML.devolverRespuestas(str(i + 1))
                self.comboNumeroCuestionario.addItem(str(i + 1))

        if self.__nuevasClaves:
            #self.comboNumeroCuestionario.currentIndexChanged[str].connect(self.comboNumeroCuestionarioCurrentIndexChanged)
            self.comboNumeroCuestionario.currentIndexChanged.connect(
                self.comboNumeroCuestionarioCurrentIndexChanged)
            self.comboNumeroCuestionario.setCurrentIndex(0)
            self.__mostrarClavesRespuesta()

        self.stackedContenido.setCurrentIndex(2)
        self.__nuevasClaves = False
        self.__numeroPreguntasAnterior = numeroPreguntas
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.__desdeButtonClaves = True

    def buttonEvaluarClicked(self):
        """Muestra la cámara para capturar la hoja de respuestas"""
        self.editNumeroPreguntas.setText(self.__archivoExamenXML.numeroPreguntas)
        mapaPixeles = QPixmap(self.__directorioGui + "/iconos/visor_de_la_camara.svg")
        self.labelCamara.setPixmap(mapaPixeles)
        self.__limpiarCajasTexto()
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.__vistaHojaClavesRespuesta(int(self.__archivoExamenXML.numeroPreguntas))
        self.stackedContenido.setCurrentIndex(3)

    def buttonHojaRespuestasClicked(self):
        self.buttonAceptar.setText("Generar")
        self.buttonAceptar.setEnabled(True)
        self.buttonCancelar.setEnabled(True)
        self.labelTituloEncabezado.setText("Hoja de respuestas")
        # Cargar los datos de la hoja de respuestas
        self.__hojaRespuestasPDF = HojaRespuestasPDF("ArchivoPDF")
        self.editTituloEncabezado.setText(self.__hojaRespuestasPDF.nombreInstitucion)
        self.editTitulo2.setText(self.__hojaRespuestasPDF.nombreArea)
        self.editTitulo3.setText(self.__hojaRespuestasPDF.nombreTema)
        self.editTextoEncabezado.insertPlainText(self.__hojaRespuestasPDF.mensajeEncabezado)
        # self.editTextoEncabezado.setText(self.__hojaRespuestasPDF.mensajeEncabezado)
        self.editTituloDatos.setText(self.__hojaRespuestasPDF.tituloIdentificacion)
        self.editDatosNombre.setText(self.__hojaRespuestasPDF.textoNombres)
        self.editDatosCurso.setText(self.__hojaRespuestasPDF.textoGrado)
        self.editTextoDatos.setText(self.__hojaRespuestasPDF.tituloCodigo)
        self.editDatosCodigo.setText(self.__hojaRespuestasPDF.textoCodigo)
        self.editTituloCuestionario.setText(self.__hojaRespuestasPDF.tituloCuestionario)
        self.editCuestionarioID.setText(self.__hojaRespuestasPDF.textoCuestionario)
        self.editTituloRespuestas.setText(self.__hojaRespuestasPDF.tituloRespuestas)
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.stackedContenido.setCurrentIndex(4)

    def buttonAjustesClicked(self):
        ventanaAjustes = VentanaAjustes(self, self.__configuracion)
        ventanaAjustes.respuesta.connect(self.__ventanaAjustesRespuesta)
        ventanaAjustes.exec()
        # self.__configuracion.guardar()

    def buttonAyudaClicked(self):
        mensajeAcercade = QMessageBox()
        mapaPixeles = QPixmap(self.__directorioGui + "/iconos/acerca_de.svg")  # Replace with your image path
        mapaPixeles = mapaPixeles.scaled(200, 300)
        mensajeAcercade.setIconPixmap(mapaPixeles)
        mensajeAcercade.setWindowTitle("Acerca de...")
        mensajeAcercade.setText("Stefy, 0.2.0"
                                "\n\n© 2024 Pedro Vicente RM"
                                "\npedrovicenterosero@gmail.com")
        mensajeAcercade.setStandardButtons(QMessageBox.StandardButton.Ok)
        mensajeAcercade.setDefaultButton(QMessageBox.StandardButton.Ok)
        mensajeAcercade.exec()
        # print("Acerca de...")

    def __ventanaAjustesRespuesta(self, mensaje):
        print(f"Nuevo umbral {self.__configuracion.umbralColorOpcionMarcada}")
        self.__configuracion.actualizarValores()
        self.__configuracion.guardar(self.__archivoConfiguracion)

    def buttonAceptarClicked(self):
        if self.stackedContenido.currentIndex() == 1:
            self.__archivoExamenXML.nombreExamen = self.editNombreExamen.text()
            self.__archivoExamenXML.materia = self.editMateria.text()
            self.__archivoExamenXML.grado = self.editGrado.text()
            self.__archivoExamenXML.conjuntosCuestionarios = str(self.spinConjuntosCuestionarios.value())
            # print(f"Conjuntos cuestionarios ---->>> {self.__archivoExamenXML.conjuntosCuestionarios}")
            self.__archivoExamenXML.numeroPreguntas = str(self.spinNumeroPreguntas.value())
            self.__archivoExamenXML.calificacionMinima = self.editCalificacionMinima.text()
            self.__archivoExamenXML.calificacionMaxima = self.editCalificacionMaxima.text()
            self.__archivoExamenXML.rangoCalculoMinimo = self.editRangoMinimo.text()
            self.__archivoExamenXML.rangoCalculoMaximo = self.editRangoMaximo.text()
            self.__archivoExamenXML.actualizarValores()
            # self.__archivoExamenXML.crearEstructura()
            self.__estadoBotonesMenu(True, True, True, True, True)
            self.__cargarClavesRespuesta()
            # print(self.__archivoExamenXML.nombreExamen)
        elif self.stackedContenido.currentIndex() == 2:
            # Cargar al diccionario las claves que están en pantalla
            numeroCuestionario = self.comboNumeroCuestionario.currentText()
            self.__diccionarioClavesNuevo[numeroCuestionario] = self.__clavesRespuesta()

            # Cargar las claves de respuesta al archivoXML
            for i in range(int(self.__archivoExamenXML.conjuntosCuestionarios)):
                dic = self.__diccionarioClavesNuevo[str(i + 1)]
                # print("Diccionario existe")
                self.__archivoExamenXML.agregarRespuestas(str(i + 1), self.__diccionarioClavesNuevo[str(i + 1)])

            self.__archivoExamenXML.eliminarExcesoCuestionarios(int(self.__archivoExamenXML.conjuntosCuestionarios))
            self.__estadoBotonesMenu(True, True, True, True, True)
            self.stackedContenido.setCurrentIndex(1)
        elif self.stackedContenido.currentIndex() == 3: # Manejo de la captura con la cámara
            self.__iniciarCaptura()
        elif self.stackedContenido.currentIndex() == 4:
            self.__hojaRespuestasPDF = HojaRespuestasPDF()
            self.__hojaRespuestasPDF.nombreInstitucion = self.editTituloEncabezado.text()
            self.__hojaRespuestasPDF.nombreArea = self.editTitulo2.text()
            self.__hojaRespuestasPDF.nombreTema = self.editTitulo3.text()
            self.__hojaRespuestasPDF.mensajeEncabezado = self.editTextoEncabezado.toPlainText()
            self.__hojaRespuestasPDF.tituloIdentificacion = self.editTituloDatos.text()
            self.__hojaRespuestasPDF.textoNombres = self.editDatosNombre.text()
            self.__hojaRespuestasPDF.textoGrado = self.editDatosCurso.text()
            self.__hojaRespuestasPDF.tituloCodigo = self.editTextoDatos.text()
            self.__hojaRespuestasPDF.textoCodigo = self.editDatosCodigo.text()
            self.__hojaRespuestasPDF.tituloCuestionario = self.editTituloCuestionario.text()
            self.__hojaRespuestasPDF.textoCuestionario = self.editCuestionarioID.text()
            self.__hojaRespuestasPDF.archivoLogo = self.__logoHojaRespuestasPDF
            nombreArchivo, _ = QFileDialog.getSaveFileName(None, "Guardar como...",
                                                           f"HojaRespuetas_{self.__hojaRespuestasPDF.nombreTema}",
                                                           "Archivos PDF (*.pdf)")
            if nombreArchivo:
                self.__hojaRespuestasPDF.nombreArchivo = nombreArchivo
                self.__hojaRespuestasPDF.dibujar()
                self.__hojaRespuestasPDF.guardar()

        if self.stackedContenido.currentIndex() != 3:
            self.__archivoGuardado = False

    def buttonCancelarClicked(self):
        if self.stackedContenido.currentIndex() == 3:
            self.temporizador.stop()
            self.labelCamara.clear()
            mapaPixeles = QPixmap(self.__directorioApp + "/iconos/visor_de_la_camara.svg")
            self.labelCamara.setPixmap(mapaPixeles)
            self.stackedContenido.setCurrentIndex(1)
            self.__limpiarWidget(self.frameClavesRespuesta.layout())
            self.__itemsOpcionesVista.clear()
        else:
            self.__diccionarioClavesNuevo.clear()
            self.stackedContenido.setCurrentIndex(1)
            self.comboNumeroCuestionario.clear()
        self.__estadoBotonesMenu(True, True, True, True, True)

    def buttonCerrarClicked(self):
        self.close()

    def comboNumeroCuestionarioCurrentIndexChanged(self, indice):
        # print("comboNumeroCuestionarioCurrentIndexChanged...")
        if (indice < 0):
            return

        texto = str(indice + 1)
        # if not self.__desdeButtonClaves:
        self.__diccionarioClavesNuevo[self.__itemAnterior] = self.__clavesRespuesta()
        self.__mostrarClavesRespuesta(texto)
        self.__itemAnterior = str(texto)
        self.__desdeButtonClaves = False

    def temporizadorTimeout(self):
        """Realiza la captura de los cuadros de la cámara"""
        tamanoLabelCamara = self.labelCamara.size()
        #print(f"Tamaño antes de la captura - {tamanoLabelCamara}")
        if not self.__hojaRespuestas.capturada:
            frame = self.__hojaRespuestas.capturar()
            if self.__hojaRespuestas.exitoCaptura:
                qImagen = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
                # Convierte el objeto QImage a un QPixmap
                mapaPixeles = QPixmap.fromImage(qImagen)
                mapaPixeles = mapaPixeles.scaled(QSize(tamanoLabelCamara.width(), tamanoLabelCamara.height()),
                                                 Qt.AspectRatioMode.KeepAspectRatio)
                # Muestra el QPixmap en una QLabel
                self.labelCamara.setPixmap(mapaPixeles)
            else:
                self.labelCamara.setText(f"Error de captura en el puerto {self.__hojaRespuestas.puertoCamara}...")
        else:
            # print("Se capturó la hoja de respuestas")
            self.temporizador.stop()
            numeroPreguntas = int(self.__archivoExamenXML.numeroPreguntas)
            conjuntosCuestionarios = int(self.__archivoExamenXML.conjuntosCuestionarios)
            soluciones = {}
            for i in range(conjuntosCuestionarios):
                # print(i + 1)
                diccionarioSolucion = self.__archivoExamenXML.devolverRespuestas(str(i + 1))
                solucion = {}
                if len(diccionarioSolucion) != 0:
                    for j in range(numeroPreguntas):
                        letra = diccionarioSolucion[str(j + 1)]
                        # print(letra) # solucion["i + 1"] =
                        if letra == "A":
                            solucion[j + 1] = Respuesta.A
                        elif letra == "B":
                            solucion[j + 1] = Respuesta.B
                        elif letra == "C":
                            solucion[j + 1] = Respuesta.C
                        elif letra == "D":
                            solucion[j + 1] = Respuesta.D
                        else:
                            solucion[j + 1] = Respuesta.NS

                    soluciones[Cuestionario(i)] = solucion

            calificacionMaxima = float(self.editCalificacionMaxima.text())
            calificacionMinima = float(self.editCalificacionMinima.text())
            rangoMinimo = float(self.editRangoMinimo.text())
            self.__calificador = Evaluador(self.__hojaRespuestas, calificacion_maxima=calificacionMaxima, calificacion_minima=calificacionMinima, rango_minimo=rangoMinimo,numero_items=numeroPreguntas)
            self.__calificador.cuestionarioIndefinido.connect(self.__cuestionarioIndefinidoCalificador)
            self.__calificador.solucionarioIndefinido.connect(self.__calificadorSolucionarioIndefinido)
            self.__calificador.cuestionarioVarios.connect(self.__calificadorSolucionarioIndefinido)
            self.__calificador.solucion = soluciones
            self.__calificador.marca_correctas = True
            # print("Se va a evaluar...")
            imagen_formulario = self.__calificador.evaluar()
            nota = self.__calificador.calificacion
            numeroCuestionario = str(self.__calificador.numeroCuestionario.value + 1)
            self.editCuestionario.setText("C" + numeroCuestionario )
            self.editRespuestasCorrectas.setText(str(self.__calificador.respuestasCorrectas))
            self.editRespuestasIncorrectas.setText(str(self.__calificador.respuestasIncorrectas))
            self.editRespuestasNoMarcadas.setText(str(self.__calificador.noMarcadas))
            self.editCalificacion.setText(str(nota))

            qImagen = QImage(imagen_formulario.data, imagen_formulario.shape[1], imagen_formulario.shape[0], QImage.Format.Format_RGB888)

            # Convierte el objeto QImage a un QPixmap
            mapaPixeles = QPixmap.fromImage(qImagen)
            mapaPixeles = mapaPixeles.scaled(QSize(tamanoLabelCamara.width(), tamanoLabelCamara.height()), Qt.AspectRatioMode.KeepAspectRatio)

            # Muestra el QPixmap en una QLabel
            # self.labelCamara.setPixmap(mapaPixeles.scaled(self.labelCamara.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
            self.labelCamara.setPixmap(mapaPixeles)

            self.__mostrarHojaClavesRespuesta(numeroCuestionario)

    def __clavesRespuesta(self):
        claves = {}
        for itemOpciones in self.__itemsOpciones:
            claves[itemOpciones.nombre] = itemOpciones.seleccion

        return  claves

    def itemClicked(self):
        self.buttonNuevo.setEnabled(False)
        self.buttonCargar.setEnabled(False)
        self.buttonEvaluar.setEnabled(False)

    def buttonLogoClicked(self):
        logoHojaRespuestasPDF, _ = QFileDialog.getOpenFileName(None,
                                                             "Seleccione un archivo de imagen",
                                                             "",
                                                             "Archivos de imagen (*.jpeg *.jpg *.png *.svg)"
                                                             )
        if logoHojaRespuestasPDF:
            self.__logoHojaRespuestasPDF = logoHojaRespuestasPDF
            mapaPixeles = QPixmap(self.__logoHojaRespuestasPDF)
            ancho = self.labelLogo.width()
            alto = self.labelLogo.height()
            mapaPixeles = mapaPixeles.scaled(ancho, alto)
            self.labelLogo.setPixmap(mapaPixeles)
            print(f"Si hay logo PDF {logoHojaRespuestasPDF}")

    def __cargarClavesRespuesta(self):
        numeroCuestionarios = self.__archivoExamenXML.conjuntosCuestionarios

        for i in range(int(numeroCuestionarios)):
            self.__diccionarioClavesNuevo[str(i + 1)] = self.__archivoExamenXML.devolverRespuestas(str(i + 1))

    def __mostrarClavesRespuesta(self, texto = "1"):
        clavesActual = self.__diccionarioClavesNuevo[texto]

        if clavesActual:
            print("Claves actual")
            for clave, valor in clavesActual.items():
                # if valor is not None:
                self.__itemsOpciones[int(clave) - 1].seleccion = valor
        else:
            print("No hay respuestas")
            for itemOpciones in self.__itemsOpciones:
                itemOpciones.seleccion = None

    def __agregarItemsRespuestas(self, numeroPreguntas:int):
        # numeroPreguntas = int(self.__archivoExamenXML.numeroPreguntas)
        gruposItems = int((numeroPreguntas - (numeroPreguntas % 15)) / 15)
        if numeroPreguntas % 15 > 0:
            gruposItems += 1

        numeroItems = gruposItems * 15

        if self.__nuevasClaves:
            print("Mostrar items nuevos")
            self.frameItemsRespuesta.layout = QHBoxLayout(self.frameItemsRespuesta)
            # self.__agregarWidgetsItemsRespuestas(0, numeroItems)
            widget = None
            for i in range(numeroItems):
                if (i + 0) % 15 == 0:
                    widget = QWidget(self.frameItemsRespuesta)
                    # widget = QFrame()
                    widget.layout = QVBoxLayout(widget)
                    widget.setMaximumSize(QSize(300, 16777215))
                    widget.layout.setContentsMargins(12, 6, 12, 6)
                    widget.layout.setSpacing(6)
                    self.frameItemsRespuesta.layout.addWidget(widget)

                item = ItemRespuesta(widget, str(i + 1))
                item.activado = i < numeroPreguntas
                item.clicked.connect(self.itemClicked)  # Se clickea sobre un item de respuesta
                widget.layout.addWidget(item)
                self.__itemsOpciones.append(item)
        else:
            #print("No es nueva....")
            numeroPreguntasAnterior = self.__numeroPreguntasAnterior
            gruposItemsAnterior = int((numeroPreguntasAnterior - (numeroPreguntasAnterior % 15)) / 15)
            if numeroPreguntasAnterior % 15 > 0:
                gruposItemsAnterior += 1

            # numeroItems = gruposItems * 15
            numeroItemsAnterior = gruposItemsAnterior * 15

            if gruposItems > gruposItemsAnterior:
                #print("Si es mayor")
                if numeroItems > len(self.__itemsOpciones):
                    self.__agregarWidgetsItemsRespuestas(numeroItemsAnterior, numeroItems)
                for i in range(numeroPreguntasAnterior, numeroPreguntas):
                    item = self.__itemsOpciones[i]
                    item.activado = True
            elif gruposItems < gruposItemsAnterior:
                for i in range(numeroPreguntas, numeroItemsAnterior):
                    item = self.__itemsOpciones[i]
                    item.activado = False
            else:
                inicioRango = numeroPreguntasAnterior
                finalRango = numeroPreguntas

                if numeroPreguntas < numeroPreguntasAnterior:
                    inicioRango = numeroPreguntas
                    finalRango = numeroPreguntasAnterior

                for i in range(inicioRango, finalRango):
                    item = self.__itemsOpciones[i]
                    item.activado = (numeroPreguntas > numeroPreguntasAnterior)

    def __agregarWidgetsItemsRespuestas(self, inicio: int, final: int):
        widget = None
        for i in range(inicio, final):
            if (i + 0) % 15 == 0:
                widget = QWidget(self.frameItemsRespuesta)
                widget.layout = QVBoxLayout(widget)
                widget.setMaximumSize(QSize(300, 16777215))
                widget.layout.setContentsMargins(12, 6, 12, 6)
                widget.layout.setSpacing(6)
                self.frameItemsRespuesta.layout.addWidget(widget)

            item = ItemRespuesta(widget, str(i + 1))
            item.activado = i < int(self.__archivoExamenXML.numeroPreguntas)
            item.clicked.connect(self.itemClicked)  # Se clickea sobre un item de respuesta
            widget.layout.addWidget(item)
            self.__itemsOpciones.append(item)

    def __estadoBotonesMenu(self, estadoClaves:bool, estadoNuevo:bool, estadoCargar:bool, estadoEvaluar:bool, estadoGuardar:bool):
        self.buttonClaves.setEnabled(estadoClaves)
        self.buttonNuevo.setEnabled(estadoNuevo)
        self.buttonCargar.setEnabled(estadoCargar)
        self.buttonEvaluar.setEnabled(estadoEvaluar and self.__archivoExamenXML.existenClaves)
        self.buttonGuardar.setEnabled(estadoGuardar)
        self.buttonAceptar.setEnabled(not estadoNuevo)
        self.buttonCancelar.setEnabled(not estadoNuevo)
        self.buttonHojaRespuestas.setEnabled(estadoGuardar)
        self.buttonAjustes.setEnabled(estadoEvaluar)

    def __mostrarDatosArchivo(self, nombreArchivo:str):
        self.setWindowTitle(f"Stefy [{nombreArchivo}]")
        self.labelTituloEncabezado.setText(f"{self.__archivoExamenXML.nombreExamen}")
        self.editNombreExamen.setText(self.__archivoExamenXML.nombreExamen)
        self.editMateria.setText(self.__archivoExamenXML.materia)
        self.editGrado.setText(self.__archivoExamenXML.grado)
        self.spinConjuntosCuestionarios.setValue(int(self.__archivoExamenXML.conjuntosCuestionarios))
        self.spinNumeroPreguntas.setValue(int(self.__archivoExamenXML.numeroPreguntas))
        self.editNombreExamen.setFocus()
        self.editNombreExamen.selectAll()

    def __cuestionarioIndefinidoCalificador(self, mensaje):
        # print(f"Señal: {mensaje}")
        respuesta, aceptarPresionado = QInputDialog.getInt(self, 'Número de cuestionario', 'Numero de cuestionario C:',
                                                           1, 1, 4)

        if aceptarPresionado and respuesta is not None:
            self.__calificador.numeroCuestionario = Cuestionario(respuesta - 1)

    def __calificadorSolucionarioIndefinido(self, mensaje):
        cajaMensajes = QMessageBox(self)
        cajaMensajes.setText("El proceso de calificación no se pudo realizar: " + mensaje)
        cajaMensajes.setWindowTitle("Calificación del examen")
        cajaMensajes.addButton(QMessageBox.StandardButton.Ok)
        cajaMensajes.setIcon(QMessageBox.Icon.Information)
        cajaMensajes.show()

    def __editTextoCambiado(self):
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.editRangoMaximo.setText(self.editCalificacionMaxima.text())
        # self.buttonAceptar.setEnabled(True)
        # self.buttonCancelar.setEnabled(True)

    def __limpiarCajasTexto(self):
        self.editCuestionario.setText('')
        self.editRespuestasCorrectas.setText('')
        self.editRespuestasIncorrectas.setText('')
        self.editRespuestasNoMarcadas.setText('')
        self.editCalificacion.setText('-')

    def __iniciarCaptura(self):
        puertoCamara = self.comboCamara.currentData()
        # print(f"PUERTO CAMARA {puertoCamara}")
        self.__estadoBotonesMenu(False, False, False, False, False)
        self.__limpiarCajasTexto()
        self.__hojaRespuestas = HojaRespuestas(puertoCamara=puertoCamara)
        self.__hojaRespuestas.numeroItems = self.__archivoExamenXML.numeroPreguntas
        self.__hojaRespuestas.capturada = False
        self.__hojaRespuestas.umbralPGP = int(self.__configuracion.umbralColorPuntosGuiaPrincipales)
        self.__hojaRespuestas.umbralPGS = int(self.__configuracion.umbralColorPuntosGuiaSecundarios)
        self.__hojaRespuestas.umbralOpcionMarcada = int(self.__configuracion.umbralColorOpcionMarcada)
        self.temporizador.start(30)
        self.__hojaRespuestas.inicializar()

    def __stackedContenidoCurrentChanged(self, indice):
        iconoAceptar = QIcon(self.__directorioGui + "/iconos/editar.svg")
        textoAceptar = "Aceptar"
        self.comboCamara.setVisible(False)
        self.labelPuertoCamara.setVisible(False)
        if indice == 0:
            self.labelTituloEncabezado.setText("Inicio")
        elif indice == 1:
            self.labelTituloEncabezado.setText(f"{self.__archivoExamenXML.nombreExamen}")
        elif indice == 2:
            self.labelTituloEncabezado.setText(f"Claves de respuesta - {self.__archivoExamenXML.nombreExamen}")
        elif indice == 3:
            self.labelTituloEncabezado.setText(f"Calificación - {self.__archivoExamenXML.nombreExamen}")
            iconoAceptar = QIcon(self.__directorioGui + "/iconos/visor_de_la_camara.svg")
            textoAceptar = "Capturar"
            # camaras = self.__escanearCamaras()
            self.comboCamara.clear()
            # camaras = QMediaDevices.videoInputs()
            self.comboCamara.addItem("Camara posible", 2)
            #if len(self.__camaras) > 0:
            #    for camara in self.__camaras:
            #        nombreCamara = camara.description().split(':')[0].strip()
            #        self.comboCamara.addItem(nombreCamara, int(camara.id()))
            #else:
            #    self.buttonAceptar.setEnabled(False)

            self.labelPuertoCamara.setVisible(True)
            self.comboCamara.setVisible(True)
        elif indice == 4:
            iconoAceptar = QIcon(self.__directorioGui + "/iconos/archivo_pdf.svg")
            textoAceptar = "Generar"

        if iconoAceptar is not None:
            self.buttonAceptar.setIcon(iconoAceptar)
            self.buttonAceptar.setText(textoAceptar)

    def __escanearCamaras(cantidadPuertos=10):
        camarasConectadas = []
        cameras = QMediaDevices.videoInputs()
        for cameraDevice in cameras:
            camarasConectadas.append(int(cameraDevice.id()))
        return camarasConectadas

    def __vistaHojaClavesRespuesta(self, numeroPreguntas:int):
        gruposItems = int((numeroPreguntas - (numeroPreguntas % 15)) / 15)
        if numeroPreguntas % 15 > 0:
            gruposItems += 1

        numeroItems = gruposItems * 15

        if self.frameClavesRespuesta.layout() is None:
            QHBoxLayout(self.frameClavesRespuesta)
        # self.__agregarWidgetsItemsRespuestas(0, numeroItems)
        widget = None
        for i in range(numeroItems):
            if (i + 0) % 15 == 0:
                if i > 14:
                    print("Agregar separador...")
                    spacerHorizontal = QSpacerItem(10, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
                    self.frameClavesRespuesta.layout().addItem(spacerHorizontal)

                widget = QWidget(self.frameClavesRespuesta)
                # widget.layout = QVBoxLayout(widget)
                QVBoxLayout(widget)
                widget.setMaximumSize(QSize(150, 16777215))
                widget.layout().setContentsMargins(1, 2, 1, 2)
                widget.layout().setSpacing(1)
                self.frameClavesRespuesta.layout().addWidget(widget)
                # self.frameClavesRespuesta.addWidget(widget)

            item = ItemRespuesta(widget, str(i + 1), tamanoFuente=10, radio=10, asignable=False)
            item.activado = i < numeroPreguntas
            # item.clicked.connect(self.itemClicked)  # Se clickea sobre un item de respuesta
            widget.layout().addWidget(item)
            self.__itemsOpcionesVista.append(item)
            self.labelTituloHoja.setText("Hoja de respuestas")

    def __mostrarHojaClavesRespuesta(self, texto="1"):
        # clavesActual = self.__diccionarioClavesNuevo[texto]
        clavesActual = self.__archivoExamenXML.devolverRespuestas(texto)
        if clavesActual:
            print("Claves actual")
            for clave, valor in clavesActual.items():
                # if valor is not None:
                self.__itemsOpcionesVista[int(clave) - 1].seleccion = valor
                self.labelTituloHoja.setText("Hoja de respuestas C" + texto)
        else:
            print("No hay respuestas")
            for itemOpciones in self.__itemsOpcionesVista:
                itemOpciones.seleccion = None

            self.labelTituloHoja.setText("Hoja de respuestas")
