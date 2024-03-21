import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt

mouvement = []
tour1 = []
tour2 = []
tour3 = []

# Définir l'environnement QT_QPA_PLATFORM sur wayland
os.environ["QT_QPA_PLATFORM"] = "wayland"
class SimpleHanoiWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.tours = [tour1, tour2, tour3]
        self.tourSelectionnee = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simplification des Tours de Hanoï')
        self.setGeometry(1000, 500, 1000, 800)  # Ajustement pour une meilleure visualisation
        self.show()

    def mousePressEvent(self, event):
        tourIndex = event.x() // (self.width() // 3)
        if self.tourSelectionnee is None and self.tours[tourIndex]:
            self.tourSelectionnee = tourIndex
        else:
            if self.tourSelectionnee != tourIndex and self.tours[tourIndex] is not None:
                self.tours[tourIndex].append(self.tours[self.tourSelectionnee].pop())
            self.tourSelectionnee = None
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawTours(qp)
        self.drawDisques(qp)
        qp.end()

    def drawTours(self, qp):
        qp.setBrush(QColor(165, 42, 42))  # Couleur des tours
        tourWidth = self.width() * 0.02
        tourHeight = self.height() * 0.5
        for i in range(3):
            x = (i + 1) * self.width() / 4
            y = self.height() * 0.5 - tourHeight / 2
            qp.drawRect(int(x - tourWidth / 2), int(y), int(tourWidth), int(tourHeight))

    def drawDisques(self, qp):
        qp.setBrush(QColor(0, 255, 0))  # Couleur des disques
        disqueHeight = self.height() * 0.02
        for i, tour in enumerate(self.tours):
            x = (i + 1) * self.width() / 4
            for j, disque in enumerate(tour):
                disqueWidth = self.width() * 0.2 * disque / 5  # Ajuster la largeur relative au disque
                y = self.height() * 0.75 - j * disqueHeight - disqueHeight
                qp.drawRect(int(x - disqueWidth / 2), int(y), int(disqueWidth), int(disqueHeight))

def main_gui():
    app = QApplication(sys.argv)
    ex = SimpleHanoiWidget()
    sys.exit(app.exec_())

#if __name__ == '__main__':
    #main_gui()
