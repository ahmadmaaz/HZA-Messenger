from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5 import QtWidgets
from mainChat import ChatApp
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
    chat_app = ChatApp()
    run_peer(chat_app.emitter,cs,sp,cpf,spf)
    chat_app.show()

    sys.exit(app.exec_())
