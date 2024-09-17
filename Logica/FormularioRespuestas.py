import cv2
import numpy as np
# import winsound
from ItemRespuesta import ItemRespuesta
from Util import Util
from Seleccion import *


class FormularioRespuestas():
    def __init__(self, opciones_cuestionarios=4, separacion_opciones_cuestionario=71, opciones_respuesta=4,
                 alto_ajustado=552, ancho_ajustado=418):
        self.__alto_ajustado = alto_ajustado
        self.__ancho_ajustado = ancho_ajustado
        self.__opciones_cuestionarios = opciones_cuestionarios
        self.__separacion_opciones_cuestionario = separacion_opciones_cuestionario
        self.__secciones = None
        self.__cuestionario = None
        self.__items_respuestas = None  # Carga todos los items de respuesta
        self.__opciones_respuesta = opciones_respuesta  # Número de opciones de respuesta
        self.__frame_original = None

        # self.respuestas = list()

    @property
    def frame_original(self):
        return self.__frame_original

    @property
    def items_respuestas(self):
        """Devuelve un listado con los items y sus respuestas marcadas"""
        return self.__items_respuestas

    @property
    def cuestionario(self):
        return self.__cuestionario

    def escanear(self, puerto_video=0):
        captura = cv2.VideoCapture(puerto_video)
        ancho_ajustado = self.__ancho_ajustado
        alto_ajustado = self.__alto_ajustado
        lado_contorno = 0
        # resolucion_ancho = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        # resolucion_alto = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        imagen_ajustada = None
        anchoFrame = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        altoFrame = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        while True:
            exito, frame = captura.read()
            if exito:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                frame_original = frame.copy()
                self.__frame_original = frame_original

                # Cuadros guia de captura
                colorGuia = (255, 165, 0)
                largo = 70
                cv2.rectangle(frame, (-1, -1), (largo, largo), color=colorGuia, thickness=1)
                cv2.rectangle(frame, (altoFrame - largo, -1), (altoFrame, largo), color=colorGuia,
                              thickness=1)
                cv2.rectangle(frame, (-1, anchoFrame - largo), (largo, anchoFrame), color=colorGuia,
                              thickness=1)
                cv2.rectangle(frame, (altoFrame - largo, anchoFrame - largo), (altoFrame, anchoFrame), color=colorGuia,
                              thickness=1)

                contornos_guia_principales = self.__contornos_guia_principales(frame)
                # cv2.imshow("Captura formulario", frame)

                if len(contornos_guia_principales) == 4:
                    # print("Puntos guia: 4")
                    longitud_promedio_contorno = Util.longitud_promedio_contornos(
                        contornos_guia_principales
                    )
                    lado_contorno = int(longitud_promedio_contorno / 4)
                    medio_lado = int(lado_contorno / 2)
                    centros = Util.centros_contornos(contornos_guia_principales)
                    centros = Util.ordenar_puntos(centros)
                    # print(centros)
                    puntos_guia_originales = [
                        (centros[0][0] - medio_lado, centros[0][1] - medio_lado),
                        (centros[1][0] + medio_lado, centros[1][1] - medio_lado),
                        (centros[2][0] - medio_lado, centros[2][1] + medio_lado),
                        (centros[3][0] + medio_lado, centros[3][1] + medio_lado),
                    ]
                    puntos_guia_originales = np.float32(puntos_guia_originales)
                    puntos_nuevos_ajustados = np.float32(
                        [
                            [0, 0],
                            [ancho_ajustado, 0],
                            [0, alto_ajustado],
                            [ancho_ajustado, alto_ajustado],
                        ]
                    )
                    matriz_transformacion = cv2.getPerspectiveTransform(
                        puntos_guia_originales, puntos_nuevos_ajustados
                    )
                    imagen_ajustada = cv2.warpPerspective(
                        frame_original, matriz_transformacion, (ancho_ajustado + 2, alto_ajustado + 2)
                    )

                    # cv2.imshow("Imagen ajustada", imagen_ajustada)
                    # Util.beep()
                    break
                cv2.imshow("Captura formulario", frame)
            if cv2.waitKey(1) == 27:
                break

        captura.release()
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        self.__segmentos_secciones(imagen_ajustada, lado_contorno)
        return imagen_ajustada

    def __segmentos_secciones(self, imagen_ajustada, lado_cuadro_guia):
        secciones = list()
        items_respuestas = list()
        # Segmento lateral izquierdo para establecer los puntos guia
        segmento_lateral = Util.recorte_imagen(
            imagen_ajustada, (0, 0), (lado_cuadro_guia, self.__alto_ajustado)
        )
        segmento_lateral = Util.eliminar_ruido(segmento_lateral)
        puntos_guia_secundarios = Util.puntos_guia_secundarios(
            segmento_lateral, area_minima=40
        )

        # Extraer el segmento correspondiente al nombre del estudiante
        punto_g0 = puntos_guia_secundarios[0]
        punto_g1 = puntos_guia_secundarios[1]
        segmento_nombre = Util.recorte_imagen(imagen_ajustada,
                                              (lado_cuadro_guia + 2, 0),
                                              (self.__ancho_ajustado - lado_cuadro_guia, punto_g1[1])
                                              )

        punto_g2 = puntos_guia_secundarios[2]
        segmento_cuestionario = Util.recorte_imagen(imagen_ajustada,
                                                    (lado_cuadro_guia + 2, punto_g1[1]),
                                                    (self.__ancho_ajustado - lado_cuadro_guia, punto_g2[1])
                                                    )
        # -------->
        puntoSegmento = (self.__ancho_ajustado, punto_g2[1] - punto_g1[1]-2)
        cv2.rectangle(segmento_cuestionario, (0, 0), puntoSegmento, (0, 0, 255), 1)
        # -------->

        separacion_h = self.__separacion_opciones_cuestionario

        segmento_item_cuestionario = Util.recorte_imagen(segmento_cuestionario,
                                                         (115, 20-8),
                                                         (155 + self.__opciones_cuestionarios * separacion_h, 42-6))
        # ---------->
        puntoSegmento = (self.__ancho_ajustado, 42)
        cv2.rectangle(segmento_item_cuestionario, (0, 0), puntoSegmento, (0, 50, 255), 1)
        # ---------->

        # item_cuestionario = ItemRespuesta(segmento_item_cuestionario,
        #                                   separacion_opciones=separacion_h,
        #                                   seccion=Seccion.Cuestionario)
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
        punto_g3 = puntos_guia_secundarios[3]
        punto_g4 = puntos_guia_secundarios[4]

        # Carga las respuestas de la primera seccion
        segmento_respuestas1 = Util.recorte_imagen(imagen_ajustada,
                                                   (lado_cuadro_guia + 2, punto_g3[1]),
                                                   (medio_ancho, punto_g4[1])
                                                   )
        separacion_h = 32
        separacion_v = 25
        for k in range(15):
            segmento_item_respuestas1 = Util.recorte_imagen(segmento_respuestas1,
                                                            (48, 12 + k * separacion_v),
                                                            (80 + self.__opciones_respuesta * separacion_h,
                                                             38 + k * separacion_v
                                                             )
                                                            )
            item_respuestas1 = ItemRespuesta(segmento_item_respuestas1, nombre=k + 1,
                                             numero_opciones=self.__opciones_respuesta,
                                             separacion_opciones=separacion_h)
            item_respuestas1.nombreItemOpcion = True
            item_respuestas1.dibujar_circulos_opciones()
            items_respuestas.append(item_respuestas1)
            # self.items_respuestas.append(item_respuestas1)
            # if item_respuestas1.unica_seleccion:
            #     print("{} - {}".format(item_respuestas1.numero_item, item_respuestas1.seleccionadas[0].nombre))
            # else:
            #     print("Mal")

        # Carga las respuestas de la segunda sección
        segmento_respuestas2 = Util.recorte_imagen(imagen_ajustada,
                                                   (medio_ancho, punto_g3[1]),
                                                   (self.__ancho_ajustado - lado_cuadro_guia, punto_g4[1])
                                                   )
        for k in range(15):
            segmento_item_respuestas2 = Util.recorte_imagen(segmento_respuestas2,
                                                            (48, 12 + k * separacion_v),
                                                            (80 + self.__opciones_respuesta * separacion_h,
                                                             38 + k * separacion_v
                                                             )
                                                            )
            item_respuestas2 = ItemRespuesta(segmento_item_respuestas2,
                                             nombre=k + 16,
                                             numero_opciones=self.__opciones_respuesta,
                                             separacion_opciones=separacion_h)
            item_respuestas2.mostrarNombreItemOpcion = True
            item_respuestas2.dibujar_circulos_opciones()
            items_respuestas.append(item_respuestas2)
            # self.items_respuestas.append(item_respuestas2)

        self.__items_respuestas = items_respuestas
        # print("Items = {}".format(len(self.items_respuestas)))

        secciones.append(segmento_nombre)
        secciones.append(segmento_respuestas1)
        secciones.append(segmento_respuestas2)
        secciones.append(segmento_cuestionario)
        # cv2.imshow("Respuestas 1", segmento_respuestas1)
        # cv2.imshow("Respuestas 2", segmento_respuestas2)
        self.secciones = secciones

    def __contornos_guia_principales(self, imagen, area_minima=200, area_maxima=400, porcentaje_epsilon=0.02):
        """
        Detecta los cuadros guia del formulario de respuestas
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        gray = self.__limpiar_cuadros_guia(gray)
        # Aplicar filtro bilateral para reducir el ruido
        smooth = cv2.bilateralFilter(gray, 11, 17, 20)
        # cv2.imshow("Suave", smooth)
        imgBlur = cv2.GaussianBlur(smooth, (5, 5), 1)
        # imgBlur = eliminar_ruido(imgBlur)
        # cv2.imshow("Imagen smooth", smooth)
        _, umbral = cv2.threshold(imgBlur, 60, 255, cv2.THRESH_BINARY_INV)

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

        # contornos_4 = None
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
        # selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        # Aplicar la operación de cierre
        imagen_limpia = cv2.morphologyEx(imagen_binaria, cv2.MORPH_CLOSE, selem)

        return imagen_limpia
