import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
from level_list import first_lvl, second_lvl, third_lvl


class Word:
    def __init__(self, word):
        word = list(word)
        self.letters_dict = {}
        for letter in range(len(word)):
            if word[letter] in self.letters_dict:
                self.letters_dict[word[letter]].append(letter)
            else:
                self.letters_dict[word[letter]] = [letter]
    
    def check(self, word):
        bulls = 0
        cows = 0
        for letter in word.letters_dict:
            if letter in self.letters_dict:
                for i in self.letters_dict[letter]:
                    if i in word.letters_dict[letter]:
                        bulls += 1
                    else:
                        cows += 1
        return bulls, cows
    

def ok_word(word):
    p = morph.parse(word)
    for i in p:
        if i.tag.POS == 'NOUN':
            if (i.normal_form == word) and (
                str(i.methods_stack[0][0]) == '<DictionaryAnalyzer>'):
                return True  
            

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(353, 462)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.inputWord = QtWidgets.QLineEdit(self.centralwidget)
        self.inputWord.setGeometry(QtCore.QRect(40, 50, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputWord.setFont(font)
        self.inputWord.setObjectName("inputWord")
        self.textInputWord = QtWidgets.QLabel(self.centralwidget)
        self.textInputWord.setGeometry(QtCore.QRect(40, 20, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textInputWord.setFont(font)
        self.textInputWord.setTextFormat(QtCore.Qt.AutoText)
        self.textInputWord.setWordWrap(False)
        self.textInputWord.setObjectName("textInputWord")
        self.check = QtWidgets.QPushButton(self.centralwidget)
        self.check.setGeometry(QtCore.QRect(40, 100, 75, 23))
        self.check.setObjectName("check")
        self.textBulls = QtWidgets.QLabel(self.centralwidget)
        self.textBulls.setGeometry(QtCore.QRect(40, 170, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textBulls.setFont(font)
        self.textBulls.setObjectName("textBulls")
        self.bullsNum = QtWidgets.QLCDNumber(self.centralwidget)
        self.bullsNum.setGeometry(QtCore.QRect(40, 210, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.bullsNum.setFont(font)
        self.bullsNum.setDigitCount(3)
        self.bullsNum.setObjectName("bullsNum")
        self.textCows = QtWidgets.QLabel(self.centralwidget)
        self.textCows.setGeometry(QtCore.QRect(140, 170, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textCows.setFont(font)
        self.textCows.setObjectName("textCows")
        self.cowsNum = QtWidgets.QLCDNumber(self.centralwidget)
        self.cowsNum.setGeometry(QtCore.QRect(140, 210, 64, 51))
        self.cowsNum.setDigitCount(3)
        self.cowsNum.setObjectName("cowsNum")
        self.repeat = QtWidgets.QPushButton(self.centralwidget)
        self.repeat.setGeometry(QtCore.QRect(40, 300, 81, 31))
        self.repeat.setObjectName("repeat")
        self.level = QtWidgets.QComboBox(self.centralwidget)
        self.level.setGeometry(QtCore.QRect(40, 390, 111, 31))
        self.level.setObjectName("level")
        self.level.addItems(['лёгкий', 'средний', 'сложный'])
        self.textlevel = QtWidgets.QLabel(self.centralwidget)
        self.textlevel.setGeometry(QtCore.QRect(40, 370, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textlevel.setFont(font)
        self.textlevel.setObjectName("textlevel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 353, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bulls and cows"))
        self.textInputWord.setText(_translate("MainWindow", "Введите слово:"))
        self.check.setText(_translate("MainWindow", "Проверить"))
        self.textBulls.setText(_translate("MainWindow", "Быки:"))
        self.textCows.setText(_translate("MainWindow", "Коровы:"))
        self.repeat.setText(_translate("MainWindow", "Начать"))
        self.textlevel.setText(_translate("MainWindow", "Уровень сложности:"))

        
class MyWidget(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.start = False
        self.repeat.clicked.connect(self.run_begin)
        self.check.clicked.connect(self.run_check)
    
    def run_begin(self):
        if not self.start:
            level = self.level.currentText()
            if level == 'лёгкий':
                answer_word = random.choice(first_lvl)
            elif level == 'средний':
                answer_word = random.choice(second_lvl)
            else:
                answer_word = random.choice(third_lvl)
            self.right = answer_word
            self.answer_word = Word(answer_word)
            self.repeat.setText('Сдаться')
            self.inputWord.setText('')
            self.start = True
        else:
            self.inputWord.setText(self.right)
            self.repeat.setText('Начать')
            self.start = False
        self.bullsNum.display(0)
        self.cowsNum.display(0)
        
    def run_check(self):
        if self.start:
            word = self.inputWord.text().lower()
            if ok_word(word):
                if word == self.right:
                    self.win()
                else:
                    word = Word(word)
                    bulls, cows = self.answer_word.check(word)
                    self.bullsNum.display(bulls)
                    self.cowsNum.display(cows)
            else:
                self.bullsNum.display(0)
                self.cowsNum.display(0)
                self.inputWord.setText('*НЕДОПУСТИМОЕ СЛОВО*')
        else:
            self.inputWord.setText('*ИГРА НЕ НАЧАЛАСЬ*')
                
    def win(self):
        self.bullsNum.display(0)
        self.cowsNum.display(0)
        self.repeat.setText('Начать')
        self.inputWord.setText('*WIN!*')
        self.start = False
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
