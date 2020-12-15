from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor
from menu_toolbar import Menu_toolbar
from confirmations import Confirmations
import os

class Click_methods(QMenu):
    def __init__(self,main,treev,filesm,app,text, webview):
        super().__init__()
        self.menu_toolbar = Menu_toolbar(main, treev, filesm, text, webview)
        self.treev = treev
        self.main = main
        self.filesm = filesm
        self.text = text
        self.app = app
        self.webview = webview
        self.confirmations = Confirmations(main)
        self.index_path = None
        self.index = None

    #Evento haciendo doble click
    def double_open(self, index):
        self.index = index
        self.index_path = self.filesm.filePath(index)
        if os.path.isdir(self.index_path):
            return
        else:
            self.open_file(self.index_path)
        

    def r_click(self, point):
        self.mmm = QMenu(self)
        #Abrir
        action_open = QAction("Open")
        action_open.triggered.connect(self.check_open)
        self.mmm.addAction(action_open)
        #Renombrar
        action_rename = QAction("Rename")
        action_rename.triggered.connect(self.rename_file)
        self.mmm.addAction(action_rename)
        #Eliminar
        action_delete = QAction("Delete")
        action_delete.triggered.connect(self.delete_th)
        self.mmm.addAction(action_delete)
        #Copiar
        action_copy = QAction("Copy")
        action_copy.triggered.connect(self.copy)
        self.mmm.addAction(action_copy)
        self.mmm.exec_(self.treev.mapToGlobal(point))

    #Metodo para copiar al portapapeles
    def copy(self):
        self.index = self.treev.currentIndex()
        self.index_path = self.filesm.filePath(self.index)
        self.text.clipboard().setText(self.index_path)


    #Metodo para borrar
    def delete_th(self):
        self.index = self.treev.currentIndex()
        self.index_path = self.filesm.filePath(self.index)
        asnwer = self.confirmations.delete_dialog()
        if asnwer == QMessageBox.Yes:
            os.remove(self.index_path)
        else:
            return
    #Metodo para renombrar
    def rename_file(self):
        self.index = self.treev.currentIndex()
        self.treev.edit(self.index)


    #Primer paso de abrir
    def check_open(self):
        self.index = self.treev.currentIndex()
        self.index_path = self.filesm.filePath(self.index)
        self.open_file(self.index_path)

    #Abrir el archivo 
    def open_file(self, path):
        if os.path.isdir(path):
            self.treev.expand(self.index)
        else:
            if self.main.save_if_modified() == False:
                return
            else:    
                with open(path, 'r') as f:
                    self.main.text.setPlainText(f.read())
                self.main.file_path = path
                self.menu_toolbar.filename = path
                self.main.show_md()   

    