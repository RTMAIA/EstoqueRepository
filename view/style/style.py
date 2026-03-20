estilo_tabela = """
    /* 1. Cor das Células (dados) */
    QTableView {
        background-color: #D9D9D9; /* Fundo branco para os dados */
        color: #585858;             /* Letra escura para os dados */
        gridline-color: #BDBDBD;    /* Cor das linhas da grade */
    }

    /* 2. Cor dos Cabeçalhos (Topo e Lateral) */
    QHeaderView::section {
        background-color: #BDBDBD; /* Cor escura para os headers */
        color: #585858;              /* Letra branca para os headers */
        padding: 4px;
        border: 1px solid #BDBDBD;
        font-weight: bold;
    }

    /* 3. Cor do Botão do Canto (Onde os headers se cruzam) */
    QTableView QTableCornerButton::section {
        background-color: #BDBDBD;
        border: 1px solid #BDBDBD;
    }
"""

cor_fundo = 'background-color: #D9D9D9;'

cor_secundaria = 'background-color: #BDBDBD;'

estilo_qline_edit = ''' QLineEdit {
                              background-color: #D9D9D9; color: #585858; font-size: 15px;
                              border-radius: none;
                              }
                              QLineEdit::focus {
                              border-bottom: 1px solid #909090;
                              }'''

cor_texto_campos = 'color: #686868; font-weight: bold; font-family: Arial, sans-serif; font-size: 13px;'

estilo_menu = '''
                                    QMenuBar {
                                        background-color: #BDBDBD;
                                        color: #585858;
                                        font-size: 14px;
                                 }

                                    QMenuBar::item {
                                        padding: 6px 12px;
                                        margin: 0px;
                                        border-right: 1px solid #585858;
                                        border-bottom: 1px solid #585858;
                                 }    

                                    QMenuBar::item:selected {
                                        background-color: #C9C9C9;
                                 }

                                    QMenu {
                                        background-color: #BDBDBD;
                                    color: #585858;
                                    margin: 0px;
                                    min-width: 100px;
                                 }

                                    QMenu::item {
                                        margin: 0px;
                                        padding: 12px 12px;
                                 }

                                    QMenu::item:selected {
                                        background-color: #D9D9D9;
                                 }
                                '''

estilo_botao = '''
                                        QPushButton {
                                            background-color: #BDBDBD; color: #585858; font-size: 15px;
                                      }

                                        QPushButton:pressed {
                                            background-color: #C0C0C0;
                                      }
                                        '''

estilo_messagebox_warning = '''
                                QMessageBox {
                                    background-color: #D9D9D9;
                                }
                                QLabel {
                                    color: #FF0000;
                                    font-weight: bold;
                                }
                                QPushButton {
                                    color: black;
                                    background-color: white;
                                }
    '''

estilo_messagebox_information = '''
                                QMessageBox {
                                    background-color: #D9D9D9;
                                }
                                QLabel {
                                    color: #4287f5;
                                    font-weight: bold;
                                }
                                QPushButton {
                                    color: black;
                                    background-color: white;
                                }
    '''

estilo_menu_suspenso = """
    QComboBox {
        background-color: #D9D9D9;
        font-size: 13px;
        font-family: Arial, sans-serif;
        color: #909090;
        border: 0px solid #BDBDBD;
        border-radius: 0px;
        padding: 0px;
        margin: 0px;
        min-width: 150px;
    }

    QComboBox QAbstractItemView, QComboBox QFrame {
        background-color: #D4D4D4;
        color: #686868;
        selection-background-color: #E9E9E9;
        border: 1px solid: #BDBDBD;
        margin: 0px;
        outline: none;
    }
"""