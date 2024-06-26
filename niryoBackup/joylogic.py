import pygame
import time

class JoystickControl:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.deplacement = ()

    def joy_callback(self):
        pygame.event.pump()
        position1 = 0
        position2 = 0
        var = False
        continuer = True
        while(continuer):
            time.sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    print(event)
                    # Un bouton a été appuyé
                    if event.button == 1:  # Bouton A
                        print("bouton A")
                        if var == False:
                            position1 = 3
                            var = True
                        else:
                            position2 = 3
                            print(position1)
                            print(position2)
                            continuer = False
                            var = False
                            self.deplacement = (position1, position2)
                            self.joystick.quit()
                            break
                    elif event.button == 2:  # Bouton Y
                        print("bouton Y")
                        if var == False :
                            position1 = 1
                            var = True
                        else :
                            position2 = 1
                            print(position1)
                            print(position2)
                            continuer = False
                            var = False
                            self.deplacement = (position1, position2)
                            self.joystick.quit()
                            break
                    elif event.button == 3:  # Bouton X
                        print("bouton X")
                        if var == False :
                            position1 = 2
                            var = True
                        else :
                            position2 = 2
                            print(position1)
                            print(position2)
                            continuer = False
                            var = False
                            self.deplacement = (position1, position2)
                            self.joystick.quit()
                            break

                    elif event.button == 0:  # Bouton X
                        print("bouton B")
                        self.deplacement = (-2, -2)
                        self.joystick.quit()
                        break
                    elif event.button == 6:  # Bouton X
                        print("bouton -")
                        self.deplacement = (0, 0)
                        self.joystick.quit()
                        break

    def get_deplacement(self):
            return self.deplacement

    def run(self):
        self.joy_callback()

def recupererDeplacementManette():
    try:
        joystick_control = JoystickControl()
        joystick_control.run()
        dep = joystick_control.get_deplacement()
        joystick_control.joystick.quit()
        return dep
    except KeyboardInterrupt:
        pass
