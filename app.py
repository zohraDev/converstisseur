import matplotlib.pyplot as plt
from PySide2 import QtWidgets

plt.figure()
import currency_converter


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Currency Convert")
        self.resize(600, 50)
        self.setup_ui()
        self.set_default_values()
        self.setup_connection()
        self.setup_css()

    def setup_ui(self):
        # initialize the element of  GUI
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.spn_montant = QtWidgets.QSpinBox()
        self.ccb_devisesTo = QtWidgets.QComboBox()
        self.spn_montant_converti = QtWidgets.QSpinBox()
        self.btn_inverse = QtWidgets.QPushButton("Inverse devise")
        # add the widget to the layout
        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.spn_montant)
        self.layout.addWidget(self.ccb_devisesTo)
        self.layout.addWidget(self.spn_montant_converti)
        self.layout.addWidget(self.btn_inverse)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list(self.c.currencies)))
        self.ccb_devisesTo.addItems(sorted(list(self.c.currencies)))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.ccb_devisesTo.setCurrentText("EUR")
        self.spn_montant.setRange(1, 10_000_000)
        self.spn_montant_converti.setRange(1, 10_000_000)
        self.spn_montant.setValue(100)
        self.spn_montant_converti.setValue(100)

    def setup_connection(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.ccb_devisesTo.activated.connect(self.compute)
        self.spn_montant.valueChanged.connect(self.compute)
        self.btn_inverse.clicked.connect(self.inverse_devise)

    def setup_css(self):
        self.setStyleSheet("""
        background-color:rgb(70,67, 67);  
        color:rgb(240, 240, 240);
        border: none;     
        """)
        self.btn_inverse.setStyleSheet("""
        background-color:rgb(78, 104, 49);
        font-weight: bold;
        """)




    def compute(self):
        # montant = self.spn_montant.value()
        try:
            result = self.c.convert(
                self.spn_montant.value(), self.cbb_devisesFrom.currentText(), self.ccb_devisesTo.currentText())
        except currency_converter.RateNotFoundError:
            print("The conversion does not work")
        else:
            self.spn_montant_converti.setValue(result)

    def inverse_devise(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.ccb_devisesTo.currentText()
        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.ccb_devisesTo.setCurrentText(devise_from)
        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()
