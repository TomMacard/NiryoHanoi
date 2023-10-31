from pyniryo2 import *
import math



def mouvement(robot):
    m=True
    print("==== Mouvement Manuel ====")
    while m:
        m=input("Entrer 0 pour terminer : ")
        if m:  
            L=  [float(input("(float) X     = "))]
            L=L+[float(input("(float) Y     = "))]
            L=L+[float(input("(float) Z     = "))]
            L=L+[float(input("(float) rot X = "))]
            L=L+[float(input("(float) rot Y = "))]
            L=L+[float(input("(float) rot Z = "))]
            print("Mouvement...")
            robot.arm.move_pose(L)
            print("OK")

def mouvrelatif(robot):
    m=True
    print("==== Mouvement Relatif ====")
    while m:
        print("- Mouvement relatif : x,-x,y,-y,z,-z")
        print("- Quitter : 0")
        print("- fermer pince : p")
        print("- ouvrir pince : -p")
        m=input("---> Commande : ")
        if m=="x":
            robot.arm.shift_pose(RobotAxis.X, 0.05)
        elif m=="-x":
            robot.arm.shift_pose(RobotAxis.X, -0.05)
        elif m=="y":
            robot.arm.shift_pose(RobotAxis.Y, 0.05)
        elif m=="-y":
            robot.arm.shift_pose(RobotAxis.Y, -0.05)
        elif m=="z":
            robot.arm.shift_pose(RobotAxis.Z, 0.05)
        elif m=="-z":
            robot.arm.shift_pose(RobotAxis.Z, -0.05)
        elif m=="p":
            robot.tool.grasp_with_tool()
        elif m=="-p":
            robot.tool.release_with_tool()
        else:
            m=int(m)



espacement=0.16
tailledisque=0.025
hauteur=0.27

def robothanoi(robot,action,p1,p2,p3):

    print("pos initiale")
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, -math.pi/2, 0.0])
    print("Relache pince")
    robot.tool.release_with_tool()

    print("Mouvement 1")
    if action[0]==1:
        robot.arm.shift_pose(RobotAxis.Y, -espacement)
        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p1))
    elif action[0]==2:
        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p2))
    elif action[0]==3: 
        robot.arm.shift_pose(RobotAxis.Y, espacement)

        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p3))

    print("Ferme pince")
    robot.tool.grasp_with_tool()

    print("Retour pos initiale")
    robot.arm.shift_pose(RobotAxis.Z, 0.20)
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, -math.pi/2, 0.0])

    print("Mouvement 2")
    if action[1]==1:
        robot.arm.shift_pose(RobotAxis.Y, -espacement)
        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p1))
    elif action[1]==2:
        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p2))
    elif action[1]==3:
        robot.arm.shift_pose(RobotAxis.Y, espacement)
        robot.arm.shift_pose(RobotAxis.Z, -hauteur+decalage(p3))

    print("Ouverture pince")
    robot.tool.release_with_tool()
    print("Remontée")
    robot.arm.shift_pose(RobotAxis.Z, hauteur)
    robot.arm.move_joints([0.0, 0.0, 0.0, 0.0, -math.pi/2, 0.0])

def decalage(L):
    h=0
    for k in range (len(L)-2):
        if L[k]!=0:
            h=h+tailledisque
    return(h)









