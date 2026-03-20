from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit
from PySide6.QtGui import QIntValidator,QDoubleValidator, QRegularExpressionValidator
from PySide6.QtCore import QLocale, QRegularExpression


class NumDelegateOnly(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)

        validator = QIntValidator(0, 999999, editor)
        editor.setValidator(validator)
        return editor


class StrDelegateOnly(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)

        regex = QRegularExpression('^[a-zA-Z]*$')
        validator = QRegularExpressionValidator(regex, editor)
        
        editor.setValidator(validator)
        return editor
    
class IntValidation(QIntValidator):

    @classmethod
    def validate(cls):
        validator = QIntValidator(0, 999999)

        return validator
    
class DecimalValidation(QDoubleValidator):

    @classmethod
    def validate(cls):
        validator = QDoubleValidator(0.0, 999999.99, 2)
        validator.setLocale(QLocale("C"))
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        
        return validator