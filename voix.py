

import speech_recognition as sr

"""
l = sr.Recognizer()

l.energy_threshold=2000 #par défaut 300

try:
    with sr.Microphone() as source:

        l.adjust_for_ambient_noise(source, duration=1)
        print('Dites les commandes (ex : 1 2)...')
        voix = l.listen(source, timeout=3)
        print('Analyse...')
        commande = l.recognize_google(voix, language="fr-FR")
        print("Commande : " +commande)

        action = commande.split()
        action = map(int, action)
        action = tuple(action)
        print(action)

except sr.WaitTimeoutError:
    print("Aucune parole détectée dans le délai imparti. Veuillez réessayer.")

except sr.UnknownValueError:
    print("Impossible de comprendre la parole. Veuillez réessayer.")

except sr.RequestError as e:
    print(f"Erreur lors de la demande au service Google Speech Recognition; {e}")
"""


L12=["1 2", "1 et 2", "gauche milieu", "gauche et milieu","gauche-milieu"]
L21=["2 1", "2 et 1", "milieu gauche", "milieu et gauche","milieu-gauche"]
L13=["1 3", "1 et 3", "gauche droite", "gauche et droite","gauche-droite"]
L31=["3 1", "3 et 1", "droite gauche", "droite et gauche","droite-gauche"]
L23=["2 3", "2 et 3", "milieu droite", "milieu et droite","milieu-droite"]
L32=["3 2", "3 et 2", "droite milieu", "droite et milieu","droite-milieu"]
Lquitte=["quitter", "quitte",]




def choix_voix():
    while True:
        try:
            entier = int(input("Voulez-vous parler pour jouer? 1=oui, 0=non : "))
            if entier==1 or entier ==0:
                return entier
            else:
                print("Entrer soit 0 soit 1 !")
        except ValueError:
            print("Veuillez entrer un entier !")

def action_voix():
    l = sr.Recognizer()

    l.energy_threshold=2000 #par défaut 300
    
    action = 0
    while not action:
        try:
            with sr.Microphone() as source:

                l.adjust_for_ambient_noise(source, duration=1)

                while not action:
                    print('Dites les commandes (ex : "1 2" ou "quitter"...')
                    voix = l.listen(source, timeout=3)
                    print('Analyse...')
                    commande = l.recognize_google(voix, language="fr-FR")
                    print("Commande : " +commande)

                    if commande in L12:
                        return(1,2)
                    elif commande in L21:
                        return(2,1)
                    elif commande in L13:
                        return(1,3)
                    elif commande in L31:
                        return(3,1)
                    elif commande in L23:
                        return(2,3)
                    elif commande in L32:
                        return(3,2)
                    elif commande in Lquitte:
                        return(0,0)
                    

        except sr.WaitTimeoutError:
            print("Aucune parole détectée dans le délai imparti. Veuillez réessayer.")

        except sr.UnknownValueError:
            print("Impossible de comprendre la parole. Veuillez réessayer.")

        except sr.RequestError as e:
            print(f"Erreur lors de la demande au service Google Speech Recognition; {e}")
        
    return(action)