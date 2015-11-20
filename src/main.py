#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys
    from PySide.QtGui import QApplication
    from widget import Widget
    from sudoku_board import SudokuBoard

    app = QApplication(sys.argv)

    w = Widget()
    # w = SudokuBoard()

    # w.resize(200, 200)
    w.show()

    sys.exit(app.exec_())
