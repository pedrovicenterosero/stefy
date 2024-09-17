from Logica.OpcionRespuesta import *
from Logica.Util import *

class ItemRespuesta:
    def __init__(self, segmento_imagen, nombre=0, numero_opciones=4, separacion_opciones=32,
                 seccion=Seccion.Respuestas, umbralOpcionMarcada = 127):
        self.__nombre = nombre
        self.__numero_opciones = numero_opciones
        self.__segmento = segmento_imagen
        self.__separacion_opciones = separacion_opciones
        self.__seccion = seccion
        self.__umbralOpcionMarcada = umbralOpcionMarcada
        self.__opciones = self.__lista_opciones()
        self.__seleccionadas = self.__opciones_seleccionadas()
        self.__unica_seleccion = self.__unica_seleccionada()
        self.__respuesta = self.__respuesta_seleccionada()
        self.__opciones_falsas = self.__opciones_falsas_agregadas()
        self.__mostrarNombreItemOpcion = False

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def numero_opciones(self):
        return self.__numero_opciones

    @property
    def segmento(self):
        return self.__segmento

    @property
    def separacion_opciones(self):
        return self.__separacion_opciones

    @separacion_opciones.setter
    def separacion_opciones(self, valor):
        self.__separacion_opciones = valor

    @property
    def seccion(self):
        return self.seccion

    @seccion.setter
    def seccion(self, valor):
        self.__seccion = valor

    @property
    def opciones(self):
        """Devuelve una lista con las opciones de respuesta que componen al item"""
        return self.__opciones

    @property
    def seleccionadas(self):
        """Devuelve una lista con las opciones seleccionadas o marcadas"""
        return self.__seleccionadas

    @property
    def unica_seleccion(self):
        """Devuelve True si en el item se seleccionó una sola opción"""
        return self.__unica_seleccion

    @property
    def respuesta(self):
        return self.__respuesta

    @property
    def opciones_falsas(self):
        """Devuelve un listado de las opciones que no se pudieron detectar en el formulario físico"""
        return self.__opciones_falsas
    @property
    def mostrarNombreItemOpcion(self):
        return self.__mostrarNombreItemOpcion

    @mostrarNombreItemOpcion.setter
    def mostrarNombreItemOpcion(self, valor):
        self.__mostrarNombreItemOpcion = valor

    @property
    def umbralOpcionMarcada(self):
        return self.__umbralOpcionMarcada

    # @umbralOpcionMarcada.setter
    # def umbralOpcionMarcada(self, valor):
    #     self.__umbralOpcionMarcada = valor

    def dibujar_circulos_opciones(self, todas=False):
        if todas:
            color_circulo = (255, 0, 0)
            for opcion in self.__opciones:
                opcion.dibujar_circulo_opcion(color=color_circulo)
        else:
            if self.__seleccionadas is not None:
                if self.__unica_seleccion:
                    #color_circulo = (238, 130, 238)
                    color_circulo = (190, 0, 210)
                else:
                    color_circulo = (0, 0, 255)

                for opcion in self.__seleccionadas:
                    opcion.mostrar_texto = self.__mostrarNombreItemOpcion
                    #print(f"Nombre del item: {self.nombre}")
                    opcion.dibujar_circulo_opcion(color=color_circulo, texto=str(self.__nombre))

    def __lista_opciones(self):
        opciones = list()
        for i in range(self.numero_opciones):
            segmento_opcion = Util.recorte_imagen(self.__segmento,
                                                  (i * self.separacion_opciones, 0),
                                                  (40 + i * self.separacion_opciones, 22)
                                                  )
            opcion = OpcionRespuesta(segmento_opcion, umbralColor=self.__umbralOpcionMarcada)
            # print(f"Desde ItemRespuesta umbralColor {opcion.umbralColor}")
            if self.__seccion == Seccion.Respuestas:
                opcion.nombre = Respuesta(i)  # .name
            else:
                opcion.nombre = Cuestionario(i)  # .name
            # ------>
            # puntoSegmento = (40 + i * self.separacion_opciones, 22)
            # cv2.rectangle(segmento_opcion, (0, 0), puntoSegmento, (255, 214, 133), 1)
            # cv2.imshow(f"Item {opcion.nombre} Opcion {str(i)}", segmento_opcion)
            # ------>
            opciones.append(opcion)
        return opciones

    def __opciones_seleccionadas(self):
        seleccionadas = list()
        if self.__opciones is not None:
            for opcion in self.__opciones:
                if opcion.estado == Seleccion.Seleccionado:
                    seleccionadas.append(opcion)

        return seleccionadas

    def __unica_seleccionada(self):
        return len(self.__seleccionadas) == 1

    def __respuesta_seleccionada(self):
        # seleccionadas = list()
        if self.__unica_seleccion:
            return self.__seleccionadas[0]
        else:
            opcion_error = OpcionRespuesta(None)
            # if self.__seccion == Seccion.Respuestas:
            if len(self.__seleccionadas) > 1:
                opcion_error.nombre = Respuesta(98)
                # return opcion_error
            else:
                opcion_error.nombre = Respuesta(99)

            return opcion_error
            # else:
            #     if len(self.__seleccionadas) > 1:
            #         return Cuestionario(98)
            #     else:
            #         return Cuestionario(99)

    def __opciones_falsas_agregadas(self):
        opciones_falsas = list()
        for opcion in self.__opciones:
            if not opcion.real:
                opciones_falsas.append(opcion)

        return opciones_falsas
