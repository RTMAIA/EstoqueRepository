from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from PySide6.QtGui import QIntValidator


class NumDelegateOnly(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)

        validator = QIntValidator(0, 999999, editor)
        editor.setValidator(validator)
        return editor

class IntValidation(QIntValidator):

    @classmethod
    def validate(cls):
        validator = QIntValidator(0, 999999)

        return validator