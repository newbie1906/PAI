from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QFileDialog, QLineEdit, QGridLayout, QSpinBox, QPlainTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QStatusBar
from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QIcon, QAction, QPixmap

# Tworzenie klasy głównego okna aplikacji dziedziczącej po QMainWindow

class Window(QMainWindow):
    #Dodanie konstruktora przyjmującego okno nadrzędne
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 640, 480)
        self.setFixedSize(640, 480)
        self.setWindowTitle('PyQt6 Lab')
        
        self.createMenu()
        self.createTabs()
        
    
    # Funkcja dodająca pasek menu do okna
    def createMenu(self):
        # Stworzenie paska menu
        self.menu = self.menuBar()
        # Dodanie do paska listy rozwijalnej o nazwie File
        self.fileMenu = self.menu.addMenu("File")
        # Dodanie do menu File pozycji zamykającej aplikacje
        self.actionExit = QAction('Exit', self)
        self.actionExit.triggered.connect(self.close)
        self.fileMenu.addAction(self.actionExit)

        #Dodanie do paska listy rozwijalnej o nazwie Task1
        self.task1 = self.menu.addMenu("Task1")
        self.actionOpenT1 = QAction('Open', self)
        self.actionOpenT1.setShortcut('Ctrl+G')
        self.actionOpenT1.triggered.connect(self.openT1Picture)
        self.task1.addAction(self.actionOpenT1)

        #Dodanie do paska listy rozwijalnej o nazwie Task2
        self.task2 = self.menu.addMenu("Task2")
        self.actionClearT2 = QAction('Clear', self)
        self.actionClearT2.setShortcut('Ctrl+W')
        self.actionClearT2.triggered.connect(self.clearT2Text)
        self.actionOpenT2 = QAction('Open', self)
        self.actionOpenT2.setShortcut('Ctrl+O')
        self.actionOpenT2.triggered.connect(self.openT2Text)
        self.actionSaveT2 = QAction('Save', self)
        self.actionSaveT2.setShortcut('Ctrl+S')
        self.actionSaveT2.triggered.connect(self.saveT2Text)
        self.actionSaveAsT2 = QAction('Save as', self)
        self.actionSaveAsT2.setShortcut('Ctrl+K')
        self.actionSaveAsT2.triggered.connect(self.saveAsT2Text)
        self.task2.addAction(self.actionClearT2)
        self.task2.addAction(self.actionOpenT2)
        self.task2.addAction(self.actionSaveT2)
        self.task2.addAction(self.actionSaveAsT2)

        #Dodanie do paska listy rozwijalnej o nazwie Task3
        self.task3 = self.menu.addMenu("Task3")
        self.actionClearT3 = QAction('Clear', self)
        self.actionClearT3.setShortcut('Ctrl+Q')
        self.actionClearT3.triggered.connect(self.clearT3Inputs)
        self.task3.addAction(self.actionClearT3)
    
    # Funkcja dodająca wenętrzeny widżet do okna
    def createTabs(self):
        # Tworzenie widżetu posiadającego zakładki
        self.tabs = QTabWidget()
        
        # Stworzenie osobnych widżetów dla zakładek
        # Logika Tab1
        self.tab_1 = QWidget()
        self.tab_1.layout = QVBoxLayout()
        self.t1Photo = QLabel(self.tab_1)
        self.tab_1.layout.addWidget(self.t1Photo)
        self.tab_1.setLayout(self.tab_1.layout)

        # Logika Tab2
        self.tab_2 = QWidget()
        self.tab_2.layout = QVBoxLayout()
        self.t2Notpad = QPlainTextEdit()
        self.tab_2.layout.addWidget(self.t2Notpad)
        self.t2_buttonsWidget = QWidget()
        self.t2_buttonsWidgetLayout = QHBoxLayout(self.t2_buttonsWidget)
        button_t2_save = QPushButton("Zapisz")
        button_t2_save.clicked.connect(self.saveT2Text)
        button_t2_clear = QPushButton("Wyczyść")
        button_t2_clear.clicked.connect(self.clearT2Text)
        self.t2_buttonsWidgetLayout.addWidget(button_t2_save)
        self.t2_buttonsWidgetLayout.addWidget(button_t2_clear)

        self.tab_2.layout.addWidget(self.t2_buttonsWidget)
        self.tab_2.setLayout(self.tab_2.layout)

        # Logika Tab3
        self.tab_3 = QWidget()
        self.tab_3 = QWidget()
        self.tab_3.layout = QGridLayout()
        self.t3TE_A = QLineEdit()
        self.t3TE_B = QLineEdit()
        self.t3TE_C = QSpinBox()
        self.t3TE_ABC = QLineEdit()
        label_A = QLabel("Pole A")
        label_B = QLabel("Pole B")
        label_C = QLabel("Pole C")
        label_ABC = QLabel("Pola A+B+C")
        self.tab_3.layout.addWidget(label_A, 0, 0)
        self.tab_3.layout.addWidget(self.t3TE_A, 0, 1)
        self.tab_3.layout.addWidget(label_B, 1, 0)
        self.tab_3.layout.addWidget(self.t3TE_B, 1, 1)
        self.tab_3.layout.addWidget(label_C, 2, 0)
        self.tab_3.layout.addWidget(self.t3TE_C, 2, 1)
        self.tab_3.layout.addWidget(label_ABC, 3, 0)
        self.tab_3.layout.addWidget(self.t3TE_ABC, 3, 1)
        self.tab_3.setLayout(self.tab_3.layout)

        self.t3TE_A.returnPressed.connect(self.updateT3_ABC_QLE)
        self.t3TE_B.returnPressed.connect(self.updateT3_ABC_QLE)
        self.t3TE_C.valueChanged.connect(self.updateT3_ABC_QLE)


        # Dodanie zakładek do widżetu obsługującego zakładki
        self.tabs.addTab(self.tab_1, "Task1")        
        self.tabs.addTab(self.tab_2, "Task2")        
        self.tabs.addTab(self.tab_3, "Task3")
        
        # Dodanie widżetu do głównego okna jako centralny widżet
        self.setCentralWidget(self.tabs)

    def openT1Picture(self):
        fileName, selectedFilter = QFileDialog.getOpenFileName(self.tab_1, "Wybierz plik obrazu",  "Początkowa nazwa pliku", "All Files (*);;JPG (*.jpg);; PNG (*.png)")  

        if fileName:
            pixmap = QPixmap(fileName)
            pixmap.scaled(640, 480)
            self.t1Photo.setPixmap(pixmap)

    def openT2Text(self):
        self.t2Notpad.clear()
        self.t2_fileName, selectedFilter = QFileDialog.getOpenFileName(self.tab_1, "Wybierz plik obrazu",  "Początkowa nazwa pliku", "TXT (*.txt)")
        
        if self.t2_fileName:
            text = open(self.t2_fileName).read()
            self.t2Notpad.insertPlainText(text)

    
    def saveT2Text(self):
        try:
            if self.t2_fileName:
                file = open(self.t2_fileName, 'w')
                text = self.t2Notpad.toPlainText()
                file.write(text)
                file.close()
        except:
            self.saveAsT2Text()
    
    def saveAsT2Text(self):
        try:
            name, selectedFilter = QFileDialog.getSaveFileName(self, 'Save File As',"", '*.txt')
            file = open(name,'w')
            text = self.t2Notpad.toPlainText()
            file.write(text)
            file.close()
        except:
            pass
    
    def clearT2Text(self):
        self.t2Notpad.clear()

    def clearT3Inputs(self):
        self.t3TE_A.clear()
        self.t3TE_B.clear()
        self.t3TE_C.clear()
        self.t3TE_ABC.clear()

    def updateT3_ABC_QLE(self):
        self.t3TE_ABC.setText(f'{self.t3TE_A.text()} {self.t3TE_B.text()} {self.t3TE_C.value()}')


            
# Uruchomienie okna
app = QApplication([])
win = Window()
win.show()
app.exec()

