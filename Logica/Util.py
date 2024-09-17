import cv2
import numpy as np

class Util():
    @staticmethod
    def recorte_imagen(imagen, punto1, punto2):
        x = punto1[0]
        y = punto1[1]

        ancho = abs(punto1[0] - punto2[0])
        alto = abs(punto1[1] - punto2[1])
        recorte = imagen[y: y + alto, x: x + ancho]

        if len(recorte) == 0:
            print (f"¿Puntos de recorte erroneos? {punto1}, {punto2}")

            alto_imagen, ancho_imagen, _ = imagen.shape
            print(f"Dimensiones del segmento: {ancho_imagen} x {alto_imagen}")

        return recorte

    @staticmethod
    def detectar_circulos_opciones(
        imagen, minima_distancia=20, umbral_negro=200, min_radio=8, max_radio=20
    ):
        # Binarizar la imagen para eliminar los grises
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        _, imagen_binarizada = cv2.threshold(
            imagen_gris, umbral_negro, 255, cv2.THRESH_BINARY
        )
        # Aplicar desenfoque gaussiano para reducir el ruido
        gray = cv2.GaussianBlur(imagen_binarizada, (5, 5), 0)

        # Usar la Transformada de Hough para detectar círculos
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=minima_distancia,
            param1=50,
            param2=20,
            minRadius=min_radio,
            maxRadius=max_radio,
        )
        circulos = []

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for x, y, r in circles:
                circulos.append((x, y, r))
                # cv2.circle(imagen, (x, y), r, (0, 255, 0), 2)

        return circulos

    @staticmethod
    def agrupar_circulos(circulos, margen_error=2):
        # Ordenar los círculos por la segunda componente de su centro (eje y)
        circulos.sort(key=lambda circulo: circulo[1])

        # Crear una lista para almacenar los grupos de círculos
        grupos = []
        grupo_actual = [circulos[0]]

        for i in range(1, len(circulos)):
            # Si el círculo actual está en la misma línea horizontal que el último círculo del grupo actual
            if abs(circulos[i][1] - grupo_actual[-1][1]) <= margen_error:
                # Añadir el círculo al grupo actual
                grupo_actual.append(circulos[i])
            else:
                # Añadir el grupo actual a la lista de grupos y empezar un nuevo grupo con el círculo actual
                grupos.append(grupo_actual)
                grupo_actual = [circulos[i]]

        # Añadir el último grupo a la lista de grupos
        grupos.append(grupo_actual)
        # print("Cantidad de respuestas {}".format(len(grupos)))
        # print(grupos)
        return grupos

    @staticmethod
    def detectar_puntos_guia(
        imagen, area_minima=200, area_maxima=400, porcentaje_epsilon=0.02
    ):
        """
        Detecta los cuadros guia del formulario de respuestas
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
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
                    cv2.drawContours(imagen, [approx], 0, (0, 255, 0), 2)
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

    @staticmethod
    def centro_contorno(contorno):
        """Determina el centro el centro de un contorno"""
        M = cv2.moments(contorno)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)

    # Definir una función personalizada como clave de ordenación
    def ordenar_puntos(puntos):
        puntos.sort(key=lambda x: (x[1], x[0]))
        primeros_dos = puntos[:2]
        ultimos_dos = puntos[2:]
        primeros_dos.sort(key=lambda x: x[0])
        ultimos_dos.sort(key=lambda x: x[0])
        return primeros_dos + ultimos_dos

    def eliminar_ruido(imagen):
        _, imagen_binaria = cv2.threshold(imagen, 127, 255, cv2.THRESH_BINARY)
        elemento_estructurante = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        imagen_dilatacion = cv2.dilate(imagen_binaria, elemento_estructurante)
        imagen_erosion = cv2.erode(imagen_dilatacion, elemento_estructurante)
        return imagen_erosion

    @staticmethod
    def longitud_promedio_contornos(lista_contornos):
        """Calcula la longitud promedio de una lista de contornos"""
        cantidad_contornos = len(lista_contornos)
        porcentaje = 1 / cantidad_contornos
        longitud_promedio = 0
        for contorno in lista_contornos:
            longitud_contorno = cv2.arcLength(contorno, True)
            longitud_promedio += int(porcentaje * longitud_contorno)

        return longitud_promedio

    @staticmethod
    def centros_contornos(lista_contornos):
        """Determina los centros de los contornos pasados en una lista"""
        centros = []
        for contorno in lista_contornos:
            centros.append(Util.centro_contorno(contorno))
        return centros

    @staticmethod
    def puntos_guia_secundarios(imagen, area_minima=6, umbral=60): # umbral --> Mayor valor para exceso de luz, y vice
        lista_contornos = list()
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        _, binaria = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY_INV)
        contornos, _ = cv2.findContours(binaria, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contorno in contornos:
            area_contorno = cv2.contourArea(contorno)
            # print("Area", area_contorno)
            if area_contorno > area_minima:
                if Util.es_contorno_unico(contorno, lista_contornos, tolerancia=5):
                    lista_contornos.append(contorno)
        lista_centros = list()
        for contorno in lista_contornos:
            centro = Util.centro_contorno(contorno)
            lista_centros.append(centro)

        # Comprueba que estén todos los centros secundarios necesarios
        # centrosProbables = [(6, 7), (3, 55), (3, 101), (3, 153), (6, 544)]
        centrosProbables = [(6, 7), (3, 110), (3, 160), (3, 225), (6, 618)]
        for centroProbable in centrosProbables:
            existeCentro = False
            cpx, cpy = centroProbable
            for centro in lista_centros:
                cx, cy = centro
                if abs(cpx - cx) < 5 and abs(cpy - cy) < 10:
                    existeCentro = True
                    break
            if not existeCentro:
                lista_centros.append(centroProbable)
                print(f"Este punto guia no fue encontrado: {centroProbable}")

        # Ordena los centros por su segunda componente
        if len(lista_centros) > 0:
            lista_centros.sort(key=lambda x: (x[1]))

        return lista_centros

    def es_contorno_unico(contorno, lista_contornos, tolerancia=100):
        centro_con = Util.centro_contorno(contorno)
        centro_con_x = centro_con[0]
        centro_con_y = centro_con[1]
        # Valida que el contorno que se va a agregar a la lista sea único
        contorno_unico = True
        for c in lista_contornos:
            centro_c = Util.centro_contorno(c)
            centro_c_x = centro_c[0]
            centro_c_y = centro_c[1]

            if (
                abs(centro_c_x - centro_con_x) < tolerancia
                and abs(centro_c_y - centro_con_y) < tolerancia
            ):
                contorno_unico = False
                break
        return contorno_unico

    #@staticmethod
    #def beep():
    #    frequencia = 3500  # Establece la frecuencia a 2500 Hertz
    #    duracion = 10  # Establece la duración a 1000 ms == 1 segundo
    #    winsound.Beep(frequencia, duracion)


