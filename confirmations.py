from PyQt5.QtWidgets import QMessageBox

class Confirmations(QMessageBox):
    def __init__(self, main):
        super().__init__()
        self.main = main
    
    #Dialogo acerca de
    def about_dialog(self):
        text = """
            <center>
            <h2>ToleWord</h2>
            </center>
            <h4>Version βeta</h4>
            <p> Copyright er pepe and et seech </p>
            """
        self.about( self.main, "ToleWord", text)

    #Dialogo de confirmación al salir de la aplicación
    def confirmation_dialog(self):
        return QMessageBox.question(
        self.main, "Confirmation", 
        "You have unsaved changes. Are you sure", 
        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)

    #Dialogo de confirmacion de borrar
    def delete_dialog(self):
        answer = QMessageBox.warning(self.main,"Warning", "Confirm delete?",QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        return answer