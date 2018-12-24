#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Отличие от sudoku.py в том, что ячейки таблицы не рисуются, а в виде виджетов расположены."""

import copy
import sys

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *


from utils import solver, sudoku_generator


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sudoku')

        self._grid_layout = QGridLayout()
        self.setLayout(self._grid_layout)

        # Пусть будет 20, все-равно после первого события resizeEvent значение изменится
        self.cell_size = 20
        self.matrix_size = 9

        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                cell = QLabel()
                # cell.resize(self.cell_size, self.cell_size)
                cell.setFixedSize(self.cell_size, self.cell_size)
                cell.setFrameShape(QFrame.Box)
                self._grid_layout.addWidget(cell, i, j, Qt.AlignCenter)

        self.resize(300, 300)

        self.matrix = None
        self.sudoku_size = None
        self.orig_matrix = None
        self.def_num_matrix = None
        self.sudoku_solutions = None

        self.new_sudoku()

    def new_sudoku(self):
        self.matrix, self.sudoku_size = sudoku_generator.gen()
        self.orig_matrix = copy.deepcopy(self.matrix)

        # Булевая матрица, описывающая местоположения элементов судоку, которые будут по умолчанию.
        # Их нельзя редактировать и выглядят внешне по другому
        self.def_num_matrix = [
            [bool(i) for i in row]
            for row in self.orig_matrix
        ]

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                # TODO: сделать матрицу для ячеек
                cell = self._grid_layout.itemAtPosition(i, j).widget()
                num = self.matrix[i][j]
                if num:
                    cell.setText(str(num))

        # Получим список решения этой судоку
        self.sudoku_solutions = list(solver.solve_sudoku(self.sudoku_size, copy.deepcopy(self.orig_matrix)))

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.cell_size = min(event.size().width(), event.size().height()) // self.matrix_size

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                # TODO: сделать матрицу для ячеек
                cell = self._grid_layout.itemAtPosition(i, j).widget()
                cell.setFixedSize(self.cell_size, self.cell_size)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    w.show()

    sys.exit(app.exec_())
