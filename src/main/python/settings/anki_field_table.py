from PyQt5.QtWidgets import QHeaderView, QFrame, QComboBox, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import sys

combo_box_options = [ '', 'definition', 'expression', 'pitch', "reading", 'screenshot', 'sentence', 'word_audio']
 
class AnkiFieldTable(QTableWidget):
    def __init__(self, fields, *args):
        QTableWidget.__init__(self, *args)
        self.setHorizontalHeaderLabels(['Field', 'Value'])
        self.fields = fields
        self.setData(fields)   
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setFrameShape(QFrame.NoFrame)
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
 
    def setData(self, fields): 
        self.setFields(fields)
        self.setOptions(len(fields))

        for i in range(len(fields)):
            combo = QComboBox()
            for t in combo_box_options:
                combo.addItem(t)
            self.setCellWidget(i, 1, combo)

    def setFields(self, fields):
         for i, field in enumerate(fields):
            item =  QTableWidgetItem(field)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            item.setForeground(QBrush(QColor(100, 100, 150)))
            self.setItem(i, 0, item)

    def setOptions(self, rows):
        for i in range(rows):
            combo = QComboBox()
            for t in combo_box_options:
                combo.addItem(t)
            self.setCellWidget(i, 1, combo)

    def setRowCount(self, rows):
        super().setRowCount(rows)
        self.setOptions(rows)

 
def main(args):
    app = QApplication(args)
    fields = ['Expression','Kana','Definition','Examples']
    table = AnkiFieldTable(fields, 4, 2)
    table.show()
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)