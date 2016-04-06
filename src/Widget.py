#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import QWidget, QVBoxLayout

from sudoku_board import SudokuBoard
from num_panel import NumPanel


class Widget(QWidget):
    def __init__(self):
        super().__init__()

        sudoku_board = SudokuBoard()

        num_panel = NumPanel()
        sudoku_board.change_cell_size.connect(num_panel.update_cell_size)

        layout = QVBoxLayout()
        layout.addWidget(sudoku_board)
        layout.addWidget(num_panel)

        self.setLayout(layout)

        self.setWindowTitle(sudoku_board.windowTitle())
        self.resize(sudoku_board.size())
