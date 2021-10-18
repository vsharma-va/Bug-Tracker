from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5 import uic
import sys
import Src.gui.custom_list_item as custom_list_item
import Src.gui.custom_list_widget as custom_list_widget
import Src.data_handling.data as data_handling
from PyQt5.QtChart import QChart, QPieSeries, QChartView, QPieSlice
import UI.images_rc

# just testing
# git pull
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class DlgMain(QMainWindow):
    dataClass = data_handling.Data()

    def __init__(self):
        super(DlgMain, self).__init__()
        uic.loadUi('../../UI/Main_Window.ui', self)
        self.FirstTab()
        self.SecondTab()

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.frmSideBar = self.findChild(QFrame, 'frmSideBar')

        self.tabWidget.currentChanged.connect(self.evt_tabWidget_currentChanged)

    def openMainWindowSideBar(self):
        currentHeightFrm = self.frmSideBar.height()
        animationSidebar = QPropertyAnimation(self.frmSideBar, b"maximumWidth")
        animationSidebar.setDuration(500)
        animationSidebar.setStartValue(currentHeightFrm)
        animationSidebar.setEndValue(150)
        animationSidebar.setEasingCurve(QEasingCurve.InQuart)

        currentHeightAddProject = self.btnAddProject.height()
        animationAddProjectButton = QPropertyAnimation(self.btnAddProject, b"maximumWidth")
        animationAddProjectButton.setDuration(500)
        animationAddProjectButton.setStartValue(currentHeightAddProject)
        animationAddProjectButton.setEndValue(150)
        animationAddProjectButton.setEasingCurve(QEasingCurve.InQuart)

        currentHeightSelectProject = self.btnSelectProject.height()
        animationSelectProjectButton = QPropertyAnimation(self.btnSelectProject, b"maximumWidth")
        animationSelectProjectButton.setDuration(500)
        animationSelectProjectButton.setStartValue(currentHeightSelectProject)
        animationSelectProjectButton.setEndValue(150)
        animationSelectProjectButton.setEasingCurve(QEasingCurve.InQuart)

        currentHeightMenuBtn = self.btnMenu.height()
        animationMenu = QPropertyAnimation(self.btnMenu, b"maximumWidth")
        animationMenu.setDuration(500)
        animationMenu.setStartValue(currentHeightMenuBtn)
        animationMenu.setEndValue(150)
        animationMenu.setEasingCurve(QEasingCurve.InQuart)

        group = QParallelAnimationGroup(self.frmSideBar)
        group.addAnimation(animationSidebar)
        group.addAnimation(animationAddProjectButton)
        group.addAnimation(animationSelectProjectButton)
        group.addAnimation(animationMenu)
        group.start()

        self.fadeWidgetOut(self.tabWidget)

        self.makeWidgetUnselectable(self.tabWidget)

    def closeMainWindowSideBar(self):
        currentHeightFrm = self.frmSideBar.width()
        animationSidebar = QPropertyAnimation(self.frmSideBar, b"maximumWidth")
        animationSidebar.setDuration(500)
        animationSidebar.setStartValue(currentHeightFrm)
        animationSidebar.setEndValue(40)
        animationSidebar.setEasingCurve(QEasingCurve.InQuart)

        currentHeightAddProject = self.btnAddProject.width()
        animationAddProjectButton = QPropertyAnimation(self.btnAddProject, b"maximumWidth")
        animationAddProjectButton.setDuration(500)
        animationAddProjectButton.setStartValue(currentHeightAddProject)
        animationAddProjectButton.setEndValue(0)
        animationAddProjectButton.setEasingCurve(QEasingCurve.InQuart)

        currentHeightSelectProject = self.btnSelectProject.width()
        animationSelectProjectButton = QPropertyAnimation(self.btnSelectProject, b"maximumWidth")
        animationSelectProjectButton.setDuration(500)
        animationSelectProjectButton.setStartValue(currentHeightSelectProject)
        animationSelectProjectButton.setEndValue(0)
        animationSelectProjectButton.setEasingCurve(QEasingCurve.InQuart)

        currentHeightMenuBtn = self.btnMenu.width()
        animationMenu = QPropertyAnimation(self.btnMenu, b"maximumWidth")
        animationMenu.setDuration(500)
        animationMenu.setStartValue(currentHeightMenuBtn)
        animationMenu.setEndValue(40)
        animationMenu.setEasingCurve(QEasingCurve.InQuart)

        group = QParallelAnimationGroup(self.frmSideBar)
        group.addAnimation(animationSidebar)
        group.addAnimation(animationAddProjectButton)
        group.addAnimation(animationSelectProjectButton)
        group.addAnimation(animationMenu)
        group.start()

        self.fadeWidgetOut(self.tabWidget)

        self.makeWidgetSelectable(self.tabWidget)

    def evt_btnMenu_clicked(self):
        if self.frmSideBar.width() == 40:
            self.openMainWindowSideBar()
        elif self.frmSideBar.width() > 40:
            self.closeMainWindowSideBar()

    def evt_tabWidget_currentChanged(self):
        self.displayRecentAdditions()
        self.displayPieChart()

    def FirstTab(self):
        self.wiPieChart = self.findChild(QChartView, 'wiPieChart')
        self.wiLineChart = self.findChild(QChartView, 'wiLineChart')
        self.frmPieChart = self.findChild(QFrame, 'frmPieChart')
        self.tblRecentAdditions = self.findChild(QTableWidget, 'tblRecentAdditions')
        self.btnMenu = self.findChild(QPushButton, 'btnMenu')
        self.btnAddProject = self.findChild(QPushButton, 'btnAddProject')
        self.btnSelectProject = self.findChild(QPushButton, 'btnSelectProject')

        self.btnMenu.clicked.connect(self.evt_btnMenu_clicked)

        self.displayPieChart()
        self.displayRecentAdditions()

    def displayPieChart(self):
        recordsCount = self.dataClass.countRecords()
        openCount = recordsCount[0]
        progressCount = recordsCount[1]
        testedCount = recordsCount[2]
        reopenCount = recordsCount[3]
        closedCount = recordsCount[4]

        series1 = QPieSeries()
        series1.append('Open', openCount)
        series1.append('In Progress', progressCount)
        series1.append('In Testing', testedCount)
        series1.append('Reopened', reopenCount)
        series1.append('Closed', closedCount)
        series1.setLabelsVisible(True)

        series1.setLabelsPosition(QPieSlice.LabelInsideHorizontal)
        for x in series1.slices():
            x.setLabel("{:.2f}%".format(100 * x.percentage()))

        chart = QChart()
        chart.legend()
        chart.addSeries(series1)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Stats")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.legend().markers(series1)[0].setLabel("Open")
        chart.legend().markers(series1)[1].setLabel("In Progress")
        chart.legend().markers(series1)[2].setLabel("In Testing")
        chart.legend().markers(series1)[3].setLabel("Reopened")
        chart.legend().markers(series1)[4].setLabel("Closed")

        self.wiPieChart.setChart(chart)

    def displayRecentAdditions(self):
        items = self.dataClass.returnTopFiveItems()
        names = items[0]
        descriptions = items[1]
        tagNames = items[2]

        row = 0
        column = 0
        if len(names) != 0:
            self.tblRecentAdditions.blockSignals(True)
            self.tblRecentAdditions.setRowCount(0)
            self.tblRecentAdditions.setRowCount(len(names))
            self.tblRecentAdditions.setColumnCount(3)
            for i in range(len(names)):
                self.tblRecentAdditions.setItem(row, column, QTableWidgetItem(names[i]))
                row += 1
            row = 0
            column += 1
            for i in range(len(descriptions)):
                self.tblRecentAdditions.setItem(row, column, QTableWidgetItem(descriptions[i]))
                row += 1
            row = 0
            column += 1
            for i in range(len(tagNames)):
                self.tblRecentAdditions.setItem(row, column, QTableWidgetItem(tagNames[i]))
                row += 1
            row = 0

        self.tblRecentAdditions.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def SecondTab(self):
        # used to store a number representing one of the list widgets
        self.whichListWidget = []
        self.tagColor = QColor(0, 0, 0, 0)
        # used to correct the row number of the dropped item in the csv
        self.callCorrectionFunction = True

        # widgets
        self.frmPullUp = self.findChild(QFrame, 'frmPullUp')
        self.frmPullUp_Tags = self.findChild(QFrame, 'frmTags')
        self.frmAdd = self.findChild(QFrame, 'frmAdd')
        self.frmLbl = self.findChild(QFrame, 'frmLbl')
        self.frmLstWid = self.findChild(QFrame, 'frmLstWid')
        self.btnAddOpen = self.findChild(QPushButton, 'btnAddOpen')
        self.btnAddProgress = self.findChild(QPushButton, 'btnAddProgress')
        self.btnAddTested = self.findChild(QPushButton, 'btnAddTested')
        self.btnAddReopen = self.findChild(QPushButton, 'btnAddReopen')
        self.btnAddClosed = self.findChild(QPushButton, 'btnAddClosed')
        self.btnConfirmAddition = self.findChild(QPushButton, 'btnConfirmAddition')
        self.btnCancelAddition = self.findChild(QPushButton, 'btnCancelAddition')
        self.btnSelectColor = self.findChild(QPushButton, 'btnSelectColor')
        self.lstWidOpen = custom_list_widget.ListWidget()
        self.txtBrowDescription = self.findChild(QTextBrowser, 'txtBrowDescription')
        self.linName = self.findChild(QLineEdit, 'linName')
        self.cmbTag = self.findChild(QComboBox, 'cmbTag')

        # instantiating the list widgets by calling the created class
        self.lstWidProgress = custom_list_widget.ListWidget()
        self.lstWidTested = custom_list_widget.ListWidget()
        self.lstWidReopen = custom_list_widget.ListWidget()
        self.lstWidClose = custom_list_widget.ListWidget()

        # added to a horizontal layout
        self.frmListWidLayout = QHBoxLayout()
        self.frmListWidLayout.addWidget(self.lstWidOpen)
        self.frmListWidLayout.addWidget(self.lstWidProgress)
        self.frmListWidLayout.addWidget(self.lstWidTested)
        self.frmListWidLayout.addWidget(self.lstWidReopen)
        self.frmListWidLayout.addWidget(self.lstWidClose)

        # then they are added to the widget frame
        self.frmListWidLayout.setSpacing(0)
        self.frmListWidLayout.setContentsMargins(0, 0, 0, 0)
        self.frmLstWid.setLayout(self.frmListWidLayout)

        # function used to load the data from csv at startup
        # important to call this function before checking for signals
        self.loadWidgetsToListView()

        '''#################################SIGNALS#####################################'''
        # these signals are used to open and close the bottom slider
        # and also to send data entered by user to self.addListWidget to create a new list item
        self.btnAddOpen.clicked.connect(self.evt_btnAddOpen_clicked)
        self.btnAddProgress.clicked.connect(self.evt_btnAddProgress_clicked)
        self.btnAddTested.clicked.connect(self.evt_btnAddTested_clicked)
        self.btnAddReopen.clicked.connect(self.evt_btnAddReopen_clicked)
        self.btnAddClosed.clicked.connect(self.evt_btnAddClosed_clicked)
        self.btnConfirmAddition.clicked.connect(self.evt_btnConfirmAddition_clicked)
        self.btnCancelAddition.clicked.connect(self.evt_btnCancelAddition_clicked)
        self.btnSelectColor.clicked.connect(self.evt_btnSelectColor_clicked)

        # these signals are used to send the row number of the item which is pressed
        self.lstWidOpen.itemPressed.connect(self.evt_lstWidOpen_itemPressed)
        self.lstWidProgress.itemPressed.connect(self.evt_lstWidProgress_itemPressed)
        self.lstWidTested.itemPressed.connect(self.evt_lstWidTested_itemPressed)
        self.lstWidReopen.itemPressed.connect(self.evt_lstWidReopen_itemPressed)
        self.lstWidClose.itemPressed.connect(self.evt_lstWidClose_itemPressed)

        # custom signal that is emitted whenever the user drags the item to another list widget
        # signal emitted in custom_list_widget.py under dragEnterEvent function
        self.lstWidOpen.itemEnteredSignal.connect(self.evt_lstWidOpen_itemEntered)
        self.lstWidProgress.itemEnteredSignal.connect(self.evt_lstWidProgress_itemEntered)
        self.lstWidTested.itemEnteredSignal.connect(self.evt_lstWidTested_itemEntered)
        self.lstWidReopen.itemEnteredSignal.connect(self.evt_lstWidReopen_itemEntered)
        self.lstWidClose.itemEnteredSignal.connect(self.evt_lstWidClose_itemEntered)

        # custom signal that is emitted whenever the user drops the data in another list widget
        # custom signal emitted in custom_list_widget.py under dropEvent function
        self.lstWidOpen.itemDroppedSignal.connect(self.evt_itemDropped)
        self.lstWidProgress.itemDroppedSignal.connect(self.evt_itemDropped)
        self.lstWidTested.itemDroppedSignal.connect(self.evt_itemDropped)
        self.lstWidReopen.itemDroppedSignal.connect(self.evt_itemDropped)
        self.lstWidClose.itemDroppedSignal.connect(self.evt_itemDropped)

        # signal that is emitted just before an item is inserted
        # used with callCorrectionFunction bool to send the correct row number to data.py
        self.lstWidOpen.model().rowsAboutToBeInserted.connect(self.evt_lstWidOpen_aboutToInsert)
        self.lstWidProgress.model().rowsAboutToBeInserted.connect(self.evt_lstWidProgress_aboutToInsert)
        self.lstWidTested.model().rowsAboutToBeInserted.connect(self.evt_lstWidProgress_aboutToInsert)
        self.lstWidReopen.model().rowsAboutToBeInserted.connect(self.evt_lstWidReopen_aboutToInsert)
        self.lstWidClose.model().rowsAboutToBeInserted.connect(self.evt_lstWidClose_aboutToInsert)

        self.lstWidOpen.itemDeleteSignal.connect(self.evt_lstWidOpen_itemDelete)
        self.lstWidProgress.itemDeleteSignal.connect(self.evt_lstWidProgress_itemDelete)
        self.lstWidTested.itemDeleteSignal.connect(self.evt_lstWidTested_itemDelete)
        self.lstWidReopen.itemDeleteSignal.connect(self.evt_lstWidReopen_itemDelete)
        self.lstWidClose.itemDeleteSignal.connect(self.evt_lstWidClose_itemDelete)

    '''############################GUI FUNCTIONS###########################################'''

    # this function loads saved data
    def loadWidgetsToListView(self):
        data = self.dataClass.loadListWidgetsItems()
        openData = data[0]  # [lstWidOpen, lstWidProgress, lstWidTested, lstWidReopen, lstWidClose]
        progressData = data[1]
        testedData = data[2]
        reopenData = data[3]
        closeData = data[4]
        if len(openData) != 0:
            for i in range(len(openData)):
                self.whichListWidget.clear()
                self.whichListWidget.append(0)
                self.addWidgetToListView(self.lstWidOpen, openData[-i-1][0].strip(), openData[-i-1][1].strip(), openData[-i-1][2].strip(),
                                         openData[-i-1][3].strip())

        if len(progressData) != 0:
            for i in range(len(progressData)):
                self.whichListWidget.clear()
                self.whichListWidget.append(1)
                self.addWidgetToListView(self.lstWidProgress, progressData[-i - 1][0].strip(),
                                         progressData[-i - 1][1].strip(), progressData[-i - 1][2].strip(),
                                         progressData[-i - 1][3].strip())

        if len(testedData) != 0:
            for i in range(len(testedData)):
                self.whichListWidget.clear()
                self.whichListWidget.append(2)
                self.addWidgetToListView(self.lstWidTested, testedData[-i - 1][0].strip(), testedData[-i - 1][1].strip(),
                                         testedData[-i - 1][2].strip(), testedData[-i - 1][3].strip())

        if len(reopenData) != 0:
            self.whichListWidget.clear()
            self.whichListWidget.append(3)
            for i in range(len(reopenData)):
                self.addWidgetToListView(self.lstWidReopen, reopenData[-i - 1][0].strip(), reopenData[-i - 1][1].strip(),
                                         reopenData[-i - 1][2].strip(), reopenData[-i - 1][3].strip())

        if len(closeData) != 0:
            self.whichListWidget.clear()
            self.whichListWidget.append(4)
            for i in range(len(closeData)):
                self.addWidgetToListView(self.lstWidClose, closeData[-i - 1][0].strip(), closeData[-i - 1][1].strip(),
                                         closeData[-i - 1][2].strip(), closeData[-i - 1][3].strip())

    # creates the list item and stores its data
    def addWidgetToListView(self, listWidget: QListWidget, heading: str, description: str, color: str = '',
                            tagName: str = ''):
        # first create an empty item for the list widget
        Item = QListWidgetItem(listWidget)
        # instantiate your custom widget
        listItem = custom_list_item.ListItem()
        listItem.setHeading(heading)
        listItem.setDescription(description)
        if len(color) == 0 and len(tagName) == 0:
            # store the data
            listItem.setTag(self.tagColor.name(), self.cmbTag.currentText())
            self.dataClass.newWidgetStoreData(heading, description, str(self.tagColor.name()),
                                              self.cmbTag.currentText(), self.whichListWidget[0])
        else:
            listItem.setTag(color, tagName)
        # set the size of the empty item to the size of your custom widget
        Item.setSizeHint(listItem.size())
        # add the empty item to the list widget
        listWidget.addItem(Item)
        # now put the custom widget inside the empty item
        # which is now present inside the list widget
        listWidget.setItemWidget(Item, listItem)

    def closeAnimationPullUpFrame(self):
        currentHeight = self.frmPullUp.height()

        animation = QPropertyAnimation(self.frmPullUp, b"maximumHeight")
        animation.setDuration(750)
        animation.setStartValue(currentHeight)
        animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuart)

        group = QParallelAnimationGroup(self.frmPullUp)
        group.addAnimation(animation)
        group.start()

        self.fadeWidgetIn(self.frmAdd)
        self.fadeWidgetIn(self.frmLbl)
        self.fadeWidgetIn(self.frmLstWid)

        self.makeWidgetSelectable(self.frmAdd)
        self.makeWidgetSelectable(self.frmLbl)
        self.makeWidgetSelectable(self.frmLstWid)

    def openAnimationPullUpFrame(self):
        currentHeight = self.frmPullUp.height()

        animation = QPropertyAnimation(self.frmPullUp, b"maximumHeight")
        animation.setDuration(500)
        animation.setStartValue(currentHeight)
        animation.setEndValue(450)
        animation.setEasingCurve(QEasingCurve.InQuart)

        group = QParallelAnimationGroup(self.frmPullUp)
        group.addAnimation(animation)
        group.start()

        self.fadeWidgetOut(self.frmAdd)
        self.fadeWidgetOut(self.frmLbl)
        self.fadeWidgetOut(self.frmLstWid)

        self.makeWidgetUnselectable(self.frmAdd)
        self.makeWidgetUnselectable(self.frmLbl)
        self.makeWidgetUnselectable(self.frmLstWid)

    def fadeWidgetOut(self, widget: QWidget):
        opacityEffect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacityEffect)

        opacityAnimation = QPropertyAnimation(opacityEffect, b"opacity")
        opacityAnimation.setDuration(750)
        opacityAnimation.setStartValue(1)
        opacityAnimation.setEndValue(0.5)

        group = QParallelAnimationGroup(widget)
        group.addAnimation(opacityAnimation)
        group.start()

    def fadeWidgetIn(self, widget: QWidget):
        opacityEffect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacityEffect)

        opacityAnimation = QPropertyAnimation(opacityEffect, b"opacity")
        opacityAnimation.setDuration(750)
        opacityAnimation.setStartValue(0.5)
        opacityAnimation.setEndValue(1)

        group = QParallelAnimationGroup(widget)
        group.addAnimation(opacityAnimation)
        group.start()

    def makeWidgetUnselectable(self, widget: QFrame):
        widget.setEnabled(False)

    def makeWidgetSelectable(self, widget: QFrame):
        widget.setEnabled(True)

    '''###########################DATA FUNCTIONS#################################################'''

    def getListItemData(self, listWidget: QWidget, whichList: int):
        listItemData = self.dataClass.returnListWidgetsItemsData(listWidget.currentRow(), whichList)
        listItemName = listItemData[0].strip(' ')
        listItemDescription = listItemData[1].strip(' ')
        listItemColor = listItemData[2].strip(' ')
        offset = 0
        print(listItemData)
        # if two more than two spaces are typed while typing the tag name these blank strings are created when splitting
        # this for loop removes those blank strings, and every time it adds it to offset.
        # normally the tag name will start from the third index, but when empty strings are created they are pushed back
        # therefore that offset is added to the number 3.
        # then every element after offset + 3 is converted into a string and returned
        for i in range(len(listItemData)):
            if listItemData[i] == '':
                offset += 1
            if i == 3 + offset:
                listItemTag = ' '.join(listItemData[i:])
        return [listItemName, listItemDescription, listItemColor, listItemTag]

    def clearAllListWidgets(self):
        self.lstWidOpen.clear()
        self.lstWidProgress.clear()
        self.lstWidTested.clear()
        self.lstWidReopen.clear()
        self.lstWidClose.clear()

    '''##################################EVENTS############################################'''

    def evt_btnAddOpen_clicked(self):
        self.callCorrectionFunction = False
        self.openAnimationPullUpFrame()
        self.whichListWidget.clear()
        self.whichListWidget.append(0)

    def evt_btnAddProgress_clicked(self):
        self.callCorrectionFunction = False
        self.openAnimationPullUpFrame()
        self.whichListWidget.clear()
        self.whichListWidget.append(1)

    def evt_btnAddTested_clicked(self):
        self.callCorrectionFunction = False
        self.openAnimationPullUpFrame()
        self.whichListWidget.clear()
        self.whichListWidget.append(2)

    def evt_btnAddReopen_clicked(self):
        self.callCorrectionFunction = False
        self.openAnimationPullUpFrame()
        self.whichListWidget.clear()
        self.whichListWidget.append(3)

    def evt_btnAddClosed_clicked(self):
        self.callCorrectionFunction = False
        self.openAnimationPullUpFrame()
        self.whichListWidget.clear()
        self.whichListWidget.append(4)

    def evt_btnConfirmAddition_clicked(self):
        self.closeAnimationPullUpFrame()
        # creates the list items for respective list widgets
        if self.whichListWidget[0] == 0:
            self.addWidgetToListView(self.lstWidOpen, self.linName.text(), self.txtBrowDescription.toPlainText())
        elif self.whichListWidget[0] == 1:
            self.addWidgetToListView(self.lstWidProgress, self.linName.text(), self.txtBrowDescription.toPlainText())
        elif self.whichListWidget[0] == 2:
            self.addWidgetToListView(self.lstWidTested, self.linName.text(), self.txtBrowDescription.toPlainText())
        elif self.whichListWidget[0] == 3:
            self.addWidgetToListView(self.lstWidReopen, self.linName.text(), self.txtBrowDescription.toPlainText())
        elif self.whichListWidget[0] == 4:
            self.addWidgetToListView(self.lstWidClose, self.linName.text(), self.txtBrowDescription.toPlainText())

    def evt_btnCancelAddition_clicked(self):
        self.closeAnimationPullUpFrame()

    def evt_btnSelectColor_clicked(self):
        colorDialog = QColorDialog(self)
        self.tagColor = colorDialog.getColor()

    # itemPressed slots
    # whenever the list item is clicked a snapshot of it is sent to the getData function in custom_list_widget.py
    # so whenever that item is dragged and dropped to another list widget, custom_list_widget.py creates a new list
    # item based on the data. Same for all _itemPressed functions
    def evt_lstWidOpen_itemPressed(self, item):
        listItemData = self.getListItemData(self.lstWidOpen, 0)
        listItemName = listItemData[0]
        listItemDescription = listItemData[1]
        listItemColor = listItemData[2]
        listItemTag = listItemData[3]
        custom_list_widget.ListWidget.getData(listItemName, listItemDescription, listItemColor, listItemTag)

        self.callCorrectionFunction = True
        print('evt_lstWidOpen_itemPressed')
        self.dataClass.setRemovedItemIndex(self.lstWidOpen.row(item))
        self.dataClass.setListRemoved(0)

    def evt_lstWidProgress_itemPressed(self, item):
        listItemData = self.getListItemData(self.lstWidProgress, 1)
        listItemName = listItemData[0]
        listItemDescription = listItemData[1]
        listItemColor = listItemData[2]
        listItemTag = listItemData[3]

        custom_list_widget.ListWidget.getData(listItemName, listItemDescription, listItemColor, listItemTag)

        self.callCorrectionFunction = True
        print('evt_lstWidProgress_itemPressed')
        self.dataClass.setRemovedItemIndex(self.lstWidProgress.row(item))
        self.dataClass.setListRemoved(1)

    def evt_lstWidTested_itemPressed(self, item):
        listItemData = self.getListItemData(self.lstWidTested, 2)
        listItemName = listItemData[0]
        listItemDescription = listItemData[1]
        listItemColor = listItemData[2]
        listItemTag = listItemData[3]

        custom_list_widget.ListWidget.getData(listItemName, listItemDescription, listItemColor, listItemTag)

        self.callCorrectionFunction = True
        print('evt_lstWidTested_itemPressed')
        self.dataClass.setRemovedItemIndex(self.lstWidTested.row(item))
        self.dataClass.setListRemoved(2)

    def evt_lstWidReopen_itemPressed(self, item):
        listItemData = self.getListItemData(self.lstWidReopen, 3)
        listItemName = listItemData[0]
        listItemDescription = listItemData[1]
        listItemColor = listItemData[2]
        listItemTag = listItemData[3]

        custom_list_widget.ListWidget.getData(listItemName, listItemDescription, listItemColor, listItemTag)

        self.callCorrectionFunction = True
        print('evt_lstWidReopen_itemPressed')
        self.dataClass.setRemovedItemIndex(self.lstWidReopen.row(item))
        self.dataClass.setListRemoved(3)

    def evt_lstWidClose_itemPressed(self, item):
        listItemData = self.getListItemData(self.lstWidClose, 4)
        listItemName = listItemData[0]
        listItemDescription = listItemData[1]
        listItemColor = listItemData[2]
        listItemTag = listItemData[3]
        custom_list_widget.ListWidget.getData(listItemName, listItemDescription, listItemColor, listItemTag)

        self.callCorrectionFunction = True
        print('evt_lstWidClose_itemPressed')
        self.dataClass.setRemovedItemIndex(self.lstWidClose.row(item))
        self.dataClass.setListRemoved(4)

    # this is the slot for the signal itemEntered
    # whenever the item enters a new list widget, it sends the index of the list widget to a function in data.py
    # the currentRow returns 0 because the item hasn't yet been dropped into list widget
    def evt_lstWidOpen_itemEntered(self):
        self.dataClass.setInsertedItemIndex(self.lstWidOpen.currentRow())
        self.dataClass.setListInserted(0)

    def evt_lstWidProgress_itemEntered(self):
        self.dataClass.setInsertedItemIndex(self.lstWidProgress.currentRow())
        self.dataClass.setListInserted(1)

    def evt_lstWidTested_itemEntered(self):
        self.dataClass.setInsertedItemIndex(self.lstWidTested.currentRow())
        self.dataClass.setListInserted(2)

    def evt_lstWidReopen_itemEntered(self):
        self.dataClass.setInsertedItemIndex(self.lstWidReopen.currentRow())
        self.dataClass.setListInserted(3)

    def evt_lstWidClose_itemEntered(self):
        self.dataClass.setInsertedItemIndex(self.lstWidClose.currentRow())
        self.dataClass.setListInserted(4)

    # this signal is emitted whenever the item is dropped into a list widget
    # since this signal is emitted before aboutToInsert signal the function in data.py just adds the item at the last
    # index in the csv
    def evt_itemDropped(self):
        self.dataClass.switchListWidgetsItem()

    # when this signal is emitted the item has been registered by the list widget, therefore now I can send its correct
    # index. The function in data.py takes the data and puts it at the correct index
    def evt_lstWidOpen_aboutToInsert(self, model, rowIndex, columnIndex):
        if self.callCorrectionFunction:
            self.dataClass.setInsertedItemIndex(rowIndex)
            self.dataClass.switchListWidgetsItem(True, True)

    def evt_lstWidProgress_aboutToInsert(self, model, rowIndex, columnIndex):
        if self.callCorrectionFunction:
            self.dataClass.setInsertedItemIndex(rowIndex)
            self.dataClass.switchListWidgetsItem(True, True)

    def evt_lstWidTested_aboutToInsert(self, model, rowIndex, columnIndex):
        if self.callCorrectionFunction:
            self.dataClass.setInsertedItemIndex(rowIndex)
            self.dataClass.switchListWidgetsItem(True, True)

    def evt_lstWidReopen_aboutToInsert(self, model, rowIndex, columnIndex):
        if self.callCorrectionFunction:
            self.dataClass.setInsertedItemIndex(rowIndex)
            self.dataClass.switchListWidgetsItem(True, True)

    def evt_lstWidClose_aboutToInsert(self, model, rowIndex, columnIndex):
        if self.callCorrectionFunction:
            self.dataClass.setInsertedItemIndex(rowIndex)
            self.dataClass.switchListWidgetsItem(True, True)

    def evt_lstWidOpen_itemDelete(self):
        self.dataClass.deleteListItem(0, self.lstWidOpen.currentRow())
        self.callCorrectionFunction = False
        self.clearAllListWidgets()
        self.loadWidgetsToListView()

    def evt_lstWidProgress_itemDelete(self):
        self.dataClass.deleteListItem(1, self.lstWidProgress.currentRow())
        self.callCorrectionFunction = False
        self.clearAllListWidgets()
        self.loadWidgetsToListView()

    def evt_lstWidTested_itemDelete(self):
        self.dataClass.deleteListItem(2, self.lstWidTested.currentRow())
        self.callCorrectionFunction = False
        self.clearAllListWidgets()
        self.loadWidgetsToListView()

    def evt_lstWidReopen_itemDelete(self):
        self.dataClass.deleteListItem(3, self.lstWidReopen.currentRow())
        self.callCorrectionFunction = False
        self.clearAllListWidgets()
        self.loadWidgetsToListView()

    def evt_lstWidClose_itemDelete(self):
        self.dataClass.deleteListItem(4, self.lstWidClose.currentRow())
        self.callCorrectionFunction = False
        self.clearAllListWidgets()
        self.loadWidgetsToListView()


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
    dlgMain = DlgMain()
    dlgMain.show()
    sys.exit(app.exec_())
