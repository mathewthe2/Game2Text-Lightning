from PyQt5.QtWidgets import QGridLayout, QLabel, QComboBox, QPushButton, QWidget, QTabWidget,QVBoxLayout
from PyQt5.QtCore import Qt
from settings.anki_field_table import AnkiFieldTable

class UIMain(object):
    
    def setupUi(self, parent):
        self.layout = QVBoxLayout(self)
     
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab2,"OCR")
        self.tabs.addTab(self.tab1,"Anki")

        # Capture settings
        self.captureLayout = QGridLayout()
        self.captureLayout.addWidget(QLabel('Capture Method'),0,0)
        self.captureComboBox = QComboBox()
        self.captureComboBox.setEnabled(False)
        self.captureComboBox.addItem('Window')
        self.captureComboBox.addItem('Desktop Area')
        self.captureLayout.addWidget(self.captureComboBox,0,1)
        self.captureLayout.setColumnStretch(1, 1)

        # window
        # if window
        self.captureLayout.addWidget(QLabel('Window'),1,0)
        self.captureWindowComboBox = QComboBox()
        self.captureLayout.addWidget(self.captureWindowComboBox,1,1)

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(False)
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.changeColor)

        # Create second tab
        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addLayout(self.captureLayout)
        self.tab2.layout.addWidget(self.start_button)
        self.tab2.setLayout(self.tab2.layout)
        self.tab2.layout.setAlignment(Qt.AlignTop)

        # Deck and model row
        self.modelDeckLayout = QGridLayout()
        self.modelDeckLayout.addWidget(QLabel('Deck'),0,0)
        self.deckComboBox = QComboBox()
        self.modelDeckLayout.addWidget(self.deckComboBox,0,1)
        self.modelDeckLayout.addWidget(QLabel('Model'),1,0)
        self.modelComboBox = QComboBox()
        self.modelDeckLayout.addWidget(self.modelComboBox,1,1)
        self.modelDeckLayout.setColumnStretch(1, 1)
        self.modelDeckLayout.setSpacing(10)

        # Table
        self.tableFields = AnkiFieldTable([], 0, 2)
        self.tableFields.hide()

        # First Tab
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addLayout(self.modelDeckLayout)
        self.tab1.layout.addWidget(self.tableFields)
        self.tab1.layout.addWidget(QLabel('Make sure AnkiConnect is installed, and Anki is open.'))
        self.tab1.setLayout(self.tab1.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def changeColor(self):
        if self.start_button.isChecked():
            self.start_button.setText('Stop')
            self.start_button.setStyleSheet("background-color : lightblue")
        else:
            self.start_button.setText('Start')
            self.start_button.setStyleSheet("")