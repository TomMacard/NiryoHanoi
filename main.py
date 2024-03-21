
# Sources
#
# https://docs.niryo.com/dev/pyniryo2/v1.0.0/en/source/api_doc/niryo_robot.html
#
########################################


iprobot=""


########################################


from pyniryo2 import *
import math
from robottools import *
from voix import *
from hanoi import *
from ia import *
import time
from joylogic import *
from pyniryo2.vision import *
import interface6 as gui

rejouer=1

robot=connexion_robot(iprobot)
if robot:
    robot.led_ring.rainbow_chase(0.1,100)
debut()

'''
vis = Vision(robot)
img_compressed = vis.get_img_compressed()
camera_info = vis.get_camera_intrinsics()
img = vis.uncompress_image(img_compressed)
img = vis.undistort_image(img, camera_info.intrinsics, camera_info.distortion)
'''



while rejouer:

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
            gui.tour1 = jeu.piquet1
            gui.tour1.reverse()
            del(gui.tour1[0])
            gui.tour2 = jeu.piquet2
            gui.tour2.reverse()
            del(gui.tour2[0])
            gui.tour3 = jeu.piquet3
            gui.tour3.reverse()
            del(gui.tour3[0])
            gui.main_gui()

            print("Après interface !")
            #action = action_utilisateur()
        elif choix == "manette" or choix == "m":
            action = recupererDeplacementManette()
        elif choix == "voix" or choix == "v":
            action = action_voix(robot)
        else :
            print("Rien à faire !")

        if action[0]==0 and action[1]==0 :
            continuer = False
        elif action[0]==-2 and action[1]==-2 :
            Val,act=jeu.annuler_dernier_mouvement()
            if Val:
                if robot:
                    robothanoi(robot,act,jeu.piquet1,jeu.piquet2,jeu.piquet3)
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
                if robot:
                    robot.led_ring.alternate([[255,0,0],[0,0,255]], 0.5, 10, False)

        else:
            if robot:
                robot.led_ring.alternate([[255,0,0],[0,0,255]], 0.5, 10, False)
            print("On arrive jamais ici !")

        if(jeu.jeu_resolu()):
            print("\n * * * Félicitations !! * * *")
            if robot:
                robot.led_ring.rainbow_chase(0.1)
            continuer = False 

    rejouer=int(input("Voulez-vous rejouer? (1=oui, 0=)non :"))


if robot:
    deconnexion_robot(robot)