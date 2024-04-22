from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from rec import Ui_Form as form


class Widget(QWidget,form):
    def __init__(self, parent=  None ):
        super(Widget,self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
