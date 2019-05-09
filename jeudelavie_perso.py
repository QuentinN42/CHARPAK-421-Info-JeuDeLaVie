# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:55:50 2019

Simulateur du jeu de la vie de John Horton

@author: Lieumont Quentin, Waeckel Matthieu
"""


import sys
import time


from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect


TAILLE_x = 3000  # on met des tailles très grandes pour pas limiter
TAILLE_y = 3000
idem = False  # regardera si la generation présente est dans l'exact meme etat que la gen -1
cellsize = 10   # surface par defaut des cellules

# %%


def dessiner_grille(qp):
    """
    dessine la grille de l'automate cellulaire sur le QPainter qp
    """
    
    noir = QColor(0, 0, 0)
    blanc = QColor(252, 252, 252)
# Choix du pinceau noir
    qp.setPen(noir)
    global cellsize
    W = cellsize*len(vivante[0])
    H = cellsize*len(vivante)   # adapte la taille de la fenetre a celle du fichier
    w = 0
    h = 0
    x = 0
    y = 0
    grand_rectangle = QRect(cellsize, cellsize, W, H)
    qp.drawRect(grand_rectangle)
    for i, line in enumerate(vivante):   # vertical
        for j, val in enumerate(line):  # horizontal
            x =(j + 1) * cellsize
            y =(i + 1) * cellsize 
            w = cellsize
            h = cellsize
            petit_rectangle = QRect(x, y, w, h)
            if val:
                qp.fillRect(petit_rectangle, noir)
            else:
                qp.fillRect(petit_rectangle, blanc)
# qp.drawRect(petit_rectangle)
# %%


def decodage_ligne(ligne):
    """
    prend en entrée une ligne contenant des . et des O

    -------les O sont plus jolis que les * --------
    """
    nvlle_liste = []
    for k in ligne:
        if k == ".":
            nvlle_liste.append(False)
        else:
            if k == "O":  # les O sont plus jolis que les *
                nvlle_liste.append(True)
    return nvlle_liste
# %%


def initialiser_depuis_fichier(lien):
    """
    prend en entrée une la chaine de caractères représentant le chemin pour arriver au 
    fichier cible
    """
    results = []
    f = open(lien)
    for nb, ligne in enumerate(f):
        
        if nb > (TAILLE_y-1):
            print('trop haut!')
            return None
        if ligne[0] == '  # ':
            continue
               
        for num, i in enumerate(ligne):
            compteur = 0   # permet de tester que les lignes sont biens de même taille
            if compteur > 0:
                if len(f[nb]) != len(f[nb-1]):
                    return None
            if len(ligne) > (TAILLE_x-1):
                print('trop long!')
                return None
            if ligne[num] != '.' and ligne[num] != 'O' and ligne[num] != '\n':
                print('vos lignes ne contiennent pas les bons caractères')
                return None
            compteur += 1
        results.append(decodage_ligne(ligne))
            
    f.close()        
    return results
            
# %%


class FenetreDessin(QWidget):
    """
    Notre classe fenÃªtre qui permettra d'afficher l'Ã©tat de l'automate
    cellulaire
    """

    def paintEvent(self, event):
        """
        paintEvent est appelÃ©e chaque fois qu'il faut redessiner la fenÃªtre
        """
        qp = QPainter(self)
        dessiner_grille(qp)

# %%


def nombre_de_voisins(x, y):
    compteur = 0
    for i in range(x-1, x+2):
        if i < 0 or i > len(vivante)-1:
            continue
        for j in range(y-1, y+2):
            if j < 0 or j > len(vivante[i])-1:
                continue
            if i == x and j == y:
                continue
            if vivante[i][j]:
                compteur += 1
    return compteur

# %%


def etat_suivant(x, y):
    next_state = False
    if nombre_de_voisins(x, y) == 3 or(vivante[x][y] is True and nombre_de_voisins(x, y) == 2):   # les vivantes
        next_state = True
    elif(vivante[x][y] is False and nombre_de_voisins(x, y) != 3) or(vivante[x][y] is True and nombre_de_voisins(x, y) != 2):   # les mortes
        next_state = False
    return next_state

# %%


def recalculer_grille():
    global vivante
    x = len(vivante)
    y = len(vivante[0])
    vivante = [[etat_suivant(i, j) for j in range(y)] for i in range(x)]
    return vivante

# %%


def cpt():
    """
    nb de cellules vivantes
    """
    compteur = 0
    for i in vivante:
        for j in i:
            if j:
                compteur += 1
    return compteur


def replay():
    """
    si le tableau a change et il reste de cellules:
        boucler
    """
    while cpt() > 0 and idem is False:
        run_app()
# %%


if __name__ == '__main__':
    fichier = sys.argv[1]
    if sys.argv[1].split(".")[-1] == "txt":
        vivante = initialiser_depuis_fichier(fichier)
    else:
        from imagetotxt import run as decode
        decode(fichier)
        vivante = initialiser_depuis_fichier(fichier.split(".")[0]+".txt")

    n = int(sys.argv[2])
    if len(vivante)*cellsize > 700:
        cellsize = int(700/len(vivante))
    if len(vivante[0])*cellsize > 700:
        cellsize = int(700/len(vivante))
    
    def run_app():
        """
        recalcule tableau
        lance la fenetre
        """
        app = QApplication(sys.argv)
        global idem
        prectab = vivante
        for e in range(n):
            recalculer_grille()
        if prectab == vivante:
            idem = True
        else:
            idem = False
        fenetre = FenetreDessin()
        fenetre.setGeometry(20, 20, len(vivante[0])*cellsize, len(vivante)*cellsize)
        fenetre.setWindowTitle('Jeu de la Vie')
        fenetre.show()
# paintEvent(qp)
        app.exec()
    replay()
