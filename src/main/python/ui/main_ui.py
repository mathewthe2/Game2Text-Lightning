from PyQt5.QtWidgets import QGridLayout, QCheckBox, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QWidget, QTabWidget,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from settings.anki_field_table import AnkiFieldTable
from screenshot import Capture_Mode

class UIMain(object):
    
    def setupUi(self, parent):
        self.layout = QVBoxLayout(self)
     
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.settingsTab = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"OCR")
        self.tabs.addTab(self.tab2,"Anki")
        self.tabs.addTab(self.settingsTab,"Settings")

        # Capture settings
        self.captureLayout = QGridLayout()
        self.captureLayout.addWidget(QLabel('Capture Method'),0,0)
        self.captureComboBox = QComboBox()
        self.captureComboBox.addItem('Window')
        self.captureComboBox.addItem('Desktop Area')
        self.captureComboBox.currentIndexChanged.connect(self.change_capture_mode_widgets)
        self.captureLayout.addWidget(self.captureComboBox,0,1)
        self.captureLayout.setColumnStretch(1, 1)

        # window
        self.captureWindowLabel = QLabel('Window')
        self.captureLayout.addWidget(self.captureWindowLabel,1,0)
        self.captureWindowComboBox = QComboBox()
        self.captureLayout.addWidget(self.captureWindowComboBox,1,1)

        # desktop area
        self.selectRegionButton = QPushButton("Select region")
        self.selectRegionButton.setHidden(True)
        self.regionInfoLabel = QLabel('Selected Region:')
        self.regionInfoLabel.setHidden(True)

        # start button
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(False)
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.changeColor)

        # Create first tab
        self.tab1.layout = QVBoxLayout()
        self.tab1.layout.addLayout(self.captureLayout)
        self.tab1.layout.addWidget(self.selectRegionButton)
        self.tab1.layout.addWidget(self.start_button)
        self.tab1.layout.addWidget(self.regionInfoLabel)
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.layout.setAlignment(Qt.AlignTop)

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
        self.tableFields = AnkiFieldTable([], None, 0, 2)
        self.tableFields.hide()

        # reload anki button
        self.reloadAnkiButton = QPushButton("Reload")

        # Second Tab
        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addLayout(self.modelDeckLayout)
        self.tab2.layout.addWidget(self.tableFields)
        self.tab2.layout.addWidget(self.reloadAnkiButton)
        self.tab2.layout.addWidget(QLabel('Make sure AnkiConnect is installed, and Anki is open.'))
        self.tab2.setLayout(self.tab2.layout)

        # Settings
        self.resizeInputRow = QHBoxLayout()
        self.resizeCheckBox = QCheckBox("Resize Screenshot")
        self.resizeCheckBox.setChecked(True)
        self.resizeInputRow.addWidget(QLabel('Width'))
        self.resizeWidthInput = QLineEdit()
        self.resizeWidthInput.setValidator(QIntValidator())
        self.resizeWidthInput.setText('1280')
        self.resizeInputRow.addWidget(self.resizeWidthInput)
        self.resizeInputRow.addWidget(QLabel('Height'))
        self.resizeHeightInput = QLineEdit()
        self.resizeHeightInput.setValidator(QIntValidator())
        self.resizeHeightInput.setText('720')
        self.resizeInputRow.addWidget(self.resizeHeightInput)

        # Third Tab
        self.settingsTab.layout = QVBoxLayout()
        self.settingsTab.layout.addWidget(self.resizeCheckBox)
        self.settingsTab.layout.addLayout(self.resizeInputRow)
        self.settingsTab.setLayout(self.settingsTab.layout)
        self.settingsTab.layout.setAlignment(Qt.AlignTop)

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

    def change_capture_mode_widgets(self, index):
        if index == Capture_Mode.DESKTOP_AREA.value:
            # hide capture
            self.captureWindowLabel.setHidden(True)
            self.captureWindowComboBox.setHidden(True)
            # show region
            self.selectRegionButton.setHidden(False)
            self.regionInfoLabel.setHidden(False)

        elif index == Capture_Mode.WINDOW.value:
            # show capture
            self.captureWindowLabel.setHidden(False)
            self.captureWindowComboBox.setHidden(False)
            # hide region
            self.selectRegionButton.setHidden(True)
            self.regionInfoLabel.setHidden(True)