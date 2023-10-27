from hanoi import *
from ia import *
import time

debut()
niveau = choix_de_niveau()

choixia= choix_ia()
marqueur=(0,0) # 1er chiffre: dernier mouvement du petit, 2eme : si le dernier mouvement etait le petit
action=(0,0)

jeu = TourHanoi(niveau)
jeu.dessine_jeu()

continuer = True

while continuer :

    if not choixia:
        action = action_utilisateur()
    else:
        (action,marqueur) = action_ia(jeu,action,marqueur)
        time.sleep(0.7)

    if action[0]==0 and action[1]==0 :
        continuer = False
    elif action[0]!= -1 and action[1] != -1:
        if jeu.deplacer_disque(action[0], action[1]) == 0:
            jeu.dessine_jeu()
    else:
        print("On arrive jamais ici !")

    if(jeu.jeu_resolu()):
        print("\n * * * Félicitations !! * * *")
        continuer = False
