from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt

import math

class QBarPlot(QWidget):

    def __init__(self):
        super().__init__()

        self.horizontal_margin = 10
        self.vertical_margin = 10

        self.data = None
        self.data_index = None
        self.title = None

        self.ymin = None
        self.ymax = None

        # Set window background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)

        self.setPalette(palette)

    def paintEvent(self, event):
        qp = QPainter(self)

        try:
            num_bar = len(self.data)
        except:
            num_bar = 0

        if self.data_index is not None and len(self.data_index) != len(self.data):
            raise ValueError("len(data_index) != len(data)")              # TODO

        size = self.size()
        widget_width = size.width()
        widget_height = size.height()

        if num_bar > 0:
            plot_area_width = max(0, widget_width - 2 * self.horizontal_margin)
            plot_area_height = max(0, widget_height - 2 * self.vertical_margin)

            data_min = min(self.data) if self.ymin is None else self.ymin
            data_max = max(self.data) if self.ymax is None else self.ymax

            data = [data_value - data_min for data_value in self.data]

            # Set antialiasing
            qp.setRenderHint(QPainter.Antialiasing)           # <- Set anti-aliasing  See https://wiki.python.org/moin/PyQt/Painting%20and%20clipping%20demonstration

            # Set Pen and Brush
            qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            for data_index, data_value in enumerate(data):
                x_length = math.floor(plot_area_width / num_bar)
                y_length = - math.floor( data_value * plot_area_height / (data_max - data_min))

                x_start = self.horizontal_margin + data_index * x_length
                y_start = widget_height - self.vertical_margin

                # Draw bar
                qp.drawRect(x_start, y_start, x_length, y_length)
