from niryo import *
from hanoi import *
from ia import *
from voix2 import *
import time
import joylogic as j

try:
    robot = NiryoRobot("10.10.101.33")

    if robot.arm.need_calibration():
        robot.arm.calibrate_auto()
    robot.tool.update_tool()

    pose_g, pose_m, pose_d = positions_arret(robot, 16)

    initialisation = ""
    while initialisation != "o" and initialisation != "n":
        initialisation = input("Voulez vous proceder à l'initiation de l'environnement du jeu (o/n) ? : ")

    if initialisation == "o":
        tckeck_environnement(robot, 25.2, pose_g, pose_m, pose_d)

    robot.tool.release_with_tool()
except:
    robot = tab_h = pose_g = pose_m = pose_d = 0

tab_h = [25.5 , 23.5, 21.5, 19.5, 17.5]

debut()

niveau = choix_de_niveau()
choix = choix_manipulation()
jeu = TourHanoi(niveau)
jeu.dessine_jeu()

continuer = True
dpl = 0

marqueur=(0,0) # 1er chiffre: dernier mouvement du petit, 2eme : si le dernier mouvement etait le petit
action=(0,0)

while continuer :

    if choix == "clavier":
        action = action_utilisateur()
    elif choix == "ia":
        (action,marqueur) = action_ia(jeu,action,marqueur)
        time.sleep(1.5)
    elif choix == "manette":
        action = j.recupererDeplacementManette()
    elif choix == "voix":
        action = action_voix()
    else :
        print("Rien à faire !")

    if action[0]==0 and action[1]==0 :
        continuer = False
    elif action[0] == -2 and action[1] == -2:
        if jeu.annuler_dernier_mouvement(robot, tab_h, pose_g, pose_m, pose_d):
            jeu.dessine_jeu()
            dpl = dpl + 1
        print(">> Nombre de dépalcements : ", dpl)
    elif action[0]!= -1 and action[1] != -1:
        if jeu.deplacer_disque(robot, tab_h, pose_g, pose_m, pose_d,action[0], action[1]) == 0:
            jeu.dessine_jeu()
            jeu.sauvegarder_dep(action[0], action[1])
            dpl = dpl + 1
            print(">> Nombre de dépalcements : ", dpl)
    else:
        print("On arrive jamais ici !")

    if(jeu.jeu_resolu()):
        print("\n * * * Félicitations !! * * *")
        continuer = False

if robot != 0:
    robot.tool.release_with_tool()
    robot.arm.move_to_home_pose()
    robot.end()


