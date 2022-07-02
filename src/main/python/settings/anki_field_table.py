from PyQt5.QtWidgets import QHeaderView, QFrame, QComboBox, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import sys
from anki import Anki_Values

combo_box_options = [' '] + [e.name.lower() for e in Anki_Values]

class AnkiFieldTable(QTableWidget):
    def __init__(self, fields, on_change, *args):
        QTableWidget.__init__(self, *args)
        self.setHorizontalHeaderLabels(['Field', 'Value'])
        self.fields = fields
        self.setData(fields)   
        self.on_change = on_change
        self.user_options = [] 
        self.user_field_map = {}
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setFrameShape(QFrame.NoFrame)
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
 
    def setData(self, fields, user_field_map={}): 
        self.fields = fields
        self.user_field_map = user_field_map
        self.setFields(fields)
        self.setOptions(len(fields))
        if user_field_map:
            self.set_field_selection(user_field_map)

    def setFields(self, fields):
        for i, field in enumerate(fields):
            item =  QTableWidgetItem(field)
            item.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )
            item.setForeground(QBrush(QColor(100, 100, 150)))
            self.setItem(i, 0, item)

    def setOptions(self, rows):
        self.user_options = []
        for i in range(rows):
            self.user_options.append(QComboBox())
            for t in combo_box_options:
                self.user_options[i].addItem(t)
            self.user_options[i].currentIndexChanged.connect(lambda selected_index, option_index=i: self.select_option(selected_index, option_index))
            self.setCellWidget(i, 1, self.user_options[i])

    def setRowCount(self, rows):
        super().setRowCount(rows)
        self.setOptions(rows)

    def select_option(self, selected_index, option_index):
        field = self.fields[option_index]
        if selected_index == 0:
              self.user_field_map.pop(field, None)
        else:
            anki_value = Anki_Values(selected_index-1)
            if anki_value:
                self.user_field_map[field] = anki_value.name
        self.on_change(self.user_field_map)

    def set_field_selection(self, user_field_map):
        for key, value in user_field_map.items():
            field_index = self.fields.index(key)
            if field_index >= 0:
                option_index = combo_box_options.index(value.lower())
                if option_index >= 1:
                    self.user_options[field_index].setCurrentIndex(option_index)
 
def main(args):
    app = QApplication(args)
    fields = ['Expression','Kana','Definition','Examples']
    table = AnkiFieldTable(fields, None, 4, 2)
    table.show()
    sys.exit(app.exec_())
 
if __name__=="__main__":
    main(sys.argv)