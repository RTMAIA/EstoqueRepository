from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from decimal import Decimal

class TableClass(QAbstractTableModel):
    def __init__(self, data):
        self._data = data
        super().__init__()

    def rowCount(self, parent=QModelIndex()):
        return(len(self._data[0]))
    
    def columnCount(self, parent=QModelIndex()):
        return(len(self._data[0][0]))

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return(self._data[0][index.row()][index.column()])

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (f'{self._data[1][section]}')
            if orientation == Qt.Vertical:
                return f'{section + 1}'
        return None
    
    def atualizar_dados_model(self, novos_dados):
        self.beginResetModel()
        self._data = novos_dados
        self.endResetModel()

    def retornar_data(self):
        return self._data

class TableEditableClass(QAbstractTableModel):
    def __init__(self, data, columns):
        self.columns = columns
        self._data = data
        self.dado = {}
        super().__init__()    

    def rowCount(self, parent=QModelIndex()):
        return(len(self._data[0]))
    
    def columnCount(self, parent=QModelIndex()):
        return(len(self._data[0][0]))

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return(self._data[0][index.row()][index.column()])

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (f'{self._data[1][section]}')
            if orientation == Qt.Vertical:
                return f'{section + 1}'
        return None
    
    def flags(self, index):
        if self.columns:
            for i in self.columns:
                if index.column() == i:
                    return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def setData(self, index, value, role =Qt.EditRole):
            if role == Qt.EditRole:
                self.row = index.row()
                self.col = index.column()
                if isinstance(value, int) or value.isdigit():
                    if self._data[1][self.col].lower() ==  'valor_unitario':
                        self._data[0][self.row][self.col] = value
                        self.dado[self._data[1][self.col].lower()] = Decimal(self._data[0][self.row][self.col])
                        self.dataChanged.emit(index, index, [Qt.DisplayRole])
                    else:    
                        self._data[0][self.row][self.col] = value
                        self.dado[self._data[1][self.col].lower()] = int(self._data[0][self.row][self.col])
                        self.dataChanged.emit(index, index, [Qt.DisplayRole])
                else:
                    self._data[0][self.row][self.col] = value
                    self.dado[self._data[1][self.col].lower()] = self._data[0][self.row][self.col]
                    self.dataChanged.emit(index, index, [Qt.DisplayRole])
                    return True
                return False
            return False
    
    def retornar_data(self):
        return self.dado

    def atualizar_dados_model(self, novos_dados):
        self.beginResetModel()
        self._data = novos_dados
        self.endResetModel()