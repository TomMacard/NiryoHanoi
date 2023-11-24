#Deplacement en cm
import math
from hanoi import *
from pyniryo2 import *

def deplacement(robot, deplacement, tab_h, pose_g, pose_m, pose_d, piquet1, piquet2):
    if robot != 0 :
        prise_sur_piquet(robot, deplacement[0], tab_h, pose_g, pose_m, pose_d, piquet1)
        placement_disque(robot, deplacement[1], tab_h, pose_g, pose_m, pose_d, 0.6, piquet2)


#retourne 3 positions : a) position initiale + decalage à gauche; b) position initiale; c) position + décalage à droite
def positions_arret(robot, decalage):
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, -math.pi/2, 0.0])
    pose2 = robot.arm.get_pose()
    robot.arm.shift_pose(RobotAxis.Y, -(decalage / 100))
    pose1 = robot.arm.get_pose()
    robot.arm.shift_pose(RobotAxis.Y, 2*(decalage / 100))
    pose3 = robot.arm.get_pose()

    robot.arm.move_pose(pose2)

    return pose1, pose2, pose3

#position : 1 ou -1
def mouvement_horizontal(robot, direction, longueur_en_cm):
    robot.arm.shift_pose(RobotAxis.Z, direction * (longueur_en_cm / 100))

def prise(robot):
    robot.tool.grasp_with_tool()
    robot.arm.shift_pose(RobotAxis.Z, 0.02)


def tckeck_environnement(robot, hauteur, pose_gauche, pose_initiale, pose_droite):
    robot.tool.release_with_tool()

    test = "o"
    while test != "n":
        robot.arm.move_pose(pose_initiale)
        mouvement_horizontal(robot, -1, hauteur)
        while (input("Tapez a avancer : ") != "a" ):
            robot.tool.grasp_with_tool()
            robot.tool.release_with_tool()
        robot.arm.move_pose(pose_initiale)

        robot.arm.move_pose(pose_gauche)
        mouvement_horizontal(robot, -1, hauteur)
        while (input("Tapez a avancer : ") != "a"):
            robot.tool.grasp_with_tool()
            robot.tool.release_with_tool()
        robot.arm.move_pose(pose_gauche)

        robot.arm.move_pose(pose_droite)
        mouvement_horizontal(robot, -1, hauteur)
        while (input("Tapez a avancer : ") != "a"):
            robot.tool.grasp_with_tool()
            robot.tool.release_with_tool()
        robot.arm.move_pose(pose_droite)
        test = input("Continuer le test (o/n) ? : ")
    robot.arm.move_pose(pose_initiale)


# hauteur_de_prise <-- valeur de retour de la fonction : calcul_hauteur(piquet, hauteur_piece, hauteur_base, hauteur_pose_initiale_sol)
def prise_sur_piquet(robot, num_piquet, hauteur_de_prise, pose_gauche, pose_initiale, pose_droite, piquet):
    if num_piquet == 1 :
        robot.arm.move_pose(pose_gauche)
        mouvement_horizontal(robot, -1, hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)-1])
        prise(robot)
        robot.arm.move_pose(pose_gauche)

    elif num_piquet == 2 :
        robot.arm.move_pose(pose_initiale)
        mouvement_horizontal(robot, -1, hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)-1])
        prise(robot)
        robot.arm.move_pose(pose_initiale)

    elif num_piquet == 3 :
        robot.arm.move_pose(pose_droite)
        mouvement_horizontal(robot, -1, hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)-1])
        prise(robot)
        robot.arm.move_pose(pose_droite)

    else:
        print("On fait rien !")


def placement_disque(robot, num_piquet, hauteur_de_prise, pose_gauche, pose_initiale, pose_droite, difference, piquet):
    if num_piquet == 1 :
        robot.arm.move_pose(pose_gauche)
        mouvement_horizontal(robot, -1, (hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)]- difference))
        robot.tool.release_with_tool()
        robot.arm.move_pose(pose_gauche)

    elif num_piquet == 2 :
        robot.arm.move_pose(pose_initiale)
        mouvement_horizontal(robot, -1, (hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)]- difference))
        robot.tool.release_with_tool()
        robot.arm.move_pose(pose_initiale)

    elif num_piquet == 3 :
        robot.arm.move_pose(pose_droite)
        mouvement_horizontal(robot, -1, (hauteur_de_prise[calcul_nbre_disque_sur_piquet(piquet)]- difference))
        robot.tool.release_with_tool()
        robot.arm.move_pose(pose_droite)

    else:
        print("On fait rien !")


def calcul_hauteur(piquet, hauteur_piece, hauteur_base, hauteur_pose_initiale_sol):
    nbre_disque_sur_le_piquet = calcul_nbre_disque_sur_piquet(piquet)

    print("La hauteur : ",hauteur_pose_initiale_sol - ((nbre_disque_sur_le_piquet * hauteur_piece) + hauteur_base))  # Pour le momment bien sur ! on doit calculer la hauteur en cm

    return (hauteur_pose_initiale_sol - ((nbre_disque_sur_le_piquet * hauteur_piece) + hauteur_base))# Pour le momment bien sur ! on doit calculer la hauteur en cm

def calcul_nbre_disque_sur_piquet(piquet):
    nbre = 0
    for i in range(len(piquet)-1):
        print(i," ", piquet[i])
        if piquet[i] != 0 :
            nbre = nbre + 1
    print("nombre de disque : ", nbre)
    return nbre-5

# si unite_de_mesure_en_cm = 1 on avance ic de 1cm à chauqe fois ( on peut mettre 0.5 pour avancer de 0.5 cm, 0.2 pour 0.2 cm etc...
# longeur_estimee est longeur partant de la pince jusqu'à un endroit qu'on estime proche du sol
def mesure_hauteur_pince_sol(robot, pose_initiale, unite_de_mesure_en_cm, longeur_estimee_en_cm):
    robot.arm.move_pose(pose_initiale)
    robot.arm.shift_pose(RobotAxis.Z, (longeur_estimee_en_cm / 100))
    unite_en_m = unite_de_mesure_en_cm / 100
    continuer = True
    i=0
    while continuer :
        try:
            robot.arm.shift_pose(RobotAxis.Z, -unite_en_m)
            i = i + 1
        except :
            robot.arm.move_pose(pose_initiale)
            return (i*(unite_en_m * 100) + longeur_estimee_en_cm) #on retourne le resultat en cm <=> return (i)
    return 0






