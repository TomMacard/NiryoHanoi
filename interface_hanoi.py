import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

class DraggableDisc(QGraphicsRectItem):
    def __init__(self, rect, mainWindow, color):
        super().__init__(rect)
        self.mainWindow = mainWindow
        self.setBrush(QBrush(color))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.originalPosition = rect.topLeft()

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.mainWindow.place_disc_on_tower(self)
        super().mouseReleaseEvent(event)

class HanoiTower(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tour de Hanoï Simulation")
        self.setGeometry(100, 100, 800, 600)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(20, 20, 760, 560)
        self.towers = []
        self.discs = []
        self.draw_towers()
        self.draw_discs()

    def tower_center(self, tower_index):
        return 120 + 250 * tower_index

    def draw_towers(self):
        for i in range(3):
            tower = QGraphicsRectItem(QRectF(self.tower_center(i) - 5, 100, 10, 400))
            tower.setBrush(QBrush(Qt.black))
            self.scene.addItem(tower)
            self.towers.append(tower)

    def draw_discs(self):
        disc_height = 20
        colors = [QColor('red'), QColor('green'), QColor('blue'), QColor('yellow'), QColor('orange')]
        for i in range(5):
            disc_width = 150 - i * 20
            disc = DraggableDisc(QRectF(self.tower_center(0) - disc_width/2, 480 - i * disc_height, disc_width, disc_height), self, colors[i])
            self.scene.addItem(disc)
            self.discs.append(disc)

    def place_disc_on_tower(self, disc):
        closest_tower_index = min(range(3), key=lambda i: abs(self.towers[i].rect().x() + self.towers[i].rect().width()/2 - disc.x()))
        tower_x_center = self.towers[closest_tower_index].rect().x() + self.towers[closest_tower_index].rect().width()/2
        discs_on_tower = [d for d in self.discs if d != disc and abs(d.x() + d.rect().width()/2 - tower_x_center) < 50]
        discs_on_tower.sort(key=lambda d: d.y())

        # Place the disc at the top of the tower or on top of the highest disc.
        y_position = self.towers[closest_tower_index].rect().y() + self.towers[closest_tower_index].rect().height() - disc.rect().height()
        if discs_on_tower:
            y_position = discs_on_tower[-1].y() - disc.rect().height()

        disc.setPos(tower_x_center - disc.rect().width()/2, y_position)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = HanoiTower()
    mainWindow.show()
    sys.exit(app.exec_())
