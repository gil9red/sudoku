#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

import sys

from PySide.QtGui import *
from PySide.QtCore import *

from utils import solver, sudoku_generator


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sudoku')

        self.cell_size = 20
        self.matrix_size = 9

        self.x_highlight_cell = -1
        self.y_highlight_cell = -1

        # TODO: числа, которые уже есть в матрице сделать неизменяемыми и с другим оформлением
        self.matrix, self.sudoku_size = sudoku_generator.gen()

        self.setMouseTracking(True)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if event.key() == Qt.Key_Space:
            # Получим список решения этой судоку
            for solution in solver.solve_sudoku(self.sudoku_size, self.matrix):
                # Берем самое первое
                self.matrix = solution

                # Перерисовываем окно
                self.update()

                break

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w, h = event.size().width(), event.size().height()
        min_size = min(w, h)

        self.cell_size = min_size // self.matrix_size

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        pos = event.pos()

        self.x_highlight_cell = pos.x() // self.cell_size
        self.y_highlight_cell = pos.y() // self.cell_size

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        # Если индекс ячейки под курсором валидный
        if 0 <= self.x_highlight_cell < self.matrix_size and 0 <= self.y_highlight_cell < self.matrix_size:
            # Выделение всего столбца и строки пересекающих ячейку под курсором
            painter.save()
            painter.setBrush(Qt.lightGray)

            # Выделение строки
            for i in range(self.matrix_size):
                painter.drawRect(i * self.cell_size,
                                 self.y_highlight_cell * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)

            # Выделение столбца
            for j in range(self.matrix_size):
                painter.drawRect(self.x_highlight_cell * self.cell_size,
                                 j * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)

            painter.restore()

            # Выделение ячейки под курсором
            painter.save()
            painter.setBrush(Qt.yellow)
            painter.drawRect(self.x_highlight_cell * self.cell_size,
                             self.y_highlight_cell * self.cell_size,
                             self.cell_size,
                             self.cell_size)
            painter.restore()

        # Рисование цифр в ячейки таблицы
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                num = self.matrix[i][j]

                # Проверяем, что число не находится в диапазоне от 1 до 9
                if not 1 <= num <= 9:
                    continue

                num = str(num)

                # Алгоритм изменения размера текста взят из http://stackoverflow.com/a/2204501
                # Для текущего пришлось немного адаптировать
                factor = (self.cell_size / 2) / painter.fontMetrics().width(num)
                if factor < 1 or factor > 1.25:
                    f = painter.font()
                    point_size = f.pointSizeF() * factor
                    if point_size > 0:
                        f.setPointSizeF(point_size)
                        painter.setFont(f)

                x = i * self.cell_size
                y = j * self.cell_size
                w, h = self.cell_size, self.cell_size
                painter.drawText(x, y, w, h, Qt.AlignCenter, num)

        # Рисование сетки таблицы
        y1, y2 = 0, 0

        for i in range(self.matrix_size + 1):
            painter.drawLine(0, y1, self.cell_size * self.matrix_size, y2)
            y1 += self.cell_size
            y2 += self.cell_size

        x1, x2 = 0, 0

        for i in range(self.matrix_size + 1):
            painter.drawLine(x1, 0, x2, self.cell_size * self.matrix_size)
            x1 += self.cell_size
            x2 += self.cell_size


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    w.resize(200, 200)
    w.show()

    sys.exit(app.exec_())
