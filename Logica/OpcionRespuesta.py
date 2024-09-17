import cv2
from Logica.Seleccion import *
import numpy as np


class OpcionRespuesta():
    def __init__(self, segmento_opcion, umbralColor=127):
        self.__real = True  # Esta opción se detectó en el formulario
        self.__nombre = None
        self.__umbralColor = umbralColor
        self.__intensidadColor = 255
        if segmento_opcion is not None:
            self.__segmento = segmento_opcion
            self.__circulo = self.__circulo_opcion()
            self.__estado = self.__estado()
        self.__mostrar_texto = False

    @property
    def segmento(self):
        return self.__segmento

    @property
    def circulo(self):
        return self.__circulo

    @property
    def estado(self):
        return self.__estado

    @property
    def real(self):
        """Devuelve True si la opcion se encontró realmente en el formulario físico"""
        return self.__real

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # if not (isinstance(valor, Respuesta) or isinstance(valor, Cuestionario)):
        #     raise TypeError("El valor asignado debe ser de tipo Respuesta o Cuestionario")
        self.__nombre = valor
    @property
    def mostrar_texto(self):
        return self.__mostrar_texto

    @mostrar_texto.setter
    def mostrar_texto(self, valor):
        self.__mostrar_texto = valor

    @property
    def umbralColor(self):
        return self.__umbralColor

    # @umbralColor.setter
    # def umbralColor(self, valor):
    #     self.__umbralColor = valor
    @property
    def intensidadColor(self):
        return self.__intensidadColor

    def dibujar_circulo_opcion(self, color=(0, 255, 0), texto=''):
        cx, cy, radio = self.circulo
        cv2.circle(self.segmento, (cx, cy), radio, color, 2)
        if self.__mostrar_texto and len(texto) > 0:
            posicion = (cx - 2 * radio // 3, cy + radio // 3)
            fuente = cv2.FONT_HERSHEY_COMPLEX
            escala = 0.4
            color = (255, 255, 255)
            grosor = 1
            cv2.putText(self.segmento, texto, posicion, fuente, escala, color, grosor, cv2.LINE_AA)

    def __estado(self):
        if self.__opcion_marcada(umbral=self.__umbralColor):
            return Seleccion.Seleccionado
        else:
            return Seleccion.Deseleccionado

    def __circulo_opcion(self, min_radio=8, max_radio=10, umbral_negro=150):
        '''Devuelve el circulo que corresponde a la opción de respuesta'''
        if self.segmento is None:
            print("Error: Segmento no definido")

        # Binarizar la imagen para eliminar los grises
        imagen_gris = cv2.cvtColor(self.segmento, cv2.COLOR_BGR2GRAY)
        _, imagen_binarizada = cv2.threshold(
            imagen_gris, umbral_negro, 255, cv2.THRESH_BINARY
        )
        # Aplicar desenfoque gaussiano para reducir el ruido
        gray = cv2.GaussianBlur(imagen_binarizada, (5, 5), 0)

        # Usar la Transformada de Hough para detectar círculos
        circulos_encontrados = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=max_radio,
            param1=50,
            param2=20,
            minRadius=min_radio,
            maxRadius=max_radio,
        )

        circulo = None
        if circulos_encontrados is not None:
            circulos_encontrados = np.round(circulos_encontrados[0, :]).astype("int")
        else:
            circulos_encontrados = []

        if len(circulos_encontrados) != 1:
            dimensiones = self.segmento.shape
            # print("Dimensiones: {}".format(dimensiones))
            cx = int(dimensiones[1] / 2)
            cy = int(dimensiones[0] / 2)
            circulo = (cx, cy, int((max_radio + min_radio) / 2))
            self.__real = False  # Este círculo no se detectó en el formulario
        else:
            circulo = circulos_encontrados[0]

        return circulo

    def __opcion_marcada(self, umbral=127): # umbral=128 Mayor valor cuando hay exceso de luz, y viceversa
        cx, cy, radio = self.circulo
        centro = (cx, cy)
        # Convierte la imagen a escala de grises
        imagen_gris = cv2.cvtColor(self.segmento, cv2.COLOR_BGR2GRAY)
        imagen_gris = self.__limpiar_circulo_opcion(imagen_gris, umbral=umbral)
        # cv2.imshow("imagen gris", imagen_gris)
        # Crea una máscara circular para los píxeles dentro del círculo
        mascara = np.zeros(imagen_gris.shape, dtype=np.uint8)
        cv2.circle(mascara, centro, radio, 255, thickness=-1)

        # Calcula el promedio de color dentro del círculo
        promedio_color = np.mean(imagen_gris[np.where(mascara == 255)]) #mascara == 255
        self.__intensidadColor = promedio_color # se devuelve para comparar cuando hay varias opciones marcadas
        # print(f"Desde opcion: UmbralColor = {umbral}")
        # Compara el promedio de color con el umbral
        if promedio_color < umbral:
            # cv2.imshow(f"mascara-{promedio_color}", imagen_gris)
            return True
        else:
            return False

    def __limpiar_circulo_opcion(self, imagen, umbral=127, maximo_valor=255):
        # Aplicar umbral para obtener una imagen binaria
        _, imagen_binaria = cv2.threshold(imagen, umbral, maximo_valor, cv2.THRESH_BINARY)
        # Definir el elemento estructurante para la operación de cierre
        # En este caso es un círculo de radio 5
        selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        # Aplicar la operación de cierre
        imagen_limpia = cv2.morphologyEx(imagen_binaria, cv2.MORPH_CLOSE, selem)

        return imagen_limpia

