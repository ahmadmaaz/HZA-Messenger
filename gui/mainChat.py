from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QMessageBox
from gui.chat import Ui_MainWindow as window
from core.peer import Peer
from gui.message_emitter import MessageEmitter
from gui.sendWidget import Widget as sendWidget
from gui.receiveWidget import Widget as receiveWidget
import threading
import base64

files_bytes = {}


class ChatApp(QMainWindow, window):
    def __init__(self, parent=None):
        super(ChatApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.send_btn.clicked.connect(self.send_data)
        self.label.mousePressEvent = self.send_file
        self.emitter = MessageEmitter()
        self.emitter.msg.connect(self.update_text_edit)
        self.messageList.itemClicked.connect(self.handle_message_clicked)
        self.peer = Peer()

    def send_data(self):
        if self.input.text().strip() == "":  # In case it was empty input, drop it before sending
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("you can submit empty label even if it is with spaces ;p")
            msg.setWindowTitle("Input is empty")
            msg.exec_()
            return
        self.send_btn.setEnabled(False)
        #lambda/ call back function to re-enable the button after sending packet is done 
        #This will prevent 2 messages overlapping ( the other peer will start receiving packets for 2 diff message ids )
        receive_thread = threading.Thread(target=self.peer.message_sender.send_message, args=(
            self.input.text(), self.emitter, lambda: self.send_btn.setEnabled(True)))
        receive_thread.start()
        self.input.setText("")

    def update_text_edit(self, message):
        widget = receiveWidget()
        message_to_display = message[1:]
        if message[0] == "1":
            widget = sendWidget()
        if "⁂" in message:  #this is a file
            parts = message.split("⁂")
            file_name = parts[1]
            if len(parts) == 3:
                files_bytes[file_name] = parts[2]
            message_to_display = "⁂ " + file_name
        widget.label_2.setText(message_to_display)
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint() / 1.4)

        self.messageList.addItem(item)
        self.messageList.setItemWidget(item, widget)
        self.messageList.setMinimumWidth(widget.width())
        self.messageList.setCurrentRow(self.messageList.count() - 1)

    def send_file(self,event):
        filename = QFileDialog.getOpenFileName()
        receive_thread = threading.Thread(target=self.peer.file_sender.send_file, args=(filename[0], self.emitter,))
        receive_thread.start()

    def handle_message_clicked(self, item):
        item_widget = self.messageList.itemWidget(item)
        message_content = item_widget.label_2.text()
        if "⁂" not in message_content:
            return
        file_name = message_content[1:].strip()
        if file_name not in files_bytes.keys():  # the peer that sent the file is trying to download it
            return
        encoded_data = files_bytes[file_name.strip()]
        decoded_data = base64.b64decode(encoded_data)
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File", file_name, "All Files (*);;Text files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'wb') as file:
                    file.write(decoded_data)
                print("File saved successfully.")
            except Exception as e:
                print("An error occurred while saving the file:", e)
