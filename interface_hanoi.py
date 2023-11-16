import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import Qt, QRectF

class DraggableDisc(QGraphicsRectItem):
    def __init__(self, rect, mainWindow):
        super().__init__(rect)
        self.mainWindow = mainWindow
        self.originalPosition = rect.topLeft()
        self.setBrush(QBrush(Qt.red if rect.height() % 100 == 0 else Qt.blue))
        self.setFlag(QGraphicsRectItem.ItemIsMovable)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.align_to_tower()

    def align_to_tower(self):
        for i in range(3):
            tower_x = self.mainWindow.tower_center(i)
            if abs(self.x() + self.rect().width()/2 - tower_x) < 50:
                self.mainWindow.update_disc_positions(i, self)
                return
        self.setPos(self.originalPosition)

class HanoiTower(QMainWindow):
    def __init__(self):
        super().__init__()

        # Paramètres de la fenêtre
        self.setWindowTitle("Tour de Hanoï Simulation")
        self.setGeometry(100, 100, 800, 600)

        # Scène pour les tours et les disques
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(20, 20, 760, 560)

        # Dessin des tours
        self.draw_towers()

        # Dessin des disques
        self.draw_discs()

    def tower_center(self, tower_index):
        """ Retourne le point central de la tour spécifiée. """
        return 120 + 250 * tower_index

    def draw_towers(self):
        for i in range(3):
            tower = QGraphicsRectItem(QRectF(self.tower_center(i) - 5, 100, 10, 400))
            tower.setBrush(Qt.black)
            self.scene.addItem(tower)

    def draw_discs(self):
        disc_height = 40
        for i in range(5):  # 5 disques au total
            disc_width = 200 - i * 30
            disc = DraggableDisc(QRectF(self.tower_center(0) - disc_width/2, 500 - i * disc_height, disc_width, disc_height), self)
            self.scene.addItem(disc)

    def update_disc_positions(self, tower_index, moved_disc):
        """ Met à jour la position de tous les disques sur la tour spécifiée. """
        discs_on_tower = [item for item in self.scene.items() if isinstance(item, DraggableDisc) and self.tower_center(tower_index) - 50 < item.x() + item.rect().width()/2 < self.tower_center(tower_index) + 50]
        discs_on_tower.sort(key=lambda x: x.y(), reverse=True)

        # La position de y pour le bas de la tour
        y_position = 500  # Position de y pour la base de la tour

        for disc in discs_on_tower:
            disc.setPos(self.tower_center(tower_index) - disc.rect().width()/2, y_position - disc.rect().height())
            y_position -= disc.rect().height()

        # Mettre à jour la position du disque déplacé et le mettre en haut de la pile
        moved_disc.setPos(self.tower_center(tower_index) - moved_disc.rect().width()/2, y_position - moved_disc.rect().height())
        moved_disc.originalPosition = moved_disc.pos()  # Mise à jour de la position initiale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = HanoiTower()
    mainWindow.show()
    sys.exit(app.exec_())
