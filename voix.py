
import speech_recognition as sr
from fuzzywuzzy import fuzz
from pyniryo2 import *

piquet1 = ["premier", "un", "1", "gauche","1er"]
piquet2 = ["deuxième", "deux", "2", "milieu", "centre", "2e"]
piquet3=["troisième", "dernier", "trois", "3", "3e","droite"]
quitter = ["quitter", "quitte", "kit", "arrêter", "arrête", "arrêt"]
retour = ["annuler", "annule", "retour", "arrière", "retourne", "retourner"]

ratio=95


def action_voix(robot):
    l = sr.Recognizer()

    l.energy_threshold=2000 #par défaut 300

    action = 0
    while not action:
        try:
            with sr.Microphone() as source:

                l.adjust_for_ambient_noise(source, duration=1)

                while not action:
                    print('\n'*30)
                    print('Donnez vos instructions au robot...')
                    robot.led_ring.snake([255,128,0],1,10)
                    voix = l.listen(source, timeout=10)
                    print('Analyse...')
                    commande = l.recognize_google(voix, language="fr-FR")
                    print("Commande : " +commande)
                    liste_mot_recup = commande.split(' ')
                    return phrase_to_action(liste_mot_recup)


        except sr.WaitTimeoutError:
            print("Aucune parole détectée dans le délai imparti. Veuillez réessayer.")

        except sr.UnknownValueError:
            print("Impossible de comprendre la parole. Veuillez réessayer.")

        except sr.RequestError as e:
            print(f"Erreur lors de la demande au service Google Speech Recognition; {e}")

    return(action)

def phrase_to_action(phrase):
    action = [0,0]

    for mot in phrase :
        for mot1 in piquet1:
            if fuzz.ratio(mot, mot1) >= ratio:
                if action[0] == 0 :
                    action[0]=1
                else :
                    action[1]=1
                    return (action[0], action[1])
        for mot2 in piquet2:
            if fuzz.ratio(mot, mot2) >= ratio :
                if action[0] == 0 :
                    action[0]=2
                else :
                    action[1]=2
                    return (action[0], action[1])
        for mot3 in piquet3:
            if fuzz.ratio(mot, mot3) >= ratio:
                if action[0] == 0 :
                    action[0]=3
                else :
                    action[1]=3
                    return (action[0], action[1])
        for mot4 in quitter:
            if fuzz.ratio(mot, mot4) >= ratio:
                return (0,0)
        for mot5 in retour:
            if fuzz.ratio(mot, mot5) >= ratio :
                return (-2,-2)
    return (-1,-1)


#print(action_voix())