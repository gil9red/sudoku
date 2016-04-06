#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

import copy

from PySide.QtGui import QWidget, QPainter, QPen, QMessageBox, QSizePolicy
from PySide.QtCore import Qt, Signal

from utils import solver, sudoku_generator


class SudokuBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sudoku')

        # TODO: rem
        # # Пусть будет 20, все-равно после первого события resizeEvent значение изменится
        # self.cell_size = 20
        self.matrix_size = 9

        self.x_highlight_cell = -1
        self.y_highlight_cell = -1

        self.setMouseTracking(True)

        self.default_size = 300
        self.cell_size = min(self.default_size, self.default_size) // self.matrix_size

        self.default_pen_size_1 = 1.0
        self.default_pen_size_2 = 5.0
        self.min_default_pen_size_2 = 2.0

        self.resize(self.default_size, self.default_size)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.matrix = None
        self.sudoku_size = None
        self.orig_matrix = None
        self.def_num_matrix = None
        self.sudoku_solutions = None

        self.new_sudoku()

    change_cell_size = Signal(int)
    # change_size_font_cell_number = Signal(int)

    @property
    def cell_size(self):
        return self.__cell_size

    @cell_size.setter
    def cell_size(self, val):
        self.__cell_size = val
        self.change_cell_size.emit(val)

    # def cell_size(self, size):
    #     self.cell_size = size

    def new_sudoku(self):
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

        # TODO: если и подставлять одно из решений, то решения находить на основе копии текущей таблицы, а не
        # дефотной
        # if event.key() == Qt.Key_Space:
        #     # Получим список решения этой судоку
        #     for solution in self.sudoku_solutions:
        #         # Берем самое первое
        #         self.matrix = copy.deepcopy(solution)
        #
        #         # Перерисовываем окно
        #         self.update()
        #         break

    # def pos_numbers_panel(self):
    #     return 0, self.cell_size * self.matrix_size + 5
    #
    # def size_numbers_panel(self):
    #     return self.cell_size * self.matrix_size, self.cell_size + 5

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # num_panel_height = self.size_numbers_panel()[1]
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

                # Получим список решения этой судоку
                for solution in self.sudoku_solutions:
                    if solution == self.matrix:
                        QMessageBox.information(None, 'Победа', 'Совпало, мать его!')
                        break

                self.update()

        except IndexError:
            pass

    @staticmethod
    def _resize_font(painter, text, size):
        # Алгоритм изменения размера текста взят из http://stackoverflow.com/a/2204501
        # Для текущего пришлось немного адаптировать
        factor = (size / 2) / painter.fontMetrics().width(text)
        if factor < 1 or factor > 1.25:
            f = painter.font()
            point_size = f.pointSizeF() * factor
            if point_size > 0:
                f.setPointSizeF(point_size)
                painter.setFont(f)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)

        painter.save()

        # Рисование ячеектаблицы
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                # Если текущая ячейка относится к дефолтной судоку
                if self.def_num_matrix[i][j]:
                    # painter.setPen()
                    painter.setBrush(Qt.yellow)
                    x = i * self.cell_size
                    y = j * self.cell_size
                    w, h = self.cell_size, self.cell_size
                    painter.drawRect(x, y, w, h)

        painter.restore()

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
                painter.save()
                painter.setBrush(Qt.darkYellow)
                painter.drawRect(x * self.cell_size,
                                 y * self.cell_size,
                                 self.cell_size,
                                 self.cell_size)
                painter.restore()

        # Рисование цифр в ячейки таблицы
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                num = self.matrix[i][j]
                if not num:
                    continue

                num = str(num)
                self._resize_font(painter, num, self.cell_size)

                x = i * self.cell_size
                y = j * self.cell_size
                w, h = self.cell_size, self.cell_size
                painter.drawText(x, y, w, h, Qt.AlignCenter, num)

        # Рисование сетки таблицы
        y1, y2 = 0, 0

        factor = min(self.width(), self.height()) / self.default_size
        size = self.default_pen_size_1
        size2 = self.default_pen_size_2

        if factor < 1 or factor > 1.25:
            size *= factor
            if size < self.min_default_pen_size_2:
                size = self.min_default_pen_size_2

        painter.save()

        for i in range(self.matrix_size + 1):
            painter.setPen(QPen(Qt.black, size2 if i % 3 == 0 and i and i < self.matrix_size else size))
            painter.drawLine(0, y1, self.cell_size * self.matrix_size, y2)

            y1 += self.cell_size
            y2 += self.cell_size

        x1, x2 = 0, 0

        for i in range(self.matrix_size + 1):
            painter.setPen(QPen(Qt.black, size2 if i % 3 == 0 and i and i < self.matrix_size else size))
            painter.drawLine(x1, 0, x2, self.cell_size * self.matrix_size)

            x1 += self.cell_size
            x2 += self.cell_size

        painter.restore()

        # # Рисуем панельку с цифрами судоку
        # numbers_panel_y = self.pos_numbers_panel()[1]
        # painter.save()
        #
        # for i in range(self.matrix_size):
        #     painter.setBrush(Qt.white)
        #     painter.drawRect(i * self.cell_size,
        #                      numbers_panel_y,
        #                      self.cell_size,
        #                      self.cell_size)
        #     num = str(i + 1)
        #     self._resize_font(painter, num, self.cell_size)
        #
        #     x = i * self.cell_size
        #     y = numbers_panel_y
        #     w, h = self.cell_size, self.cell_size
        #     painter.drawText(x, y, w, h, Qt.AlignCenter, num)
        #
        # painter.restore()
