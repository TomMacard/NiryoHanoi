
import speech_recognition as sr
from fuzzywuzzy import fuzz

piquet1 = ["premier", "un", "1", "gauche", "1er"]
piquet2 = ["deuxième", "deux", "2", "milieu", "2e"]
piquet3 = ["troisième", "dernier", "trois", "3", "droite", "3e"]
quitter = ["quitter", "quitte", "kit", "arrêter", "arrête", "arrêt"]
retour = ["annuler", "annule", "retour", "arrière", "retourne", "retourner"]

def action_voix():
    l = sr.Recognizer()

    l.energy_threshold=2000 #par défaut 300

    action = 0
    while not action:
        try:
            with sr.Microphone() as source:

                l.adjust_for_ambient_noise(source, duration=1)

                while not action:
                    print('Donnez vos instructions au robot...')
                    voix = l.listen(source, timeout=10)
                    print('Analyse...')
                    commande = l.recognize_google(voix, language="fr-FR")
                    print("Commande : " +commande)
                    liste_mot_recup = commande.split(' ')
                    return phrase_to_action(piquet1, piquet2, piquet3, quitter, retour, liste_mot_recup)


        except sr.WaitTimeoutError:
            print("Aucune parole détectée dans le délai imparti. Veuillez réessayer.")

        except sr.UnknownValueError:
            print("Impossible de comprendre la parole. Veuillez réessayer.")

        except sr.RequestError as e:
            print(f"Erreur lors de la demande au service Google Speech Recognition; {e}")

    return(action)

def phrase_to_action(tab1, tab2, tab3, tab4, tab5, phrase):
    action = [0,0]

    for mot in phrase :
        for mot1 in tab1:
            if fuzz.ratio(mot, mot1) >= 80 :
                if action[0] == 0 :
                    action[0]=1
                else :
                    action[1]=1
                    return (action[0], action[1])
        for mot2 in tab2:
            if fuzz.ratio(mot, mot2) >= 80 :
                if action[0] == 0 :
                    action[0]=2
                else :
                    action[1]=2
                    return (action[0], action[1])
        for mot3 in tab3:
            if fuzz.ratio(mot, mot3) >= 80 :
                if action[0] == 0 :
                    action[0]=3
                else :
                    action[1]=3
                    return (action[0], action[1])
        for mot4 in tab4:
            if fuzz.ratio(mot, mot4) >= 80 :
                return (0,0)
        for mot5 in tab5:
            if fuzz.ratio(mot, mot5) >= 80 :
                return (-2,-2)
    return (-1,-1)
