import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ConnectorTypeDialog(QDialog):

	def __init__(self, connector):
		super().__init__()

		self.title = "Settings"
		self.type_selected = "Normal"
		self.connector = connector
		self.setModal(True)
		self.InitUI()

	def InitUI(self):
		self.setWindowTitle(self.title)
		vbox = QVBoxLayout()

		self.label = QLabel("Select a connector type:   ")

		self.normal_button = QRadioButton("Nornal")
		if(self.connector.getType() == "Normal"):
			self.normal_button.setChecked(True)
		self.normal_button.toggled.connect(lambda:self.state_changed(self.normal_button))

		self.true_button = QRadioButton("True")
		if(self.connector.getType() == "True"):
			self.true_button.setChecked(True)
		self.true_button.toggled.connect(lambda:self.state_changed(self.true_button))

		self.false_button = QRadioButton("False")
		if(self.connector.getType() == "False"):
			self.false_button.setChecked(True)
		self.false_button.toggled.connect(lambda:self.state_changed(self.false_button))

		# self.loop_button = QRadioButton("Loop")
		# if(self.connector.getType() == "Loop"):
		# 	self.loop_button.setChecked(True)
		# self.loop_button.toggled.connect(lambda:self.state_changed(self.loop_button))

		self.ok_button = QPushButton("Exit")
		self.ok_button.clicked.connect(self.ok_button_clicked)

		vbox.addWidget(self.label)
		vbox.addWidget(self.normal_button)
		vbox.addWidget(self.true_button)
		vbox.addWidget(self.false_button)
		# vbox.addWidget(self.loop_button)
		vbox.addWidget(self.ok_button)

		self.setLayout(vbox)

		self.show()

	def state_changed(self, btn):
		self.connector.setType(btn.text())

	def ok_button_clicked(self, e):
		self.close()

	def get_type_selected(self):
		return self.type_selected



if __name__ == "__main__":
	app = QApplication(sys.argv)
	dialog = ConnectorTypeDialog()
	sys.exit(app.exec_())



