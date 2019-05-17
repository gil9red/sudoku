#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from collections import defaultdict
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

        # Пусть будет 20, все-равно после первого события resizeEvent значение изменится
        self.cell_size = 20
        self.matrix_size = 9
        self.sub_matrix_size = 3

        self.x_highlight_cell = -1
        self.y_highlight_cell = -1

        self.setMouseTracking(True)

        self.default_size = 300

        self.default_pen_size_1 = 1.0
        self.default_pen_size_2 = 5.0
        self.min_default_pen_size_2 = 2.0

        self.resize(self.default_size, self.default_size)

        self.matrix = None
        self.sudoku_size = None
        self.orig_matrix = None
        self.def_num_matrix = None
        self.sudoku_solutions = None

        # Список хранит индексы с неправильными значениями. Например, когда одинаковые значения на линии
        self.invalid_indexes = []

        self.new_sudoku()

    def new_sudoku(self):
        self.invalid_indexes.clear()

        self.matrix, self.sudoku_size = sudoku_generator.gen()
        self.orig_matrix = copy.deepcopy(self.matrix)

        # Булевая матрица, описывающая местоположения элементов судоку, которые будут по умолчанию.
        # Их нельзя редактировать и выглядят внешне по другому
        self.def_num_matrix = [
            [bool(i) for i in row]
            for row in self.orig_matrix
        ]

        # Получим список решения этой судоку
        self.sudoku_solutions = list(solver.solve_sudoku(self.sudoku_size, copy.deepcopy(self.orig_matrix)))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if event.key() == Qt.Key_Space:
            self.new_sudoku()
            self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.cell_size = min(event.size().width(), event.size().height()) // self.matrix_size

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        pos = event.pos()

        self.x_highlight_cell = pos.x() // self.cell_size
        self.y_highlight_cell = pos.y() // self.cell_size

        self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        pos = event.pos()
        x, y = pos.x() // self.cell_size, pos.y() // self.cell_size

        # Нельзя изменять дефолтную ячейку
        try:
            if not self.def_num_matrix[x][y]:
                if event.button() == Qt.LeftButton:
                    self.matrix[x][y] = self.matrix[x][y] + 1 if self.matrix[x][y] < 9 else 0
                elif event.button() == Qt.RightButton:
                    self.matrix[x][y] = self.matrix[x][y] - 1 if self.matrix[x][y] > 0 else 9
                elif event.button() == Qt.MiddleButton:
                    self.matrix[x][y] = 0

                self.invalid_indexes.clear()

                # В одной плоскости
                for i in range(self.matrix_size):
                    num_by_indexes = defaultdict(list)

                    for j in range(self.matrix_size):
                        num = self.matrix[i][j]
                        if num:
                            num_by_indexes[num].append((i, j))

                    for k, v in num_by_indexes.items():
                        if len(v) > 1:
                            self.invalid_indexes += v

                # В другой плоскости
                for i in range(self.matrix_size):
                    num_by_indexes = defaultdict(list)

                    for j in range(self.matrix_size):
                        num = self.matrix[j][i]
                        if num:
                            num_by_indexes[num].append((j, i))

                    for k, v in num_by_indexes.items():
                        if len(v) > 1:
                            self.invalid_indexes += v

                # В подквадратах
                for si in range(0, self.matrix_size, self.sub_matrix_size):
                    for sj in range(0, self.matrix_size, self.sub_matrix_size):
                        num_by_indexes = defaultdict(list)
                        sub_indexes = []

                        for i in range(self.sub_matrix_size):
                            for j in range(self.sub_matrix_size):
                                sub_indexes.append((si + i, sj + j))

                        for i, j in sub_indexes:
                            num = self.matrix[i][j]
                            if num:
                                num_by_indexes[num].append((i, j))

                        for k, v in num_by_indexes.items():
                            if len(v) > 1:
                                self.invalid_indexes += v

                self.update()

                # Получим список решения этой судоку
                for solution in self.sudoku_solutions:
                    if solution == self.matrix:
                        QMessageBox.information(self, 'Победа', 'Совпало, мать его!')
                        break

        except IndexError:
            pass

    def _draw_background_cell(self, painter: QPainter):
        painter.save()

        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                # Выделяем красным ячейки с неправильными значениями
                if (i, j) in self.invalid_indexes:
                    color = Qt.red

                elif self.def_num_matrix[i][j]:
                    color = Qt.yellow

                else:
                    color = Qt.white

                painter.setBrush(color)

                x = i * self.cell_size
                y = j * self.cell_size
                w, h = self.cell_size, self.cell_size
                painter.drawRect(x, y, w, h)

        # TODO: Закомментировано
        # Если индекс ячейки под курсором валидный
        if 0 <= self.x_highlight_cell < self.matrix_size and 0 <= self.y_highlight_cell < self.matrix_size:
            # # Выделение всего столбца и строки пересекающих ячейку под курсором
            # painter.save()
            # painter.setBrush(Qt.lightGray)
            #
            # # Выделение строки
            # for i in range(self.matrix_size):
            #     painter.drawRect(i * self.cell_size,
            #                      self.y_highlight_cell * self.cell_size,
            #                      self.cell_size,
            #                      self.cell_size)
            #
            # # Выделение столбца
            # for j in range(self.matrix_size):
            #     painter.drawRect(self.x_highlight_cell * self.cell_size,
            #                      j * self.cell_size,
            #                      self.cell_size,
            #                      self.cell_size)
            #
            # painter.restore()

            x, y = self.x_highlight_cell, self.y_highlight_cell

            # Не подсвечиваем дефолтную ячейку
            if not self.def_num_matrix[x][y]:
                # Выделение ячейки под курсором
                painter.setBrush(Qt.darkYellow)
                painter.drawRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

        painter.restore()

    def _draw_cell_numbers(self, painter: QPainter):
        painter.save()

        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                num = self.matrix[i][j]
                if not num:
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

        painter.restore()

    def _draw_grid(self, painter: QPainter):
        painter.save()

        y1, y2 = 0, 0

        factor = min(self.width(), self.height()) / self.default_size
        size = self.default_pen_size_1
        size2 = self.default_pen_size_2

        if factor < 1 or factor > 1.25:
            size *= factor
            if size < self.min_default_pen_size_2:
                size = self.min_default_pen_size_2

        def _is_border(i):
            return i % self.sub_matrix_size == 0 and i and i < self.matrix_size

        for i in range(self.matrix_size + 1):
            painter.setPen(QPen(Qt.black, size2 if _is_border(i) else size))
            painter.drawLine(0, y1, self.cell_size * self.matrix_size, y2)

            y1 += self.cell_size
            y2 += self.cell_size

        x1, x2 = 0, 0

        for i in range(self.matrix_size + 1):
            painter.setPen(QPen(Qt.black, size2 if _is_border(i) else size))
            painter.drawLine(x1, 0, x2, self.cell_size * self.matrix_size)

            x1 += self.cell_size
            x2 += self.cell_size

        painter.restore()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        self._draw_background_cell(painter)

        # Рисование цифр в ячейки таблицы
        self._draw_cell_numbers(painter)

        # Рисование сетки таблицы
        self._draw_grid(painter)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = Widget()
    # w.resize(200, 200)
    w.show()

    sys.exit(app.exec_())
