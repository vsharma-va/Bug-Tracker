from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QMimeData, QEvent
from PyQt5 import QtCore
import sys
import custom_list_item
import Src.data_handling.data as data_handling


class ListWidget(QListWidget):
    itemDraggedSignal = QtCore.pyqtSignal()
    itemDroppedSignal = QtCore.pyqtSignal()
    itemEnteredSignal = QtCore.pyqtSignal()
    itemDeleteSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(ListWidget, self).__init__()
        self.dataClass = data_handling.Data()
        self.setWindowFlags(self.windowFlags() | ~Qt.CustomizeWindowHint)
        self.setFrameShape(QFrame.WinPanel)
        self.setFrameShadow(QFrame.Sunken)
        # self.setMovement(QListView.Free)
        self.setDragEnabled(True)
        self.setResizeMode(QListView.Adjust)
        self.setDragDropMode(QAbstractItemView.DragDrop)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionRectVisible(True)
        self.setVerticalScrollBar(QScrollBar())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setProperty("isWrapping", True)
        self.setWordWrap(True)
        self.setSortingEnabled(True)
        self.setAcceptDrops(True)

    @classmethod
    def getData(self, heading: str, description: str, tagColor: str, tagName: str):
        self.heading = heading
        self.description = description
        self.tagColor = tagColor
        self.tagName = tagName

    def dragEnterEvent(self, event):
        # first accept the drag event
        # right now it accepts all the drag events
        print('entering')
        self.itemEnteredSignal.emit()
        mimeData = QMimeData()
        mimeData.setText("QWidget")
        event.accept()

    def dragMoveEvent(self, event):
        # emits the itemDraggedSignal
        self.itemDraggedSignal.emit()
        event.accept()

    def dropEvent(self, event):
        # then when the item is dropped create a new widget with the same content as the widget dropped
        # and add it to the QListWidget
        event.setDropAction(Qt.MoveAction)
        # event.source() is not self is to check if the item is dropped into the same list widget from which it was
        # dragged. If that is true then a new item is not created.
        if event.source() is not self:
            print('starting')
            # creates a new list item whenever according to the data received by getData from _itemPressed slot
            # functions from gui.py file
            item = QListWidgetItem(self)
            self.itemDroppedSignal.emit()
            x = custom_list_item.ListItem(self)
            x.setHeading(self.heading)
            x.setDescription(self.description)
            x.setTag(self.tagColor, self.tagName)
            item.setSizeHint(x.size())
            self.addItem(item)
            self.setItemWidget(item, x)
            event.accept()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            menu = QMenu()
            delete = QAction('Delete')
            menu.addAction(delete)
            menuClick = menu.exec_(event.globalPos())
            if menuClick == delete:
                self.itemDeleteSignal.emit()
            return True
        return super(ListWidget, self).eventFilter(source, event)


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
    dlgMain = ListWidget()
    dlgMain.show()
    sys.exit(app.exec_())
