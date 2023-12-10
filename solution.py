import os
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from collections import Counter
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QFileDialog, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QTextEdit, QLineEdit
from PySide2.QtGui import QIcon, QGuiApplication
from PySide2.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File statistics")
        self.setGeometry(300,200,1000,700)

        self.setIcon()
        self.center()

        self.createInterface()
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.show()
        self.char_list = []

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def quitApp(self, event):
        userInfo = QMessageBox.question(self, "Confirmation", "Do you want to quit the application?",
                                        QMessageBox.Yes | QMessageBox.No)

        if userInfo == QMessageBox.Yes:
            event.accept()
            myapp.quit()
            sys.exit()

        elif userInfo == QMessageBox.No:
            event.ignore()

    def closeEvent(self, event):
        self.quitApp(event)

    def center(self):
        qRect = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def create_statistics(self):

        statistics = QDialog(self)
        statistics.setWindowTitle("Filenames's first letter distribution")
        statistics.setGeometry(300,200,1000,700)

        gridLayout = QVBoxLayout()

        capital_list = [key.lower() for key in self.char_list]
        counter = Counter(capital_list)
        sorted_list = sorted(counter.items())

        x = [element[0] for element in sorted_list]
        y = [element[1] for element in sorted_list]

        fig = Figure()
        canvas = FigureCanvas(fig)
        axes = fig.add_subplot()

        axes.set_xlabel("Characters")
        axes.set_ylabel("Number of occurrences")
        axes.bar(x, y, color=[(0.2, 0.4, 0.6, 0.6), 'darkslategray'])

        button = QPushButton('Close')
        button.setMinimumWidth(40)
        button.setMaximumWidth(100)
        button.clicked.connect(statistics.close)

        gridLayout.addWidget(canvas)
        gridLayout.addWidget(button, alignment=Qt.AlignRight)
        statistics.setLayout(gridLayout)
        statistics.exec_()

    def list_files(self, main_folder):

        for filename in os.listdir(main_folder):
            full_path = os.path.join(main_folder, filename)

            if len(self.char_list) < 1000:

                if os.path.isfile(full_path):
                    self.textArea.insertPlainText(filename)
                    self.textArea.insertHtml('<br/> ')
                    self.char_list.append(filename[0])

                elif os.path.isdir(full_path):
                    self.list_files(full_path)
            else:
                break

    def get_files(self):

        directory = QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())

        if directory:
            self.lineEdit.setText(directory)
            self.textArea.setText('')
            self.char_list = []
            self.list_files(directory)
        else:
            self.lineEdit.setText('Choose Directory')
            self.textArea.setText('')

    def createInterface(self):

        self.groupBox = QGroupBox()
        gridLayout = QGridLayout()

        self.lineEdit = QLineEdit("Selected folder")
        self.lineEdit.setStyleSheet("QLineEdit { color: rgb(47,79,79); }");
        self.lineEdit.setReadOnly(True)
        gridLayout.addWidget(self.lineEdit, 0,0)

        button = QPushButton(">>", self)
        button.setMinimumWidth(40)
        button.setMaximumWidth(60)
        button.clicked.connect(self.get_files)
        gridLayout.addWidget(button, 0,1)

        button2 = QPushButton("", self)
        button2.setIcon(QIcon("statistics.png"))
        button2.setMinimumWidth(40)
        button2.setMaximumWidth(60)
        button2.clicked.connect(self.create_statistics)
        gridLayout.addWidget(button2, 0,2)

        self.textArea = QTextEdit()
        self.textArea.setReadOnly(True)
        gridLayout.addWidget(self.textArea, 1,0,2,3)

        self.groupBox.setLayout(gridLayout)


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    window = Window()

    myapp.exec_()
    sys.exit()
