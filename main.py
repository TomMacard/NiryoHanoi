
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
from voix import *
from hanoi import *
from ia import *
import time

def jeuhanoi():

    robot=connexion_robot(iprobot)
    robot.led_ring.rainbow_chase(0.1,100)
    debut()
    
    niveau = choix_de_niveau()
    choix = choix_manipulation()

    marqueur=(0,0) # 1er chiffre: dernier mouvement du petit, 2eme : si le dernier mouvement etait le petit
    action=(0,0)

    jeu = TourHanoi(niveau)
    jeu.dessine_jeu()

    dpl = 0

    continuer = True

    while continuer :

        if choix == "ia" or choix == "i" :
            (action,marqueur) = action_ia(jeu,action,marqueur)
            if not robot:
                time.sleep(0.7)
        elif choix == "clavier" or choix == "c":
            action = action_utilisateur()
        elif choix == "manette" or choix == "m":
            action = action_utilisateur()
        elif choix == "voix" or choix == "v":
            action = action_voix(robot)
        else :
            print("Rien à faire !")

        if action[0]==0 and action[1]==0 :
            continuer = False
        elif action[0]==-2 and action[1]==-2 :
            if jeu.annuler_dernier_mouvement():
                jeu.dessine_jeu()
                dpl = dpl + 1
            print(">> Nombre de déplacements : ", dpl)

        elif action[0]!= -1 and action[1] != -1:

            if jeu.deplacer_disque(action[0], action[1]) == 0:

                if robot:
                    robothanoi(robot,action,jeu.piquet1,jeu.piquet2,jeu.piquet3)
                jeu.dessine_jeu()
                jeu.sauvegarder_dep(action[0], action[1])
                dpl = dpl + 1
                print(">> Nombre de déplacements : ", dpl)
            else:
                robot.led_ring.alternate([[255,0,0],[0,0,255]], 0.5, 10, False)
        else:
            if robot:
                robot.led_ring.alternate([[255,0,0],[0,0,255]], 0.5, 10, False)
            print("On arrive jamais ici !")

        if(jeu.jeu_resolu()):
            print("\n * * * Félicitations !! * * *")
            continuer = False 

    if robot:
        robot.led_ring.rainbow_chase(0.1)
        deconnexion_robot(robot)

jeuhanoi()

