from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys


class ListItem(QWidget):
    def __init__(self, *args, **kwargs):
        super(ListItem, self).__init__(*args, **kwargs)
        uic.loadUi('../../UI/List_Item.ui', self)
        self.setWindowFlags(self.windowFlags() | ~Qt.CustomizeWindowHint)
        # get widgets
        self.lblHeading = self.findChild(QLabel, 'lblHeading')
        self.txtBrowDescription = self.findChild(QTextBrowser, 'txtBrowDescription')
        self.lblTagName = self.findChild(QLabel, 'lblTagName')
        self.lblTagName.setAttribute(Qt.WA_StyledBackground, True)

    def setHeading(self, heading: str):
        self.lblHeading.setText(heading)

    def setDescription(self, description: str):
        self.txtBrowDescription.setText(description)

    def setTag(self, color: str, text: str):
        colorName = color
        self.lblTagName.setText(text)
        self.lblTagName.setStyleSheet(
            'border: 1px solid black; border-radius: 10px; background-color: {0};'.format(colorName))


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlgMain = ListItem()
    dlgMain.show()
    sys.exit(app.exec_())
