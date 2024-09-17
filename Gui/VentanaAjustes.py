from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6 import uic
from Logica.ConfiguracionXML import Configuracion
from blinker import Signal
class VentanaAjustes(QDialog):
    respuesta = Signal()
    def __init__(self, parent=None, configuracion: Configuracion = None):
        super().__init__(parent)
        self.__configuracion = configuracion
        uic.loadUi("Gui/disenoajustes.ui", self)

        self.spinUmbralPGP.setValue(int(configuracion.umbralColorPuntosGuiaPrincipales))
        self.spinUmbralPGS.setValue(int(configuracion.umbralColorPuntosGuiaSecundarios))
        self.spinUmbralOpcionMarcada.setValue(int(configuracion.umbralColorOpcionMarcada))

        self.buttonAceptar.clicked.connect(self.buttonAceptarClicked)
        self.buttonCancelar.clicked.connect(self.buttonCancelarClicked)

    def buttonAceptarClicked(self):
        self.__configuracion.umbralColorPuntosGuiaPrincipales = str(self.spinUmbralPGP.value())
        self.__configuracion.umbralColorPuntosGuiaSecundarios = str(self.spinUmbralPGS.value())
        self.__configuracion.umbralColorOpcionMarcada = str(self.spinUmbralOpcionMarcada.value())
        self.respuesta.send("1")
        self.close()

    def buttonCancelarClicked(self):
        self.close()

