from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from Gui.LabelOpcion import LabelOpcion

class ItemRespuesta(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None, nombre="1", tamanoFuente=14, radio=16, asignable=True):
        super(ItemRespuesta, self).__init__(parent)
        self.__nombre = nombre
        self.__seleccion = None
        self.__activado = True
        self.__tamanoFuente = str(tamanoFuente)
        self.__radio = str(radio)
        self.__asignable = asignable
        self.__inicializarItem()

    def __inicializarItem(self):
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.__labelNumeroItem = QLabel(self.__nombre)
        #self.__labelNumeroItem.setAlignment(Qt.AlignCenter)
        self.__labelNumeroItem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # print(f"font: {self.__tamanoFuente}px Arial;")
        self.__labelNumeroItem.setStyleSheet(f"font: {self.__tamanoFuente}px Arial;")
        self.__labelNumeroItem.setMinimumSize(int(self.__radio), int(self.__radio) * 2)
        self.__labelNumeroItem.setMaximumSize(int(self.__radio), int(self.__radio) * 2)
        self.layout.addWidget(self.__labelNumeroItem)

        opciones = ["A", "B", "C", "D"]
        self.__labelsOpciones = [LabelOpcion(opcion,
                                             tamanoFuente=int(self.__tamanoFuente),
                                             radio=int(self.__radio), asignable=self.__asignable) for opcion in opciones]

        for labelOpcion in self.__labelsOpciones:
            if self.__asignable:
                labelOpcion.clicked.connect(self.onClick)
            self.layout.addWidget(labelOpcion)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def seleccion(self):
        return self.__seleccion

    @seleccion.setter
    def seleccion(self, valor):
        if self.__activado:
            self.__seleccion = valor
            if self.__seleccion is not None:
                for labelOpcion in self.__labelsOpciones:
                    if labelOpcion.nombre == self.__seleccion:
                        labelOpcion.setStyleSheet(
                            f"background-color: DarkCyan; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
                        )
                    elif labelOpcion.nombre != self.__seleccion:
                        labelOpcion.setStyleSheet(
                            f"background-color: LightGray; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
                        )
            else:
                for labelOpcion in self.__labelsOpciones:
                    labelOpcion.setStyleSheet(
                        f"background-color: LightGray; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
                    )
        #print(valor)

    @property
    def activado(self):
        return self.__activado

    @activado.setter
    def activado(self, valor):
        """Activa o desactiva un item de opciones para permitir o bloquear la selección de una respuesta"""
        self.__activado = valor
        if self.__activado:
            self.__labelNumeroItem.setStyleSheet(f"color: #000000; font: {self.__tamanoFuente}px Arial;")
        else:
            self.__labelNumeroItem.setStyleSheet(f"color: #939393; font: {self.__tamanoFuente}px Arial;")

        for labelOpcion in self.__labelsOpciones:
            labelOpcion.activado = valor

    def onClick(self):
        # print("Clic {}")
        opcionSeleccionada = self.sender()
        self.__seleccion = opcionSeleccionada.nombre
        # print("Clic en {} - Item {}".format(labelO.nombre, self.__nombre))
        if self.__activado:
            for labelOpcion in self.__labelsOpciones:
                if labelOpcion is opcionSeleccionada:
                    labelOpcion.setStyleSheet(
                        f"background-color: DarkCyan; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
                    )
                else:
                    labelOpcion.setStyleSheet(
                        f"background-color: LightGray; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
                    )

            self.clicked.emit()