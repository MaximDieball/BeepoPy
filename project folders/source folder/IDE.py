import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# NOT USED RIGHT NOW
pretext = ""
'''
pretext = '"""\nWrite your first code and learn programming together with Beepo!\n\n '\
    'Controll Beepo with following functions:\n'\
    '\tBeepo.move()\t\tBeepo.turn_left()\tBeepo.turn_right()\n'\
    '\tBeepo.pickup_gear()\tBeepo.push_button()\tBeepo.set_position() \n\n'\
    'Learn more about Beepos seroundings with following sensor functions:\n'\
    '\tBeepo.wall_front()\tBeepo.wall_left()\tBeepo.wall_right()\n'\
    '\tBeepo.on_gear()\tBeepo.on_Button()\n\n'\
    'Do you whant to learn all the secret fetures of every function? Check the Documentery!\n"""\n'\
    'Write your code here:\n\n'
'''

# COUNTING TABS in beginning of string
def count_tabs(string):
  count = 0
  for char in string:
    if char == "\t":
      count += 1
    else:
      return count

# IDE CLASS
class Ui_IDE(object):

    def setupUi(self, MainWindow):

        # IDE WINDOW
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(777, 658)

        # INPUT TEXT EDIT
        self.InputTextEdit = QtWidgets.QTextEdit(MainWindow)
        self.InputTextEdit.setGeometry(QtCore.QRect(20, 80, 741, 451))
        # LOADING CODE from Code.py
        with open("Code.py", "r") as Code:
            load_code = Code.read()
            self.InputTextEdit.setText(pretext + load_code)

        # COMPILE BUTTON
        self.CompileButton = QtWidgets.QPushButton(MainWindow)
        self.CompileButton.setGeometry(QtCore.QRect(20, 30, 131, 31))
        self.CompileButton.setObjectName("CompileButton")
        self.CompileButton.clicked.connect(self.compile)

        # ERROR LABEL
        self.ErrorLabel = QtWidgets.QLabel(MainWindow)
        self.ErrorLabel.setGeometry(QtCore.QRect(20, 540, 741, 101))
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")

        # SAVE BUTTON
        self.SaveButton = QtWidgets.QPushButton(MainWindow)
        self.SaveButton.setGeometry(QtCore.QRect(170, 30, 131, 31))
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.clicked.connect(self.save)

        # SHIT
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Form"))
        self.CompileButton.setText(_translate("MainWindow", "Compile"))
        self.SaveButton.setText(_translate("MainWindow", "Save"))

    # CHECKING for ERRORS in Code.py
    # CHANGING CODE
    # WRITING Code.py to Compiled.py
    def compile(self):
        Code_file = "Code.py"
        Compiled_file = "Compiled.py"

        output = ""
        with open(Code_file, "r") as Code:
            source = Code.read()
        try:
            compile(source, Code_file, "exec")
            output += "No syntax errors found."
            compiled_output = ""
            with open(Code_file, "r") as Code:
                source = Code.readlines()
                for line in source:
                    compiled_output = compiled_output + line + "\n"
                    if ":" not in line:
                        for _ in range(count_tabs(line)):
                            compiled_output = compiled_output + "\t"
                        compiled_output = compiled_output + f"time.sleep(1)\n"
            with open(Compiled_file, "w") as Compile_Code:
                Compile_Code.write(compiled_output)
        except SyntaxError as e:
            output += f"\nSyntax error in Code:"
            output += f"\n{e.text.rstrip()}"
            output += "\n" + " " * (e.offset - 1) + "^"
            output += f"\n{e.__class__.__name__}: {e}"
        except Exception as e:
            output += f"Error reading Code: {e}"
        self.ErrorLabel.setText(output)

    # SAVING CODE writen in the ide to Code.py
    def save(self):
        Code_file = "Code.py"
        with open(Code_file,"w") as Code:
            Code.write(self.InputTextEdit.toPlainText())
