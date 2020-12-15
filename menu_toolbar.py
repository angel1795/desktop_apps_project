from PyQt5.QtWidgets import *
from confirmations import Confirmations
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QUrl
from confirmations import Confirmations
import os

#Clase para controlar los menus de arriba
class Menu_toolbar(QMenu):
    def __init__(self, main, treev, text, filesm, webview):
        super().__init__()
        self.main = main
        self.treev = treev
        self.text = text
        self.filesm = filesm
        self.webview = webview
        self.confirmations = Confirmations(main)

    def submenus(self):
        #Acerca de
        self.action_about = QAction("&About")
        self.action_about.triggered.connect(self.confirmations.about_dialog)
        self.main.menu_help.addAction(self.action_about)
        #Nuevo
        self.action_new = QAction("&New")
        self.action_new.setShortcut(QKeySequence.New)
        self.action_new.triggered.connect(self.new)
        self.main.menu_file.addAction(self.action_new)
        #Abrir
        self.action_open = QAction("&Open")
        self.action_open.setShortcut(QKeySequence.Open)
        self.action_open.triggered.connect(self.open_dialog)
        self.main.menu_file.addAction(self.action_open)
        #Guardar
        self.action_save = QAction("&Save")
        self.action_save.setShortcut(QKeySequence.Save)
        self.action_save.triggered.connect(self.save)
        self.main.menu_file.addAction(self.action_save)
        #Guardar como
        self.action_saveas = QAction("S&ave as")
        self.action_saveas.setShortcut(QKeySequence.SaveAs)
        self.action_saveas.triggered.connect(self.save_dialog)
        self.main.menu_file.addAction(self.action_saveas)
        #Cerrar
        self.action_close = QAction("&Close")
        self.action_close.setShortcut(QKeySequence.Close)
        self.action_close.triggered.connect(self.main.close)
        self.main.menu_file.addAction(self.action_close)

    #Metodo para guardado rapido
    def save(self):
        if self.main.file_path:
            with open(self.main.file_path, 'w') as f:
                f.write(self.text.toPlainText())
            self.text.document().setModified(False)
            self.main.show_md()
        else:
            self.save_dialog()

    #Metodo para guardar como
    def save_dialog(self):
        self.filename, _ = QFileDialog.getSaveFileName(self.main,
                    "Save File...",
                    os.getcwd(),
                    "Text Files (*.txt *.py)"
                  )
        if self.filename: 
            with open(self.filename, 'w') as f:
                f.write(self.text.toPlainText())
            self.text.document().setModified(False)
            self.main.show_md()
            self.main.file_path = self.filename

    #Metodo para abrir archivo
    def new(self):
        if self.main.save_if_modified()==False:
            return
        else:
            self.text.clear()
            self.webview.setHtml("")
        self.main.file_path = None


    #Metodo para abrir el dialogo de abrir el archivo
    def open_dialog(self):        
        if self.main.save_if_modified() == False:
            return
        else:    
            self.filename, _ = QFileDialog.getOpenFileName(self.main,
                            "Open File...",
                            os.getcwd(),
                            "Text Files (*.txt *.py)"
                        )
            if self.filename:
                with open(self.filename, 'r') as f:
                    self.text.setPlainText(f.read())
                self.main.file_path = self.filename   
                self.main.show_md()

    



    