import sys, datetime
import serial.tools.list_ports
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QStringListModel
from ui import Ui_MainWindow   # file bạn export ra từ Qt Designer

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Thêm model Qlistview
        self.log_model = QStringListModel()
        self.ui.log.setModel(self.log_model)
        self.log_entries = []
        self.add_log_entry("Ứng dụng khởi động")
        self.load_com_ports()   
    

        # Ket noi button
        self.ui.connect_button.clicked.connect(self.establish_connection)
        self.serial_conn = None

    def add_log_entry(self, entry: str):
        entry = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {entry}"
        fontt = self.ui.log.font()
        fontt.setPointSize(10)
        self.ui.log.setFont(fontt)
        self.log_entries.append(entry)
        self.log_model.setStringList(self.log_entries)

    def load_com_ports(self):
        """Lấy danh sách cổng COM và đưa vào combobox com_select"""
        ports = serial.tools.list_ports.comports()
        self.ui.com_select.clear()  # Xóa danh sách cũ
        font = self.ui.com_select.font()
        font.setPointSize(8)
        self.ui.com_select.setFont(font)

        for port in ports:
            # port.device: tên cổng (COM3, ttyUSB0,...)
            # port.description: mô tả (USB-SERIAL CH340,...)
            display_text = f"{port.device} - {port.description}"
            self.ui.com_select.addItem(display_text, port.device)
            
        # Nếu không có cổng nào
        if not ports:
            self.ui.com_select.addItem("Không tìm thấy cổng", None)

    def get_selected_port(self):
        """Lấy cổng COM đang chọn"""
        return self.ui.com_select.currentData()

    def establish_connection(self):
        port = self.get_selected_port()
        if port:
            try:
                self.serial_conn = serial.Serial(port, 115200, timeout=1)
                self.serial_conn.write(b'SCALA_ACTIVATE\n')  # Gửi lệnh thử
                response = self.serial_conn.readline().decode().strip()
                if response == "SCALA_OK":
                    self.add_log_entry(f"Kết nối thành công và nhận được phản hồi từ {port}")
                else:
                    self.add_log_entry(f"Kết nối thất bại hoặc phản hồi không đúng từ {port}")
            except serial.SerialException as e:
                self.add_log_entry(f"Lỗi kết nối: {e}")
        else:
            self.add_log_entry("Chưa chọn cổng COM")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
