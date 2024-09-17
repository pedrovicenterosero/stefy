import sys
from PyQt6.QtWidgets import QApplication
from Gui.Ventana import Ventana

if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(aplicacion.exec())
