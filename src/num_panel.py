#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PySide.QtGui import *
from PySide.QtCore import *


class NumPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.cell_size = 20
        self.matrix_size = 9

    def update_cell_size(self, size):
        self.cell_size = size
        # self.update()

        self.setFixedHeight(self.cell_size)

    def pos_numbers_panel(self):
        return 0, self.cell_size * self.matrix_size

    def size_numbers_panel(self):
        return self.cell_size * self.matrix_size, self.cell_size

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
        print(self.size())
        # Рисуем панельку с цифрами судоку
        numbers_panel_y = self.pos_numbers_panel()[1]
        painter.save()

        for i in range(self.matrix_size):
            painter.setBrush(Qt.red)
            painter.drawRect(i * self.cell_size,
                             numbers_panel_y,
                             self.cell_size,
                             self.cell_size)
            num = str(i + 1)
            self._resize_font(painter, num, self.cell_size)

            x = i * self.cell_size
            y = numbers_panel_y
            w, h = self.cell_size, self.cell_size
            painter.drawText(x, y, w, h, Qt.AlignCenter, num)

        painter.restore()
