from hanoi import *

debut()
niveau = choix_de_niveau()
jeu = TourHanoi(niveau)
jeu.dessine_jeu()

continuer = True

while continuer :

    action = action_utilisateur()

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
