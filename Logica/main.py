# import cv2
# import numpy as np
from src.tests.FormularioRespuestas import FormularioRespuestas
from Util import *
from Seleccion import *
from Calificador import Calificador
from ArchivoExamenXML import ArchivoExamenXML
if __name__ == '__main__':
    archivo = ArchivoExamenXML("K:/Examen de Periodo 3 Informatica06.xml")
    archivo.abrir()
    numero_preguntas = int(archivo.numeroPreguntas)
    conjuntos_cuestionarios = int(archivo.conjuntosCuestionarios)
    print(f"numero_preguntas: {numero_preguntas}")
    print(f"conjuntos_cuestionarios: {conjuntos_cuestionarios}")

    soluciones = {}
    for i in range(conjuntos_cuestionarios):
        # print(i + 1)
        diccionarioSolucion = archivo.devolverRespuestas(str(i + 1))
        solucion = {}
        for j in range(numero_preguntas):
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


    formulario = FormularioRespuestas()
    # solucion = {Cuestionario.C1: solucion_c1, Cuestionario.C2: solucion_c2}

    calificador = Calificador(formulario=formulario, numero_items=numero_preguntas)
    calificador.solucion = soluciones
    calificador.marca_correctas = True
    imagen_formulario = calificador.evaluar()

    print("Calificacion: {}".format(round(calificador.calificacion, 1)))
    # imagen_formulario = formulario.escanear_formulario(puerto_video=1)
    # print("Cuestionario {}".format(formulario.cuestionario.nombre_respuesta))
    #
    # # print(formulario.respuestas)
    # for i in range(30):
    #     item = formulario.items_respuestas[i]
    #     print("{} - {}".format(item.nombre, item.nombre_respuesta))
    #
    # cv2.imshow("Formulario", imagen_formulario)
    # segmento_cuestionario1 = formulario.secciones[1]
    # segmento_respuestas1 = formulario.secciones[2]
    # segmento_respuestas2 = formulario.secciones[3]

    # separacion_h = 70
    # for i in range(4):
    #     cv2.rectangle(segmento_cuestionario1, (115 + i * separacion_h, 20), (155 + i * separacion_h, 42), (0, 255, 0),
    #                   1)
    #
    # separacion_h = 32
    # separacion_v = 25
    # for k in range(15):
    #     for i in range(4):
    #         cv2.rectangle(segmento_respuestas1,
    #                       (48 + i * separacion_h, 12 + k * separacion_v),
    #                       (80 + i * separacion_h, 38 + k * separacion_v),
    #                       (255, 0, 0), 1)
    #
    #         cv2.rectangle(segmento_respuestas2,
    #                       (48 + i * separacion_h, 12 + k * separacion_v),
    #                       (80 + i * separacion_h, 38 + k * separacion_v),
    #                       (255, 0, 0), 1)
    #
    # # cv2.rectangle(segmento_cuestionario1, (125, 20), (147, 42), (0, 255, 0), 1)
    # # cv2.rectangle(segmento_cuestionario1, (195, 20), (217, 42), (0, 255, 255), 1)
    #
    # cv2.imshow("Segmento cuestionario", segmento_cuestionario1)
    # cv2.imshow("Respuestas 1", segmento_respuestas1)
    # cv2.imshow("Respuestas 2", segmento_respuestas2)
    # cv2.imshow("Original", formulario.frame_original)
    cv2.imshow("Formulario evaluado", imagen_formulario)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''Un enfoque válido puede ser crear una función que se encargue de capturar el video y cuando logre capturar 
la parte importante del formulario , cree el objeto formulario=FormularioRespuesta(imagen_formulario)'''
