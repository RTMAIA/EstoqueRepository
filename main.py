from view import view
from view.instancias import instances
from PySide6.QtWidgets import QApplication
import sys



app = QApplication(sys.argv)
app.setStyle('Fusion')

sistema = view.TelaPrincipal(instances.estoque_controller, instances.produto_controller, instances.categoria_controller, instances.movimentacao_controller, instances.relatorio_controller)\

sistema.show()
sys.exit(app.exec())
