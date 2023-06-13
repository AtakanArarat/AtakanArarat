import sys

from PyQt6 import QtCore, QtWidgets, QtSerialPort 
from PyQt6.QtWidgets import QApplication, QMainWindow ,QWidget ,QToolBar ,QHBoxLayout, QWidgetAction ,QStatusBar ,QLineEdit ,QPushButton ,QTextEdit , QVBoxLayout 
from PyQt6.QtCore import Qt , pyqtSignal
from PyQt6.QtSerialPort import QSerialPortInfo

class AddComport(QMainWindow):
    porttnavn = pyqtSignal(str)

    def __init__(self, parent , menu):
        super().__init__(parent)

  
        menuComport = menu.addMenu("COM Port")
    
        info_list = QSerialPortInfo()
        serial_list = info_list.availablePorts()
        serial_ports = [port.portName() for port in serial_list]
        if(len(serial_ports)> 0):
            port_num = len(serial_ports)
            count = 0
            while count < port_num:
                button_action = QWidgetAction(serial_ports[count], self)
                txt = serial_ports[count]
                portinfo = QSerialPortInfo(txt)
                buttoninfotxt = " Bilgi Yok"
                if portinfo.hasProductIdentifier():
                    buttoninfotxt = ("Ürün Özellikleri = " + str(portinfo.vendorIdentifier()))
                if portinfo.hasVendorIdentifier():
                    buttoninfotxt =  buttoninfotxt + (" Üretici kimliği = "+ str(portinfo.productIdentifier()))
                button_action = QWidgetAction( txt , self)
                button_action.setStatusTip( buttoninfotxt)
                button_action.triggered.connect(lambda checked, txt = txt: self.selectComportClick(txt))
                menuComport.addAction(button_action)
                count = count +1
        else:
            print("COM Bağlantısı Kurulamadı")

    def selectComportClick(self , port):
        self.porttnavn.emit(port)
   
    def closeEvent(self, event):
        self.close()


class MainWindow(QMainWindow):  
    def __init__(self):
        super(MainWindow, self).__init__()

        portname = "None"
    
        self.setStatusBar(QStatusBar(self))
   
        menu = self.menuBar()
        comfinder = AddComport(self , menu)
        comfinder.porttnavn.connect(self.selectComport)

        self.setWindowTitle("Seri Port Penceresi / Gönder")
    
        self.message_le = QLineEdit()
        self.send_btn = QPushButton(
            text="Gönder",
            clicked=self.send
        )
    
        self.output_te = QTextEdit(readOnly=True)
        self.button = QPushButton(
            text="Bağlantı Yap", 
            checkable=True,
            toggled=self.on_toggled
        )
        lay = QVBoxLayout(self)
        hlay = QHBoxLayout()
        hlay.addWidget(self.message_le)
        hlay.addWidget(self.send_btn)
        lay.addLayout(hlay)
        lay.addWidget(self.output_te)
        lay.addWidget(self.button)
    
        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

        self.serial = QtSerialPort.QSerialPort(
            portname,
            baudRate=QtSerialPort.QSerialPort.BaudRate(9600),
            readyRead=self.receive)
   
           
    @QtCore.pyqtSlot()
    def receive(self):
        while self.serial.canReadLine():
            text = self.serial.readLine().data().decode()
            text = text.rstrip('\r\n')
            self.output_te.append(text)

    @QtCore.pyqtSlot()
    def send(self):
        self.serial.write(self.message_le.text().encode())

    @QtCore.pyqtSlot(bool)
    def on_toggled(self, checked):
        self.button.setText("Bağlantı Kes" if checked else "Bağlantı Yap")
        if checked:
            if not self.serial.isOpen():
                self.serial.open(QtCore.QIODevice.ReadWrite)
                if not self.serial.isOpen():
                    self.button.setChecked(False)
            else:
                self.button.setChecked(False)
        else:
            self.serial.close()
  
    def selectComport(self , nyport):
        seropen = False
        if self.serial.isOpen():
            seropen = True
            self.serial.close()   
        self.serial.setPortName(nyport)
        if seropen:
            self.serial.open(QtCore.QIODevice.ReadWrite)
            if not self.serial.isOpen():
                self.button.setChecked(False)
        
        print(nyport)
    
    def closeEvent(self, event):
        self.serial.close()
        print("COM Port Kapatıldı")
        # print(comporttxt)
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())