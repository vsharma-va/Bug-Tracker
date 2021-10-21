import os
import csv
import pandas as pd
from typing import List


class Data:
    def __init__(self):
        self.filePaths = []
        self.projectName = None

    # function to store data of the items in list widget to a csv file
    def newWidgetStoreData(self, heading: str, description: str, color: str, tagName: str, whichList: int):
        data = pd.read_csv(self.filePaths[whichList])
        allData = pd.read_csv(f"../../Data/ListWidgetData/{self.projectName}/together.csv")
        newRow = pd.DataFrame({'name': [heading], 'description': [description], 'color': [color], 'tagName': [tagName]})
        data = pd.concat([newRow, data]).reset_index(drop=True)
        print(data)
        data.to_csv(self.filePaths[whichList], index=False)
        togetherCsvData = data.append(allData, ignore_index=True)
        togetherCsvData.to_csv(f'../../Data/ListWidgetData/{self.projectName}/together.csv')

    # this function is used when an item is dragged and drop from one list widget to another.
    # it shifts the data from one csv file to another according to the received data
    def switchListWidgetsItem(self, getIn: bool = False, correctData: bool = False):
        if getIn:
            print('switch check')
            removeListData = pd.read_csv(self.filePaths[self.removedFromList])
            insertedListData = pd.read_csv(self.filePaths[self.insertedToList])
            removeListDataDf = pd.DataFrame(removeListData)
            insertedListDataDf = pd.DataFrame(insertedListData)
            x = removeListDataDf.iloc[[self.rowRemovedIndex]]
            removeListDataDf.drop(self.rowRemovedIndex, inplace=True)
            insertedListDataDf = pd.concat([x, insertedListDataDf]).reset_index(drop=True)
            removeListDataDf.to_csv(self.filePaths[self.removedFromList], index=False)
            insertedListDataDf.to_csv(self.filePaths[self.insertedToList], index=False)

        # when the function receives the correct index for the item it changes the csv file accordingly
        if getIn and correctData:
            print('correctData')
            df = pd.read_csv(self.filePaths[self.insertedToList])
            if not df.empty:
                targetRow = len(df) - 1
                print(targetRow)
                index = [targetRow] + [i for i in range(len(df)) if i != targetRow]
                print(index)
                df.iloc[index].reset_index(drop=True)
                df.to_csv(self.filePaths[self.insertedToList], index=False)

    def returnListWidgetsItemsData(self, rowIndex: int, whichList: int):
        print(rowIndex, whichList)
        itemDataList = []
        df = pd.read_csv(self.filePaths[whichList])
        name = df.iat[rowIndex, 0]
        description = df.iat[rowIndex, 1]
        color = df.iat[rowIndex, 2]
        tagName = df.iat[rowIndex, 3]
        itemDataList.extend([name, description, color, tagName])
        return itemDataList

    def loadListWidgetsItems(self):
        openData = []
        progressData = []
        testedData = []
        reopenData = []
        closeData = []
        try:
            dfOpen = pd.read_csv(self.filePaths[0])
            dfProgress = pd.read_csv(self.filePaths[1])
            dfTested = pd.read_csv(self.filePaths[2])
            dfReopen = pd.read_csv(self.filePaths[3])
            dfClose = pd.read_csv(self.filePaths[4])

            if not dfOpen.empty:
                for i in range(len(dfOpen)):
                    name = dfOpen.iat[i, 0]
                    description = dfOpen.iat[i, 1]
                    color = dfOpen.iat[i, 2]
                    tagName = dfOpen.iat[i, 3]
                    openData.extend([[name, description, color, tagName]])

            if not dfProgress.empty:
                for i in range(len(dfProgress)):
                    name = dfProgress.iat[i, 0]
                    description = dfProgress.iat[i, 1]
                    color = dfProgress.iat[i, 2]
                    tagName = dfProgress.iat[i, 3]
                    progressData.extend([[name, description, color, tagName]])

            if not dfTested.empty:
                for i in range(len(dfTested)):
                    name = dfTested.iat[i, 0]
                    description = dfTested.iat[i, 1]
                    color = dfTested.iat[i, 2]
                    tagName = dfTested.iat[i, 3]
                    testedData.extend([[name, description, color, tagName]])

            if not dfReopen.empty:
                for i in range(len(dfReopen)):
                    name = dfReopen.iat[i, 0]
                    description = dfReopen.iat[i, 1]
                    color = dfReopen.iat[i, 2]
                    tagName = dfReopen.iat[i, 3]
                    reopenData.extend([[name, description, color, tagName]])

            if not dfClose.empty:
                for i in range(len(dfClose)):
                    name = dfClose.iat[i, 0]
                    description = dfClose.iat[i, 1]
                    color = dfClose.iat[i, 2]
                    tagName = dfClose.iat[i, 3]
                    closeData.extend([[name, description, color, tagName]])

            return [openData, progressData, testedData, reopenData, closeData]
        except IndexError:
            return False

    def deleteListItem(self, whichList: int, rowNumber: int):
        df = pd.read_csv(self.filePaths[whichList])
        df.drop(rowNumber, inplace=True)
        df.to_csv(self.filePaths[whichList], index=False)

    def setRemovedItemIndex(self, rowRemovedIndex: int):
        self.rowRemovedIndex = rowRemovedIndex

    def setInsertedItemIndex(self, rowInsertedIndex: int):
        self.rowInsertedIndex = rowInsertedIndex

    def setListRemoved(self, removedFromList: int):
        self.removedFromList = removedFromList

    def setListInserted(self, insertedToList: int):
        self.insertedToList = insertedToList

    def setProject(self, projectName: str):
        self.projectName = projectName
        self.filePaths = [f"../../Data/ListWidgetData/{self.projectName}/lstWidOpen.csv", f"../../Data/ListWidgetData/{self.projectName}/lstWidProgress.csv",
                          f"../../Data/ListWidgetData/{self.projectName}/lstWidTested.csv", f"../../Data/ListWidgetData/{self.projectName}/lstWidReopen.csv",
                          f"../../Data/ListWidgetData/{self.projectName}/lstWidClosed.csv"]

        if not os.path.isdir(f"../../Data/ListWidgetData/{self.projectName}"):
            os.makedirs(f"../../Data/ListWidgetData/{self.projectName}")

        if not os.path.isfile(f"../../Data/ListWidgetData/{self.projectName}/together.csv"):
            with open(f"../../Data/ListWidgetData/{self.projectName}/together.csv", 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
            file.close()

        if not os.path.isfile(self.filePaths[0]):
            with open(self.filePaths[0], 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
            file.close()
        if not os.path.isfile(self.filePaths[1]):
            with open(self.filePaths[1], 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
            file.close()
        if not os.path.isfile(self.filePaths[2]):
            with open(self.filePaths[2], 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
            file.close()
        if not os.path.isfile(self.filePaths[3]):
            with open(self.filePaths[3], 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
                file.close()
        if not os.path.isfile(self.filePaths[4]):
            with open(self.filePaths[4], 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'description', 'color', 'tagName'])
            file.close()

    def countRecords(self) -> List[int]:
        try:
            dfOpen = pd.read_csv(self.filePaths[0])
            dfProgress = pd.read_csv(self.filePaths[1])
            dfTested = pd.read_csv(self.filePaths[2])
            dfReopen = pd.read_csv(self.filePaths[3])
            dfClosed = pd.read_csv(self.filePaths[4])
            return [len(dfOpen), len(dfProgress), len(dfTested), len(dfReopen), len(dfClosed)]
        except IndexError:
            print('No Project Selected')
            return [0, 0, 0, 0, 0]

    def returnTopFiveItems(self) -> list:
        try:
            df = pd.read_csv(f"../../Data/ListWidgetData/{self.projectName}/together.csv")
            requiredDf = df.head(5)
            name = requiredDf['name'].tolist()
            description = requiredDf['description'].tolist()
            tagName = requiredDf['tagName'].tolist()
            return [name, description, tagName]
        except AttributeError:
            return False

    def returnDirectories(self) -> list:
        required = os.listdir("../../Data/ListWidgetData")
        print(required)
        return required

    def returnCurrentProjectName(self) -> str:
        return self.projectName

    def saveLastKnown(self):
        with open("../../Data/LastKnown.csv", 'w', encoding='utf-8') as file:
            file.write(self.projectName)
        file.close()
