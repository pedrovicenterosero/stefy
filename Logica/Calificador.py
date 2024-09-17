# from src.tests.FormularioRespuestas import FormularioRespuestas
from HojaRespuestas import HojaRespuestas
from Seleccion import *


class Calificador:
    def __init__(self, formulario=HojaRespuestas(),
                 calificacion_maxima=5,
                 calificacion_minima=1,
                 numero_items=20):
        self.__formulario = formulario
        self.__solucion = dict()
        self.__calificacion_maxima = calificacion_maxima
        self.__calificacion_minima = calificacion_minima
        self.__numero_items = numero_items
        self.__calificacion = 0
        self.__marca_correctas = False

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

    def evaluar(self):
        imagen_formulario = self.__formulario.escanear(0)
        item_cuestionario = self.__formulario.cuestionario
        opcion_cuestionario = item_cuestionario.respuesta.nombre
        #print(f"opcion cuestionario -------------------> {opcion_cuestionario}")
        if opcion_cuestionario == Respuesta.NS:
            nc = int(input("Número de cuestionario = "))

            if nc == 1:
                opcion_cuestionario = Cuestionario.C1
            elif nc == 2:
                opcion_cuestionario = Cuestionario.C2
            elif nc == 3:
                opcion_cuestionario = Cuestionario.C3
            elif nc == 4:
                opcion_cuestionario = Cuestionario.C4

        #print(opcion_cuestionario)
        suma = 0
        numero_incorrectas = 0
        numero_correctas = 0
        if opcion_cuestionario == Respuesta.MS:
            print("Se seleccionaron varias opciones de cuestionario. No se puede calificar")
        elif opcion_cuestionario == Respuesta.NS:
            print("No seleccionó un cuestionario")
        else:
            print("Cuestionario seleccionado: -----> {}".format(opcion_cuestionario))
            try:
                diccionario_solucion = self.__solucion[opcion_cuestionario]
            except KeyError:
                print("No se ha definido un solucionario para este cuestionario.")
                return imagen_formulario
            limite_revision = 1  # self.__numero_items
            for item_respuesta in self.__formulario.items_respuestas:
                nombre_item = item_respuesta.nombre
                opcion_respuesta = item_respuesta.respuesta.nombre
                #print("Item {}".format(item_respuesta.nombre))
                opcion_correcta = diccionario_solucion[nombre_item]
                # print("Respuesta solucion: {}".format(opcion_correcta))

                if opcion_correcta is not None:
                    if opcion_correcta == opcion_respuesta:
                        suma += self.__calificacion_maxima / self.__numero_items
                        if self.__marca_correctas:
                            item_respuesta.respuesta.dibujar_circulo_opcion()
                        # print("Correcto")
                        numero_correctas += 1
                    else:
                        # print("Incorrecto")
                        numero_incorrectas += 1
                    print(f"Calificacion ---> {suma}")
                limite_revision += 1
                if limite_revision > self.__numero_items:
                    break

            if suma < 1:
                suma = 1

        self.__calificacion = round(suma, 2)
        print(f"Respuestas correctas   = {numero_correctas}")
        print(f"Respuestas incorrectas = {numero_incorrectas}")
        print(f"Total evaluadas       = {numero_correctas + numero_incorrectas}")
        return imagen_formulario
