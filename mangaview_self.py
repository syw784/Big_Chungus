""" Hi mom and dad on github
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap, QPalette, QResizeEvent
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog
import os, time

class MangaView(QMainWindow):
    
    def __init__(self):
        super(MangaView, self).__init__()
        self.resize(345, 256)
        self.setWindowTitle('Big Chungus')
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.verticalLayout.addWidget(self.scrollArea)
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollVLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.open_the_waygate = QAction("open", shortcut="Ctrl+O", triggered=self.load_images_from_waygate)
        self.remove_ALL_label_menu = QAction("&clear", triggered=self.remove_ALL_label)
        self.test_menu = QAction("&testo", shortcut="Ctrl+F", triggered=self.test)
        self.zoomInAct = QAction("Zoom &In (25%)", shortcut="Up", triggered=self.zoomIn)
        self.zoomOutAct = QAction("Zoom &Out (25%)", shortcut="Down", triggered=self.zoomOut)
        self.normalSizeAct = QAction("&Reset Scale", shortcut="0", triggered=self.normalSize)
        self.about_menu = QAction("&About", triggered=self.about)
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.fileMenu = QMenu("Function")
        self.fileMenu.addAction(self.open_the_waygate)
        self.fileMenu.addAction(self.remove_ALL_label_menu)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.zoomInAct)
        self.fileMenu.addAction(self.zoomOutAct)
        self.fileMenu.addAction(self.normalSizeAct)

        self.aboutMenu = QMenu("About")
        self.aboutMenu.addAction(self.about_menu)

        self.menubar.addMenu(self.fileMenu)
        self.menubar.addMenu(self.aboutMenu)

        self.labels = []
        self.label_pix = {}
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.display_current_page)
        self.set_scale()
        self.setAcceptDrops(True)
        self.show()

    def wheelEvent(self, event):
        return
        if (event.modifiers() & QtCore.Qt.ControlModifier):
            if event.angleDelta().y() > 0:
                self.zoomIn()
            elif event.angleDelta().y() < 0:
                self.zoomOut()
            event.accept()            

    def test(self):
        #print(self.get_current_index())
        return None

    def dragEnterEvent(self, e):
        if (len(e.mimeData().urls()) > 0):
            e.accept()

    def keyPressEvent(self, e):
        if (e.key() == QtCore.Qt.Key_Delete):
            if self.labels == []:
                return None
            if QMessageBox.question(self, 'Confirm', 'about to delete ' + 
            self.address + '/' + self.accepted[self.get_current_index()], 
            QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                os.remove(self.address + '/' + self.accepted[self.get_current_index()])
                #self.labels[self.get_current_index()].setParent(None)
                self.labels.pop(self.get_current_index()).setParent(None)

    def dropEvent(self, e):
        try:
            self.load_images(self.solve_path(e))
        except:
            QMessageBox.about(self, 'WTF', 'No')

    def solve_path(self, event):
        d = event.mimeData().urls()[0].path()[1:]
        if os.path.isdir(d):
            return d
        else:
            return d[:d.rfind('/')]

    def display_current_page(self):
        i = self.get_current_index()
        self.statusBar().showMessage(str(i + 1) + '/' + str(len(self.labels)) )#+ " :" + self.accepted[i])

    def get_current_index(self):
        ind = 0
        j = 0
        k = self.scrollArea.verticalScrollBar().value()
        if k == self.scrollArea.verticalScrollBar().maximum():
            return len(self.labels) - 1
        for i in self.labels:
            j += i.pixmap().size().height()
            if j > k:
                return ind
            ind += 1
        return ind

    def get_scale(self):
        if self.labels == []:
            self.scale = 1.0
        return self.scale

    def get_content_width(self):
        return self.scrollArea.size().width() - 40

    def set_scale(self, scale = 1.0):
        self.scale = scale
        if len(self.labels) > 0:
            i = self.scrollArea.verticalScrollBar()
            i.setValue(i.value() * scale / self.labels[0].pixmap().size().width() * self.get_content_width())
        for i in self.labels:#.scaled(640, 512, Qt::KeepAspectRatio))
            j = self.label_pix[i]
            i.setPixmap(j.scaledToWidth(self.get_content_width() * scale))
            #i.resize(self.scale * i.pixmap().size())

    def resizeEvent(self, event):
        self.set_scale(self.get_scale())
        #print('poo')

    def add_label(self, path, index = 'last'):
        #
        label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        label.setPixmap(QtGui.QPixmap(path))
        self.label_pix[label] = label.pixmap().copy()
        label.resize(label.pixmap().size())
        #label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        
        """ label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label.setScaledContents(True) """
        
        if index == 'last':
            self.scrollVLayout.addWidget(label)
            self.labels.append(label)
        else:
            self.scrollVLayout.insertWidget(index, label)
            self.labels.insert(index, label)

    def remove_ALL_label(self):
        for i in self.labels:
            """ self.scrollVLayout.removeWidget(i) """
            i.setParent(None)
        """ for i in range(0, self.scrollVLayout.count()):
            self.scrollVLayout.itemAt(i).widget().setParent(None) """
        self.labels = []
        self.label_pix = {}
        
    def zoomIn(self):
        self.set_scale(min(self.get_scale() + 0.2, 2))

    def zoomOut(self):
        self.set_scale(max(self.get_scale() - 0.2, 0.2))

    def normalSize(self):
        self.set_scale()

    def find_files(self, address):
        self.address = address
        supported_ext = ['.jpg', '.png', '.bmp', '.gif']
        self.accepted = []
        if address == '':
            return [] 
        os.chdir(address)
        for i in sorted(os.listdir()):
            for j in supported_ext:
                if i.find(j) != -1:
                    self.accepted += [i]
                    continue
        return self.accepted

    def create_from_list(self, list):
        for i in list:
            self.add_label(path = self.address + r'\\' + i)

    def load_images(self, dir):
        self.remove_ALL_label()
        self.create_from_list(self.find_files(dir))
        self.normalSize()
        self.scrollArea.verticalScrollBar().setValue(0)
        #self.statusBar().showMessage('loaded.')

    def load_images_from_waygate(self):
        self.load_images(str(QFileDialog.getExistingDirectory(self, "Open the Waygate")))

    def about(self):
        QMessageBox.about(self, 'duh', 'f u <br> k')
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MangaView()
    sys.exit(app.exec_())
