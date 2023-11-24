from hanoi import *
import niryo as n

def choix_manipulation():
    choix =""
    while choix != "manette" and choix != "ia" and choix != "clavier" and choix != "voix" :
        choix = input("Vous jouez avec :\n- tapez manette, pour utiliser la manette\n- taper ia, et laissez l'ia jouer\n- taper clavier, pour jouer avec le clavier\n- tapez voix, et parlez directement au robot\nEcrivez : ")
    return choix

def debut():
    print("\n---------------------------------------------------   T O U R S    D E    H A N O I   ---------------------------------------------------\n")
    print("- Déplace tous les disques sur le troisième piquet, en utilisant le piquet intermédiaire au milieu")
    print("- Décris ton déplacement avec 2 nombres n1 et n2, séparés par des virgules. EX : 1,2 ")
    print("- n1 correspond au piquet où tu vas prendre le disque, et n2, le piquet où tu vas deposer le disque")
    print("- Tape q : pour arreter le jeu !\n")
    retour = "z"
    while retour != "c":
        retour = input("Tape c pour continuer : ")
        retour = retour.strip().lower()

def choix_de_niveau():
    while True:
        try:
            entier = int(input("Entre le nombre de disque (min : 1 , max : 5) : "))
            if 1 <= entier <= 5:
                return entier
            else:
                print("le nombre de disque doit être compris entre 1 et 5 !")
        except ValueError:
            print("Veuillez entrer un entier !")

def action_utilisateur():
    input_string = input("\nEntrez les numeros du piquet de depart, d'arrivée (ou 'q' pour quitter,'a' pour retourner en arriere) séparés par des virgules : ")

    if input_string.strip().lower() == 'q':
        print("Vous avez choisi de quitter !")
        return (0,0)
    elif input_string.strip().lower() == 'a':
        print("Retour en arrière !")
        return (-2,-2)
    else:
        numbers = input_string.split(',')

        if len(numbers) != 2:
            print("Veuillez entrer deux nombres séparés par une virgule ! ")
            return (-1,-1)
        else:
            try:
                num1 = int(numbers[0])
                num2 = int(numbers[1])

                # Vérifiez que les nombres sont compris entre 1 et 3
                if 1 <= num1 <= 3 and 1 <= num2 <= 3:
                    return (num1, num2)
                else:
                    print("Les nombres doivent être compris entre 1 et 3.")
                    return (-1,-1)
            except ValueError:
                print("Assurez-vous que les valeurs entrées sont des nombres valides.")
                return (-1,-1)


def nbre_symbole(n):
    return (5 + (n - 1) * 8)

class TourHanoi:
    niveau = 3
    espace_init = 6
    max_symbole = 0

    piquet1 = []
    piquet2 = []
    piquet3 = []

    def __init__(self, niveau):
        self.niveau = niveau
        self.max_symbole = nbre_symbole(niveau)
        self.deps_prec = []

        for i in range(niveau):
            self.piquet1.append(i+1)
            self.piquet2.append(0)
            self.piquet3.append(0)

        self.piquet1.append(niveau+1)
        self.piquet2.append(niveau+1)
        self.piquet3.append(niveau+1)


    def get_piquet(self, n):
        if n == 1:
            return self.piquet1
        if n == 2:
            return self.piquet2
        if n == 3:
            return self.piquet3

    def dessine_piquet(self):
        print("\n",((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", "!", ((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", end=" ")
        print("",((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", "!", ((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", end=" ")
        print("",((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", "!", ((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", end=" \n")

    def dessine_disque(self, niveau_disque):
        if niveau_disque == 0 :
            print("",((int)((self.max_symbole - 1) / 2) + self.espace_init ) * " ", "!", ((int)((self.max_symbole - 1) / 2) + self.espace_init) * " ", end=" ")
        else :
            n = nbre_symbole(niveau_disque)
            nbre_espace = (int)((self.max_symbole - n) / 2) + self.espace_init
            print("",nbre_espace * " ", n * "=", nbre_espace * " ", end=" ")

    def dessine_socle(self):
        print(((3 * (self.max_symbole + (2 * self.espace_init) + 4) - 2)) * ":")
        print("+", (self.max_symbole + (2 * self.espace_init))*" ","+", (self.max_symbole + + (2 * self.espace_init))*" ","+", (self.max_symbole + + (2 * self.espace_init))*" ","+")
        print(((3 * (self.max_symbole + (2 * self.espace_init) + 4) - 2)) * ":")

    def dessine_jeu(self):

        print("\n")
        self.dessine_piquet()

        for i in range(self.niveau):
            self.dessine_disque(self.piquet1[i])
            self.dessine_disque(self.piquet2[i])
            self.dessine_disque(self.piquet3[i])
            self.dessine_piquet()

        self.dessine_socle()

    def jeu_resolu(self):
        for i in range(self.niveau):
            if self.piquet3[i] != i + 1:
                return False
        return True


    def deplacer_disque(self,robot,tab_h,pose_g, pose_m, pose_d,num_piquet_depart, num_piquet_arrivee):
        indice_disque_a_prendre = 0
        indice_placement_disque = 0

        #premier cas : piquet1 vers piquet2
        if num_piquet_depart == 1 and num_piquet_arrivee == 2 :
            for i in range(self.niveau):
                if self.piquet1[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet1[indice_disque_a_prendre] ==0 :
                indice_disque_a_prendre = self.niveau

            for j in range(self.niveau):
                if self.piquet2[j] == 0 and self.piquet2[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet2[indice_placement_disque+1] > self.piquet1[indice_disque_a_prendre]:
                #le depacement physique passe avvant le deplement logique

                n.deplacement(robot, (1, 2), tab_h, pose_g, pose_m, pose_d, self.piquet1, self.piquet2)
                self.piquet2[indice_placement_disque] = self.piquet1[indice_disque_a_prendre]
                self.piquet1[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

        # deuxieme cas : piquet1 vers piquet3
        if num_piquet_depart == 1 and num_piquet_arrivee == 3 :
            for i in range(self.niveau):
                if self.piquet1[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet1[indice_disque_a_prendre] ==0 :
                indice_disque_a_prendre = self.niveau #Cas ou il n' y a pas de disque sur le piquet

            for j in range(self.niveau):
                if self.piquet3[j] == 0 and self.piquet3[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet3[indice_placement_disque+1] > self.piquet1[indice_disque_a_prendre]:

                n.deplacement(robot, (1, 3), tab_h, pose_g, pose_m, pose_d, self.piquet1, self.piquet3)
                self.piquet3[indice_placement_disque] = self.piquet1[indice_disque_a_prendre]
                self.piquet1[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

        #troisieme cas : piquet2 vers piquet1
        if num_piquet_depart == 2 and num_piquet_arrivee == 1 :
            for i in range(self.niveau):
                if self.piquet2[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet2[indice_disque_a_prendre] ==0 :
                indice_disque_a_prendre = self.niveau #Cas ou il n' y a pas de disque sur le piquet

            for j in range(self.niveau):
                if self.piquet1[j] == 0 and self.piquet1[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet1[indice_placement_disque+1] > self.piquet2[indice_disque_a_prendre]:

                n.deplacement(robot, (2,1), tab_h, pose_g, pose_m, pose_d, self.piquet2, self.piquet1)
                self.piquet1[indice_placement_disque] = self.piquet2[indice_disque_a_prendre]
                self.piquet2[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

        # quatrieme cas : piquet2 vers piquet3
        if num_piquet_depart == 2 and num_piquet_arrivee == 3 :
            for i in range(self.niveau):
                if self.piquet2[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet2[indice_disque_a_prendre] ==0 :
                indice_disque_a_prendre = self.niveau #Cas ou il n' y a pas de disque sur le piquet

            for j in range(self.niveau):
                if self.piquet3[j] == 0 and self.piquet3[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet3[indice_placement_disque+1] > self.piquet2[indice_disque_a_prendre]:

                n.deplacement(robot, (2,3), tab_h, pose_g, pose_m, pose_d, self.piquet2, self.piquet3)
                self.piquet3[indice_placement_disque] = self.piquet2[indice_disque_a_prendre]
                self.piquet2[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

        # cinquieme cas : piquet3 vers piquet1
        if num_piquet_depart == 3 and num_piquet_arrivee == 1 :
            for i in range(self.niveau):
                if self.piquet3[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet3[indice_disque_a_prendre] ==0 :
                indice_disque_a_prendre = self.niveau #Cas ou il n' y a pas de disque sur le piquet

            for j in range(self.niveau):
                if self.piquet1[j] == 0 and self.piquet1[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet1[indice_placement_disque+1] > self.piquet3[indice_disque_a_prendre]:

                n.deplacement(robot, (3,1), tab_h, pose_g, pose_m, pose_d, self.piquet3, self.piquet1)
                self.piquet1[indice_placement_disque] = self.piquet3[indice_disque_a_prendre]
                self.piquet3[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

        # sixieme cas : piquet3 vers piquet2
        if num_piquet_depart == 3 and num_piquet_arrivee == 2 :
            for i in range(self.niveau):
                if self.piquet3[i] != 0 :
                    indice_disque_a_prendre = i
                    #print(i)
                    break

            if indice_disque_a_prendre == 0 and self.piquet3[indice_disque_a_prendre] ==0:
                indice_disque_a_prendre = self.niveau #Cas ou il n' y a pas de disque sur le piquet

            for j in range(self.niveau):
                if self.piquet2[j] == 0 and self.piquet2[j+1] != 0 :
                    indice_placement_disque = j
                    #print(j)
                    break

            if self.piquet2[indice_placement_disque+1] > self.piquet3[indice_disque_a_prendre]:

                n.deplacement(robot, (3,2), tab_h, pose_g, pose_m, pose_d, self.piquet3, self.piquet2)
                self.piquet2[indice_placement_disque] = self.piquet3[indice_disque_a_prendre]
                self.piquet3[indice_disque_a_prendre] = 0
                return 0
            else:
                print("Mouvement interdit !")
                return 1

    def sauvegarder_dep(self, p1, p2):
        # Ajoutez l'état actuel des piquets à la pile
        # il faut que ca n'enregistre pas dans dep si je tape a
        dep_courant = (p1, p2)
        self.deps_prec.append(dep_courant)

    def annuler_dernier_mouvement(self, robot, tab_h, pose_g, pose_m, pose_d):
        # Annule le dernier mouvement en restaurant l'état précédent des piquets
        if self.deps_prec:
            dernier_dep = self.deps_prec.pop()
            print(dernier_dep[1])
            print(dernier_dep[0])
            self.deplacer_disque(robot,tab_h,pose_g, pose_m, pose_d, dernier_dep[1], dernier_dep[0])
            return True
        else:
            print("Aucun mouvement à annuler.")
            return False