import cv2

import numpy as np
from Logica.ItemRespuesta import ItemRespuesta
from Logica.Util import Util
from Logica.Seleccion import *

class HojaRespuestas():
    def __init__(self, opciones_cuestionarios=4, separacion_opciones_cuestionario=30, opciones_respuesta=4,
                 alto_ajustado=620, ancho_ajustado=390, puertoCamara=0):
        self.__alto_ajustado = alto_ajustado
        self.__ancho_ajustado = ancho_ajustado
        self.__opciones_cuestionarios = opciones_cuestionarios
        self.__separacion_opciones_cuestionario = separacion_opciones_cuestionario
        self.__secciones = None
        self.__cuestionario = None
        self.__items_respuestas = None  # Carga todos los items de respuesta
        self.__numeroItems = 30
        self.__opciones_respuesta = opciones_respuesta  # Número de opciones de respuesta
        self.__frame_original = None
        self.__puertoCamara = puertoCamara
        self.__anchoFrame = 0
        self.__altoFrame = 0
        self.__captura = None
        self.__capturada = False
        self.__imagenHoja = None
        self.__exitoCaptura = False
        self.__umbralPGP = 60 # Umbral de color para los puntos guias principales
        self.__umbralPGS = 60
        self.__umbralOpcionMarcada = 127

        # self.__inicializar()
        # self.respuestas = list()

    @property
    def frame_original(self):
        return self.__frame_original

    @property
    def items_respuestas(self):
        """Devuelve un listado con los items y sus respuestas marcadas"""
        return self.__items_respuestas

    @property
    def numeroItems(self):
        """Establece el numero de items de respuesta validos que componenen la hoja de respuestas."""
        return self.__numeroItems

    @numeroItems.setter
    def numeroItems(self, valor):
        self.__numeroItems = valor

    @property
    def cuestionario(self):
        return self.__cuestionario

    @property
    def capturada(self):
        return self.__capturada

    @capturada.setter
    def capturada(self, valor):
        self.__capturada = valor

    @property
    def imagenHoja(self):
        return self.__imagenHoja

    @property
    def exitoCaptura(self):
        return self.__exitoCaptura

    @property
    def puertoCamara(self):
        return self.__puertoCamara

    @property
    def umbralPGP(self):
        return self.__umbralPGP

    @umbralPGP.setter
    def umbralPGP(self, valor):
        self.__umbralPGP = valor

    @property
    def umbralPGS(self):
        return self.__umbralPGS

    @umbralPGS.setter
    def umbralPGS(self, valor):
        self.__umbralPGS = valor

    @property
    def umbralOpcionMarcada(self):
        return self.__umbralOpcionMarcada

    @umbralOpcionMarcada.setter
    def umbralOpcionMarcada(self, valor):
        self.__umbralOpcionMarcada = valor

    def inicializar(self):
        self.__captura = cv2.VideoCapture(self.__puertoCamara)
        # self.__captura.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # 0.25 desactiva la exposición automática
        # print("Después de inicializar cámara...")
        # anchoAjustado = self.__ancho_ajustado
        # altoAjustado = self.__alto_ajustado
        self.__anchoFrame = int(self.__captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__altoFrame = int(self.__captura.get(cv2.CAP_PROP_FRAME_WIDTH))

    def capturar(self):
        # Captura un cuadro desde la cámara
        exito, frame = self.__captura.read()
        self.__exitoCaptura = exito
        if exito:
            # Hace una rotación de 90º sobre el cuadro capturado
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            ancho_cuadro = frame.shape[1]

            # Recortar una franja vertical
            recorte_cuadro = 20 #Ancho de la franja que se va a recortar
            frame = frame[:, recorte_cuadro:ancho_cuadro - recorte_cuadro]
            ancho_cuadro -= 2 * recorte_cuadro
            # Saca una copia del cuadro original para ser enviado al video del usuario
            frame_original = frame.copy() # Imagen que se envía permanentemente hasta lograr la captura
            self.__frame_original = frame_original
            # Cuadros guia de captura
            colorGuia = (255, 165, 0)
            largo = 60 # Dimensiones del cuadro guía mostrado en la captura
            guiasCaptura = list()
            # Sensor superior izquierdo
            cv2.rectangle(frame, (0, 0), (largo, largo), color=colorGuia, thickness=1)
            guiasCaptura.append(Util.recorte_imagen(frame, (0, 0), (largo, largo)))
            # Sensor superior derecho
            cv2.rectangle(frame, (ancho_cuadro - largo, 0), (ancho_cuadro - 1, largo), color=colorGuia,
                          thickness=1)
            guiasCaptura.append(Util.recorte_imagen(frame, (ancho_cuadro - largo, 0), (ancho_cuadro, largo)))
            # Sensor inferior izquierdo
            cv2.rectangle(frame, (0, self.__altoFrame - largo), (largo - 1, self.__altoFrame - 1), color=colorGuia,
                          thickness=1)
            guiasCaptura.append(Util.recorte_imagen(frame, (0, self.__altoFrame - largo), (largo, self.__altoFrame + 1)))
            # Sensor inferior derecho
            cv2.rectangle(frame, (ancho_cuadro - largo, self.__altoFrame - largo - 1), (ancho_cuadro - 1, self.__altoFrame - 1), color=colorGuia,
                          thickness=1)
            guiasCaptura.append(Util.recorte_imagen(frame, (ancho_cuadro - largo, self.__altoFrame - largo), (ancho_cuadro, self.__altoFrame + 1)))
            # Se buscan lo cuadros guìa negros sobre la hoja de respuestas
            contornos_guia_principales = list()
            for guiaCaptura in guiasCaptura:
                contornoGuia = self.__contornos_guia_principales(guiaCaptura, porcentaje_epsilon=0.03)
                if len(contornoGuia) == 1:
                    contornos_guia_principales.append(contornoGuia[0])
                else:
                    break
            # Se encuadra la imagen de las respuestas
            imagenHoja = None
            lado_contorno = 1
            if len(contornos_guia_principales) == 4:
                # Calcula el perímetro del cuadro guía encontrado
                longitud_promedio_contorno = Util.longitud_promedio_contornos(
                    contornos_guia_principales
                )
                lado_contorno = int(longitud_promedio_contorno / 4)
                medio_lado = int(lado_contorno / 2)
                centros = Util.centros_contornos(contornos_guia_principales)

                # Se fijan las coordenadas de las esquinas externas de los puntos guia
                # Esto asegura que los puntos guía queden dentro de la imagen recortada
                puntos_guia_originales = [
                    (centros[0][0] - medio_lado, centros[0][1] - medio_lado),
                    (ancho_cuadro - largo + centros[1][0] + medio_lado, centros[1][1] - medio_lado),
                    (centros[2][0] - medio_lado, self.__altoFrame - largo + centros[2][1] + medio_lado),
                    (ancho_cuadro - largo + centros[3][0] + medio_lado,
                     self.__altoFrame - largo + centros[3][1] + medio_lado),
                ]

                # print(f"Puntos guia originales: {puntos_guia_originales}")
                # print(f"Ancho hoja capturada: {puntos_guia_originales[0][0] - puntos_guia_originales[1][0]}")
                # print(f"Ancho hoja capturada: {puntos_guia_originales[0][1] - puntos_guia_originales[2][1]}")
                puntos_guia_originales = np.float32(puntos_guia_originales)
                puntos_nuevos_ajustados = np.float32(
                    [
                        [0, 0],
                        [self.__ancho_ajustado, 0],
                        [0, self.__alto_ajustado],
                        [self.__ancho_ajustado, self.__alto_ajustado],
                    ]
                )

                matriz_transformacion = cv2.getPerspectiveTransform(
                    puntos_guia_originales, puntos_nuevos_ajustados
                )
                # Se encuadra la imagen recortandola de tal manera que los puntos guía queden dentro
                imagenHoja = cv2.warpPerspective(
                    frame_original, matriz_transformacion, (self.__ancho_ajustado + 2, self.__alto_ajustado + 2)
                )
                self.__imagenHoja = imagenHoja # Imagen que se utiliza para mostrarla congelada y escanear las respuestas
                self.__capturada = True
                # cv2.imshow("Captura", imagenHoja)
            # print("IMAGEN CAPTURADA")
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if self.__capturada:
                self.__segmentos_secciones(imagenHoja, lado_contorno)
                self.__captura.release()
            return frameRGB

    def __segmentos_secciones(self, imagen_ajustada, lado_cuadro_guia):
        puntos_guia_base = [(6, 7), (3, 110), (3, 165), (3, 230), (6, 610)]
        secciones = list()
        items_respuestas = list()
        # Segmento lateral izquierdo para establecer los puntos guia
        segmento_lateral = Util.recorte_imagen(
            imagen_ajustada, (0, 0), (lado_cuadro_guia, self.__alto_ajustado)
        )
        segmento_lateral = Util.eliminar_ruido(segmento_lateral)
        puntos_guia_secundarios = Util.puntos_guia_secundarios(
            segmento_lateral, area_minima=40, umbral=self.__umbralPGS
        )
        # print(f"Puntos guia secundarios: {puntos_guia_secundarios}")
        # Extraer el segmento correspondiente al nombre del estudiante
        # punto_g0 = puntos_guia_secundarios[0]
        punto_g1 = puntos_guia_secundarios[1]
        punto_g2 = puntos_guia_secundarios[2]
        segmento_nombre = Util.recorte_imagen(imagen_ajustada,
                                              (punto_g1[0] + lado_cuadro_guia, punto_g1[1]),
                                              (self.__ancho_ajustado - lado_cuadro_guia, punto_g2[1] - lado_cuadro_guia)
                                              )
        # -------->
        # cv2.imshow("Segmento NOMBRE", segmento_nombre)
        # -------->

        punto_g3 = puntos_guia_secundarios[3]
        segmento_cuestionario = Util.recorte_imagen(imagen_ajustada,
                                                    (lado_cuadro_guia + 2, punto_g2[1] + lado_cuadro_guia - 5),
                                                    (self.__ancho_ajustado - lado_cuadro_guia, punto_g3[1] - lado_cuadro_guia)
                                                    )
        # -------->
        # puntoSegmento = (self.__ancho_ajustado - lado_cuadro_guia - 20, punto_g3[1] - punto_g2[1] - 2 * lado_cuadro_guia)
        # cv2.rectangle(segmento_cuestionario, (0, 0), puntoSegmento, (0, 0, 255), 1)
        # cv2.imshow("Segmento CUESTIONARIO", segmento_cuestionario)
        # -------->

        separacion_h = self.__separacion_opciones_cuestionario

        segmento_item_cuestionario = Util.recorte_imagen(segmento_cuestionario,
                                                         (156, 12),
                                                         (156 + self.__opciones_cuestionarios * (separacion_h), 34))
        # ----->
        # puntoSegmento = (200 + self.__opciones_cuestionarios * separacion_h, 36)
        # cv2.imshow("Opciones cuestionario", segmento_item_cuestionario)
        # ----->
        item_cuestionario = ItemRespuesta(segmento_item_cuestionario, nombre=0,
                                          numero_opciones=4,
                                          separacion_opciones=separacion_h,
                                          seccion=Seccion.Cuestionario)
        item_cuestionario.dibujar_circulos_opciones(todas=False)

        '''------------- Prueba de salidas -----------------'''
        # if item_cuestionario.unica_seleccion:
        #     print(item_cuestionario.nombre_respuesta)
        # else:
        #     if len(item_cuestionario.seleccionadas) < 1:
        #         print("No seleccionó un cuestionario")
        #     else:
        #         seleccionadas = ""
        #         for opcion in item_cuestionario.seleccionadas:
        #             seleccionadas += opcion.nombre + " "
        #         print("Selecciono más de una respuesta: {}".format(seleccionadas))

        '''--------------------------------------------------'''
        # if item_cuestionario.unica_seleccion:
        self.__cuestionario = item_cuestionario
        # else:

        medio_ancho = int(self.__ancho_ajustado / 2)

        punto_g4 = puntos_guia_secundarios[4]

        # Carga las respuestas de la primera seccion
        segmento_respuestas1 = Util.recorte_imagen(imagen_ajustada,
                                                   (lado_cuadro_guia + 2, punto_g3[1]),
                                                   (medio_ancho, punto_g4[1])
                                                   )
        # -------->
        # puntoSegmento = (self.__ancho_ajustado - lado_cuadro_guia - 20, punto_g4[1] - punto_g3[1])
        # cv2.rectangle(segmento_respuestas1, (0, 0), puntoSegmento, (0, 0, 255), 1)
        # cv2.imshow("Segmento RESPUESTAS 1", segmento_respuestas1)
        # -------->
        separacion_h = 30
        separacion_v = 24
        punto_inicio_h = 42 # Fija la coordenada h desde la cual se recorta el segmento util
        numeroRespuestas = int(self.__numeroItems) #Controla el numero de items que se deben cargar

        for k in range(15):
            numeroRespuestas -= 1
            if (numeroRespuestas < 0):
                break
            segmento_item_respuestas1 = Util.recorte_imagen(segmento_respuestas1,
                                                            (punto_inicio_h, 20 + k * separacion_v),
                                                            (punto_inicio_h + self.__opciones_respuesta * separacion_h,
                                                             20 + (k + 1) * separacion_v
                                                             )
                                                            )
            # -------->
            # puntoSegmento = (40 + self.__opciones_respuesta * separacion_h - 10, 28 + k * separacion_v)
            # cv2.rectangle(segmento_item_respuestas1, (0, 0), puntoSegmento, (0, 0, 255), 1)
            # cv2.imshow(f"Item {k}", segmento_item_respuestas1)
            # -------->

            item_respuestas1 = ItemRespuesta(segmento_item_respuestas1, nombre=k + 1,
                                             numero_opciones=self.__opciones_respuesta,
                                             separacion_opciones=separacion_h,
                                             umbralOpcionMarcada=self.__umbralOpcionMarcada)
            item_respuestas1.mostrarNombreItemOpcion = True
            # item_respuestas1.umbralOpcionMarcada = self.__umbralOpcionMarcada
            item_respuestas1.dibujar_circulos_opciones()
            items_respuestas.append(item_respuestas1)

        # Carga las respuestas de la segunda sección
        segmento_respuestas2 = Util.recorte_imagen(imagen_ajustada,
                                                   (medio_ancho, punto_g3[1]),
                                                   (self.__ancho_ajustado - lado_cuadro_guia, punto_g4[1])
                                                   )
        # ------>
        # cv2.imshow("Segmento RESPUESTAS 2", segmento_respuestas2)
        # ------>

        for k in range(15):
            numeroRespuestas -= 1
            if (numeroRespuestas < 0):
                break

            segmento_item_respuestas2 = Util.recorte_imagen(segmento_respuestas2,
                                                            (punto_inicio_h, 20 + k * separacion_v),
                                                            (punto_inicio_h + self.__opciones_respuesta * separacion_h,
                                                             20 + (k + 1) * separacion_v
                                                             )
                                                            )
            item_respuestas2 = ItemRespuesta(segmento_item_respuestas2,
                                             nombre=k + 16,
                                             numero_opciones=self.__opciones_respuesta,
                                             separacion_opciones=separacion_h,
                                             umbralOpcionMarcada=self.__umbralOpcionMarcada)
            item_respuestas2.mostrarNombreItemOpcion = True
            # item_respuestas2.umbralOpcionMarcada = self.__umbralOpcionMarcada
            item_respuestas2.dibujar_circulos_opciones()
            items_respuestas.append(item_respuestas2)

        self.__items_respuestas = items_respuestas
        secciones.append(segmento_nombre)
        secciones.append(segmento_respuestas1)
        secciones.append(segmento_respuestas2)
        secciones.append(segmento_cuestionario)
        self.secciones = secciones

    def __contornos_guia_principales(self, imagen, area_minima=50, area_maxima=300, porcentaje_epsilon=0.02):
        """
        Detecta los cuadros guia del formulario de respuestas
        """
        umbralColor = self.__umbralPGP
        # Convertir a escala de grises
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        gray = self.__limpiar_cuadros_guia(gray)
        # cv2.imshow("Gray", gray)
        # Aplicar filtro bilateral para reducir el ruido
        smooth = cv2.bilateralFilter(gray, 11, 17, 20)
        # cv2.imshow("Suave", smooth)
        imgBlur = cv2.GaussianBlur(smooth, (5, 5), 1)
        # imgBlur = eliminar_ruido(imgBlur)
        # cv2.imshow("Imagen smooth", smooth)
        _, umbral = cv2.threshold(imgBlur, umbralColor, 255, cv2.THRESH_BINARY_INV)

        # cv2.imshow("Imagen umbral", umbral)
        # Aplicar la función Canny para detectar los bordes en la imagen
        edged = cv2.Canny(umbral, 10, 70)
        # cv2.imshow("Canny", edged)
        # Encontrar contornos
        contornos, _ = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filtrar contornos por área (esto puede variar dependiendo del tamaño de la hoja en la imagen)
        lista_contornos_guia = list()

        for contorno in contornos:
            epsilon = porcentaje_epsilon * cv2.arcLength(contorno, True)
            approx = cv2.approxPolyDP(contorno, epsilon, True)
            if len(approx) == 4:
                areaContorno = cv2.contourArea(contorno)

                if area_minima < areaContorno < area_maxima:
                    # Dibujar contornos
                    cv2.drawContours(imagen, [approx], 0, (0, 255, 0), 1)
                    # Hallar los centros de cada contorno
                    centro_con = Util.centro_contorno(contorno)
                    centro_con_x = centro_con[0]
                    centro_con_y = centro_con[1]
                    # Valida que el contorno que se va a agregar a la lista sea único
                    contorno_unico = True
                    for c in lista_contornos_guia:
                        centro_c = Util.centro_contorno(c)
                        centro_c_x = centro_c[0]
                        centro_c_y = centro_c[1]

                        if (
                                abs(centro_c_x - centro_con_x) < 100
                                and abs(centro_c_y - centro_con_y) < 100
                        ):
                            contorno_unico = False
                            break

                    if contorno_unico:
                        lista_contornos_guia.append(contorno)
        return lista_contornos_guia

    def __limpiar_cuadros_guia(self, imagen):
        # Aplicar umbral para obtener una imagen binaria
        _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)

        # Definir el elemento estructurante para la operación de cierre
        # En este caso es un círculo de radio 5
        selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        # Aplicar la operación de cierre
        imagen_limpia = cv2.morphologyEx(imagen_binaria, cv2.MORPH_CLOSE, selem)

        return imagen_limpia
