iprobot="10.10.10.10"


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import pyqtSignal
from hanoi import TourHanoi

from robottools import *

class SimpleHanoiWidget(QWidget):
    # Signal qui envoie un tuple contenant les tours de départ et d'arrivée et l'état des piquets
    deplacementEffectueSignal = pyqtSignal(tuple)

    def __init__(self, niveau, robot=None):
        super().__init__()
        self.jeuHanoi = TourHanoi(niveau)
        self.robot = robot  # Stocker une référence au robot
        self.tourSelectionnee = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tours de Hanoï')
        self.setGeometry(100, 100, 600, 400)  # Taille de la fenêtre
        self.show()

    def mousePressEvent(self, event):
        tourIndex = event.x() // (self.width() // 3) + 1
        if self.tourSelectionnee is None:
            self.tourSelectionnee = tourIndex
        else:
            if self.jeuHanoi.deplacer_disque(self.tourSelectionnee, tourIndex) == 0:
                # Si le déplacement est valide, émettre le signal avec les informations nécessaires
                self.deplacementEffectueSignal.emit((self.tourSelectionnee, tourIndex, self.jeuHanoi.piquet1, self.jeuHanoi.piquet2, self.jeuHanoi.piquet3))
                if self.jeuGagne():
                    QMessageBox.information(self, "Victoire", "Félicitations ! Vous avez gagné. Voulez-vous rejouer ?")
                    # Ici, vous pourriez ajouter la logique pour recommencer le jeu si nécessaire
            else:
                QMessageBox.warning(self, "Mouvement interdit", "Ce mouvement est interdit. Veuillez essayer de nouveau.")
            self.tourSelectionnee = None
            self.update()

    def jeuGagne(self):
        # Un jeu est gagné si le piquet 3 contient tous les disques dans l'ordre décroissant et les autres piquets sont vides
        return self.jeuHanoi.piquet1 == [] and self.jeuHanoi.piquet2 == [] and self.jeuHanoi.piquet3 == list(
            range(self.jeuHanoi.niveau, 0, -1))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawTours(qp)
        self.drawDisques(qp)
        qp.end()

    def drawTours(self, qp):
        qp.setBrush(QColor(165, 42, 42))
        tourWidth = self.width() // 20
        tourHeight = self.height() // 2
        for i in range(3):
            x = (i + 0.5) * self.width() / 3
            y = self.height() / 2 - tourHeight / 2
            qp.drawRect(int(x - tourWidth / 2), int(y), int(tourWidth), int(tourHeight))

    def drawDisques(self, qp):
        qp.setBrush(QColor(0, 255, 0))
        disqueHeight = self.height() // 40
        piquets = [self.jeuHanoi.piquet1, self.jeuHanoi.piquet2, self.jeuHanoi.piquet3]
        for i, piquet in enumerate(piquets):
            x = (i + 0.5) * self.width() / 3
            baseY = self.height() * 0.75 - len(piquet) * disqueHeight
            for j, disque in enumerate(reversed(piquet)):
                disqueWidth = self.width() * 0.15 * disque / self.jeuHanoi.niveau
                y = baseY - j * disqueHeight
                qp.drawRect(int(x - disqueWidth / 2), int(y), int(disqueWidth), int(disqueHeight))

# Fonction qui gère le signal émis lors d'un déplacement valide
def onDeplacementEffectue(deplacement):
    tourDepart, tourArrivee, piquet1, piquet2, piquet3 = deplacement
    #mouvements = deplacement
    # Supposons que robothanoi est une fonction définie pour contrôler le robot
    robothanoi(robot, (tourDepart, tourArrivee), piquet1, piquet2, piquet3)

    print(f"Déplacement de {tourDepart} à {tourArrivee}")


def main_gui(niveau, robot=None):
    app = QApplication(sys.argv)
    ex = SimpleHanoiWidget(niveau, robot)
    ex.deplacementEffectueSignal.connect(onDeplacementEffectue)
    sys.exit(app.exec_())

if __name__ == '__main__':
    # Supposons que 'robot' est rotre instance de robot initialisée correctement
    # Mise en place l'initialisation de notre robot ici
    robot = connexion_robot(iprobot)
    if robot:
        robot.led_ring.rainbow_chase(0.1, 100)
    level = int(input("Veuiillez entrer le   niveau de jeu (nombre de disques) !!"))
    main_gui(level, robot)
