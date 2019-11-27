from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt, QVariant
class sortableElement(QStandardItem):
    def __lt__(self, other):
        try:
            if ( isinstance(other, QStandardItem)):
                my_value = int(self.data(Qt.EditRole).split("#")[-1])
                other_value= int(other.data(Qt.EditRole).split("#")[-1])
                if ( my_value and other_value ):
                    return my_value < other_value
            return super(MyTableWidgetItem, self).__lt__(other)
        except Exception as e:
            return False
