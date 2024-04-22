from PyQt5.QtCore import QObject, pyqtSignal

class MessageEmitter(QObject):
    msg = pyqtSignal(str)