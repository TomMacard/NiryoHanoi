

import speech_recognition as sr

l = sr.Recognizer()

l.energy_threshold=2000 #par défaut 300


try:
    with sr.Microphone() as source:

        l.adjust_for_ambient_noise(source, duration=1)
        print('Ecoute...')
        voix = l.listen(source, timeout=5)
        print('Analyse...')
        commande = l.recognize_google(voix, language="fr-FR")
        print("Commande : " +commande)

        if commande=="gauche":
            print("mvt gauche")
        elif commande=="droite":
            print("mvt droite")
        elif commande=="milieu":
            print("mvt milieu")






except sr.WaitTimeoutError:
    print("Aucune parole détectée dans le délai imparti. Veuillez réessayer.")

except sr.UnknownValueError:
    print("Impossible de comprendre la parole. Veuillez réessayer.")

except sr.RequestError as e:
    print(f"Erreur lors de la demande au service Google Speech Recognition; {e}")


