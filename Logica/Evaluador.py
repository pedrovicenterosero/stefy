import cv2
from blinker import Signal
from Logica.HojaRespuestas import HojaRespuestas
from Logica.Seleccion import *


class Evaluador:
    cuestionarioIndefinido = Signal()
    cuestionarioVarios = Signal()
    solucionarioIndefinido = Signal()

    def __init__(self, formulario=HojaRespuestas(),
                 calificacion_maxima=5,
                 calificacion_minima=1,
                 rango_minimo=0,
                 numero_items=20):
        self.__formulario = formulario
        self.__solucion = dict()
        self.__calificacion_maxima = calificacion_maxima
        self.__calificacion_minima = calificacion_minima
        self.__rango_minimo = rango_minimo
        self.__numero_items = numero_items
        self.__calificacion = 0
        self.__marca_correctas = False
        self.__respuestasCorrectas = 0
        self.__respuestasIncorrectas = 0
        self.__numeroCuestionario = Respuesta.NS
        self.__noMarcadas = 0

    @property
    def solucion(self):
        return self.__solucion

    @solucion.setter
    def solucion(self, valor):
        self.__solucion = valor

    @property
    def calificacion(self):
        return self.__calificacion

    @property
    def marca_correctas(self):
        return self.__marca_correctas

    @marca_correctas.setter
    def marca_correctas(self, valor):
        self.__marca_correctas = valor
    @property
    def respuestasCorrectas(self):
        return self.__respuestasCorrectas

    @property
    def respuestasIncorrectas(self):
        return self.__respuestasIncorrectas

    @property
    def noMarcadas(self):
        return self.__noMarcadas
    @property
    def numeroCuestionario(self):
        return self.__numeroCuestionario

    @numeroCuestionario.setter
    def numeroCuestionario(self, valor):
        self.__numeroCuestionario = valor

    def evaluar(self, respuesta=None):
        imagen_formulario = self.__formulario.imagenHoja
        # print(f"opcion cuestionario ------------------->")
        item_cuestionario = self.__formulario.cuestionario
        # print(f"------->> Respuesta = {item_cuestionario.respuesta}")
        opcion_cuestionario = item_cuestionario.respuesta.nombre
        self.__numeroCuestionario = opcion_cuestionario

        if opcion_cuestionario == Respuesta.NS:
            # Emite una señal
            self.cuestionarioIndefinido.send("El número de cuestionario no se pudo identificar.")
            opcion_cuestionario = self.__numeroCuestionario
        suma = 0
        numero_incorrectas = 0
        numero_correctas = 0
        noMarcadas = 0
        if opcion_cuestionario == Respuesta.MS:
            # print("Se seleccionaron varias opciones de cuestionario. No se puede calificar")
            self.cuestionarioVarios.send("Se seleccionaron varias opciones de cuestionario.")
        elif opcion_cuestionario == Respuesta.NS:
            print("No seleccionó un cuestionario")
        else:
            # print("Cuestionario seleccionado: -----> {}".format(opcion_cuestionario))
            try:
                diccionario_solucion = self.__solucion[opcion_cuestionario]
            except KeyError:
                self.solucionarioIndefinido.send("No se han definido las claves de solución para este cuestionario.")
                # print("No se han definido las claves de solución para este cuestionario.")
                return imagen_formulario

            limite_revision = 1  # self.__numero_items
            for item_respuesta in self.__formulario.items_respuestas:
                # print(f"La respuesta: {item_respuesta.nombre} --> {item_respuesta.respuesta.nombre}")
                if item_respuesta.respuesta.nombre == Respuesta.NS:
                    noMarcadas += 1
                else:
                    nombre_item = item_respuesta.nombre
                    opcion_correcta = diccionario_solucion[nombre_item]
                    opcion_respuesta = item_respuesta.respuesta.nombre
                    if opcion_correcta is not None:
                        if opcion_correcta == opcion_respuesta:
                            suma += (self.__calificacion_maxima - self.__rango_minimo)/ self.__numero_items
                            if self.__marca_correctas:
                                item_respuesta.respuesta.dibujar_circulo_opcion()
                            numero_correctas += 1
                        else:
                            numero_incorrectas += 1
                limite_revision += 1
                if limite_revision > self.__numero_items:
                    break
            # A la suma total de los items correctos se les suma el valor base del calculo de la calificación
            suma += self.__rango_minimo
            # Si la suma da por debajo del la calificación mínima se toma la mínima
            if suma < self.__calificacion_minima:
                suma = self.__calificacion_minima

        self.__calificacion = round(suma, 1)
        self.__respuestasCorrectas = numero_correctas
        self.__respuestasIncorrectas = numero_incorrectas
        self.__noMarcadas = noMarcadas
        # print(f"Número de cuestionario: {self.__numeroCuestionario.value}")
        # print(f"Respuestas correctas   = {numero_correctas}")
        # print(f"Respuestas incorrectas = {numero_incorrectas}")
        # print(f"Total evaluadas        = {numero_correctas + numero_incorrectas}")
        imagen_formulario = cv2.cvtColor(imagen_formulario, cv2.COLOR_BGR2RGB)
        return imagen_formulario
