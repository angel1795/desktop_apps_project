from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from menu_toolbar import Menu_toolbar
from confirmations import Confirmations
from click_methods import Click_methods
import  markdown2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.confirmations = Confirmations(self)
        #Configuramos el lugar donde irá el texto
        self.text = QPlainTextEdit()
        self.text.document().setDefaultFont(QFont("Helvetica"))
        self.setCentralWidget(self.text)

        #Configuramos el explorador de archivos
        explorer = QDockWidget("Files explorer",self)
        self.addDockWidget(Qt.LeftDockWidgetArea, explorer)
        self.treev = QTreeView()
        self.filesm = QFileSystemModel(self.treev)
        self.filesm.setReadOnly(False)
        self.path = self.filesm.setRootPath("./")
        self.treev.setModel(self.filesm)
        explorer.setWidget(self.treev)

        #Configuramos la parte de MarkDown
        browser = QDockWidget("MarkDown Side", self)
        self.webview = QWebEngineView()
        browser.setWidget(self.webview)
        self.addDockWidget(Qt.RightDockWidgetArea, browser)


        #Menu toolbar y menu clicks
        self.menu_toolbar = Menu_toolbar(self, self.treev, self.text, self.filesm, self.webview)
        self.menu_file = self.menuBar().addMenu("&File")
        self.menu_help = self.menuBar().addMenu("&Help")
        self.menu_toolbar.submenus()

        #Las cabeceras del explorador de archivos no se ve bien a mi gusto
        # por lo que voy a hacer que la parte de los nombres sea más grande
        self.header = self.treev.header()
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.header.setSectionResizeMode(2, QHeaderView.Interactive)

        #Doble click y el click derecho
        self.click_methods = Click_methods(self, self.treev, self.filesm, self.text, self.webview, app)
        self.treev.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treev.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treev.doubleClicked.connect(self.click_methods.double_open)
        self.treev.customContextMenuRequested.connect(self.click_methods.r_click)
        

    #Evento para cuando la aplicación se cierra de cualquier manera
    def closeEvent(self, evt):
        if  self.text.document().isModified():
            answer = self.confirmations.confirmation_dialog()
            if answer == QMessageBox.Save:
                self.menu_toolbar.save()
            elif answer == QMessageBox.Cancel:
                evt.ignore()

    #Metodo para controlar el guardado si modificamos
    def save_if_modified(self):
        if  self.text.document().isModified():
            answer = self.confirmations.confirmation_dialog()
            if answer == QMessageBox.Save:
                self.menu_toolbar.save()
            elif answer == QMessageBox.Cancel:
                return False
    
    #Generar markdown
    def show_md(self):
        content = self.text.toPlainText()
        self.html = markdown2.markdown(content)
        self.webview.setHtml(self.html)
        self.webview.show()


if __name__=="__main__":
    app = QApplication([])
    app.setApplicationName("ToleWord")
    window = MainWindow()
    window.showMaximized()
    window.show()
    app.exec()