from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5 import QtWidgets
from design import Ui_MainWindow as ui
from peer import run as run_peer

import sys

"""
    Run the main.py to the run the application
    choose between alice and bob
    after that choose if you want to initiate connection or no
"""
if __name__ == "__main__":
    aliceOrBob= input("Alice or Bob? (a or b): ")
    if(aliceOrBob.lower()=="a"):
        cs=12000
        sp=12001
        spf=12002
        cpf=12003
    else:
        cs=12001
        sp=12000
        spf=12003
        cpf=12002
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ui()
    ui.setupUi(MainWindow)
    run_peer(ui.emitter,cs,sp,cpf,spf)
    MainWindow.show()
    sys.exit(app.exec_())
