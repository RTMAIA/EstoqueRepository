from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

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