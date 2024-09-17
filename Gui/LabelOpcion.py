from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt


class LabelOpcion(QLabel):
    clicked = pyqtSignal()

    def __init__(self, nombre, tamanoFuente=14, radio=16, asignable = True):
        super().__init__()
        self.__nombre = nombre
        self.__activado = True
        self.setText(nombre)
        self.__tamanoFuente = str(tamanoFuente)
        self.__radio = str(radio)
        self.__asignable = asignable
        self.inicializarObjeto()

    def inicializarObjeto(self):
        self.setStyleSheet(
            f"color: #000000; background-color: LightGray; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
        )
        self.setMinimumSize(int(self.__radio) * 2, int(self.__radio) * 2)
        self.setMaximumSize(int(self.__radio) * 2, int(self.__radio) * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if self.__asignable:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    @property
    def nombre(self):
        return self.__nombre

    @property
    def activado(self):
        return self.__activado

    @activado.setter
    def activado(self, valor):
        self.__activado = valor
        if self.__activado:
            self.setStyleSheet(
                f"color: #000000; background-color: LightGray; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
            )
            if self.__asignable:
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                pass
        else:
            self.setStyleSheet(
                f"color: #A3A3A3; background-color: #E3E3E3; border-radius: {self.__radio}px; font: {self.__tamanoFuente}px Arial;"
            )
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()