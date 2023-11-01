
# Sources
#
# https://docs.niryo.com/dev/pyniryo2/v1.0.0/en/source/api_doc/niryo_robot.html
#
########################################


iprobot="10.10.101.34"


########################################

from pyniryo2 import *
import math
from robottools import *

# connexion, calibration
print("Connexion...")
try:
    robot = NiryoRobot(iprobot)
    print("OK")
except:
    print("ERREUR : Pas de connexion")

print("Calibration...")
if robot.arm.need_calibration():
    robot.arm.calibrate_auto()
print("OK")

# equiper outil
print("Equipement pince...")
try:
    robot.tool.update_tool()
    print("OK")
except:
    print("ERREUR : Pas d'outil")

print("Positionnement initial...")
robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, -math.pi/2, 0.0])
print("OK")

######### CODE

#mouvement(robot)
#mouvrelatif(robot)

from hanoi import *
from ia import *
import time

def jeuhanoi():
    
    debut()
    niveau = choix_de_niveau()

    choixia= choix_ia()
    marqueur=(0,0) # 1er chiffre: dernier mouvement du petit, 2eme : si le dernier mouvement etait le petit
    action=(0,0)

    jeu = TourHanoi(niveau)
    jeu.dessine_jeu()

    dpl = 0

    continuer = True

    while continuer :

        if not choixia:
            action = action_utilisateur()
        else:
            (action,marqueur) = action_ia(jeu,action,marqueur)
            time.sleep(0.7)

        if action[0]==0 and action[1]==0 :
            continuer = False
        elif action[0]==-2 and action[1]==-2 :
            if jeu.annuler_dernier_mouvement():
                jeu.dessine_jeu()
                dpl = dpl + 1
            print(">> Nombre de dépalcements : ", dpl)

        elif action[0]!= -1 and action[1] != -1:

            robothanoi(robot,action,jeu.piquet1,jeu.piquet2,jeu.piquet3)

            if jeu.deplacer_disque(action[0], action[1]) == 0:
                jeu.dessine_jeu()
                jeu.sauvegarder_dep(action[0], action[1])
                dpl = dpl + 1
                print(">> Nombre de dépalcements : ", dpl)
        else:
            print("On arrive jamais ici !")

        if(jeu.jeu_resolu()):
            print("\n * * * Félicitations !! * * *")
            continuer = False

jeuhanoi()


######### FIN CODE


# déconnexion
print("Déconnexion...")
robot.arm.move_to_home_pose()
robot.tool.release_with_tool()
robot.end()
print("OK")