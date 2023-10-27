from hanoi import *

def choix_ia():
    while True:
        try:
            entier = int(input("Voulez-vous laisser l'IA jouer? 1=oui, 0=non : "))
            if entier==1 or entier ==0:
                return entier
            else:
                print("Entrer soit 0 soit 1 !")
        except ValueError:
            print("Veuillez entrer un entier !")


def action_ia(jeu,action,marqueur):
    p1=0
    p2=0
    p3=0
    i=0
    while p1==0:
        p1=jeu.piquet1[i]
        i=i+1
    i=0
    while p2==0:
        p2=jeu.piquet2[i]
        i=i+1
    i=0
    while p3==0:
        p3=jeu.piquet3[i]
        i=i+1

    #print(p1,p2,p3)
    
    #cas initial
    if marqueur[0]==0:
        return((1,2),(23,True))

    #cas possible si rotation du plus petit a été effectuée
    if marqueur[1]:
        if action==(1,2):
            if p1<p3:
                return((1,3),(23,False))
            else:
                return((3,1),(23,False))
        if action==(2,3):
            if p1<p2:
                return((1,2),(31,False))
            else:
                return((2,1),(31,False))
            
        if action==(3,1):
            if p3<p2:
                return((3,2),(12,False))
            else:
                return((2,3),(12,False))
    
    #rotation du plus petit
    if marqueur[0]==12:
        return((1,2),(23,True))
    if marqueur[0]==23:
        return((2,3),(31,True))
    if marqueur[0]==31:
        return((3,1),(12,True))



        
 

    