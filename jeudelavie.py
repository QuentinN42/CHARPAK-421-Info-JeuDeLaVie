#!/usr/bin/env python3
"""
Simulateur du jeu de la vie de John Horton Conway

S4 : janvier 2019

@author : Quentin Lieumont

"""

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect


vivante = [[False, False, False, True],
           [False, False, True, False],
           [False, True, False, True],
           [True, False, False, False]]
TAILLE_X = 30
TAILLE_Y = 30
cellSize = 50
n_gen = 1


#                                       Decodage Fichier

def decodage_ligne(ligne):
    """
    decode une ligne : * = True, . = False
    et None si pb
    """
    decode = [True if car == "*" else False if car == "." else None for car in ligne]
    if None in decode:
        return None
    else:
        return decode


def initialiser_depuis_fichier(lien):
    """
    prend un fichier et le decode si il est valide :
        nb de ligne < TAILLE_Y
        toutes les lignes doivent etre les memes et ne pas depasser TAILLE_X
        il n'y a pas de caracteres non valides
    et None si pb
    """
    xmax = TAILLE_X
    ymax = TAILLE_Y
    # lit le fichier
    f = open(lien, 'r')
    txt = f.read().split("\n")
    f.close()
    # suprime les coms et les lignes vides
    lignes_non_commentees = [ligne for ligne in txt if len(ligne) > 0 if ligne[0] != "#"]
    # detecte l'erreur sur Y
    if len(lignes_non_commentees) > ymax:
        print("Error in file ", lien,
              " : Max lines numbers reach : max = ", ymax,
              " get : ", len(lignes_non_commentees))
        return None

    # cree le tableau des longueurs
    len_lignes = sorted([len(l) for l in lignes_non_commentees])

    # detecte l'erreur sur X
    if len_lignes[0] != len_lignes[-1] or len_lignes[-1] > xmax:
        print("Error in file ", lien,
              " : Max lines len reach or different lines len")
        return None

    # si tout est bon, decode chaque ligne et les renvoit
    decode = [decodage_ligne(ligne) for ligne in lignes_non_commentees]
    if None in decode:
        print("Error in file ", lien,
              " : other car than . or *")
        return None
    else:
        return decode


#                                       Simulation


def nombre_de_voisins(x, y):
    """
    Renvoie le nombre de voisins
    on fera attention aux cas extremes :
        x/y = 0
        x/y = taille max du tableau en x/y
    """
    tab = vivante
    v = []  # tableau des voisins
    if x != 0:
        v.append(tab[x - 1][y])
        if y != 0:
            v.append(tab[x - 1][y - 1])
        if y <= len(tab[x]) - 2:
            v.append(tab[x - 1][y + 1])
    if x <= len(tab) - 2:
        v.append(tab[x + 1][y])
        if y != 0:
            v.append(tab[x + 1][y - 1])
        if y <= len(tab[x]) - 2:
            v.append(tab[x + 1][y + 1])
    if y != 0:
        v.append(tab[x][y - 1])
    if y <= len(tab[x]) - 2:
        v.append(tab[x][y + 1])
    return sum(map(int, v))


def etat_suivant(x, y):
    """
    renvoit si une cellule vas etre vivante
        si nb voisins = 3 : True
        si nb voisins = 2 et deja vivante : True
        sinon False
    """
    tab = vivante
    v = nombre_de_voisins(x, y)
    return v == 3 or (v == 2 and tab[x][y])


def recalculer_grille():
    """
    Pour chaque case du tableau,
    calculer l'etat suivant
    """
    global vivante
    lenx = range(len(vivante))
    leny = range(len(vivante[0]))
    vivante = [[etat_suivant(x, y) for y in leny] for x in lenx]


#                                       Dessin

def dessiner_grille(qp):
    """
    dessine la grille tab de l'automate cellulaire sur le QPainter qp avec une taille cellSize
    parcours le tableau vivante et met:
        un rectangle blanc si cellule morte (False)
        un rectangle noir si cellule vivante (True)
    """
    tab = vivante
    # init pos
    x = 0
    y = 0
    # coulleur
    b = QColor(0, 0, 0)
    w = QColor(255, 255, 255)
    qp.setPen(b)
    for E in tab:
        for e in E:
            r = QRect(x, y, cellSize, cellSize)
            if e:
                qp.fillRect(r, b)
            else:
                qp.fillRect(r, w)
            qp.drawRect(r)
            x += cellSize
        y += cellSize
        x = 0
    pass


#                                       Class


class FenetreDessin(QWidget):
    """
    Notre classe fenetre qui permettra d'afficher l'etat de l'automate
    cellulaire
    """

    def paintEvent(self, event):
        """
        paintEvent est appelee chaque fois qu'il faut redessiner la fenetre
        """
        qp = QPainter(self)
        dessiner_grille(qp)


#                                       Main


if __name__ == '__main__':
    def run_app():
        """

        """
        # test des arguments
        if len(sys.argv) != 3:
            print("Error : waiting 2 args :")
            print(" - file name")
            print(" - number of generations")
            return
        else:
            # recuperation grille
            global vivante
            global cellSize
            global n_gen
            vivante = initialiser_depuis_fichier(sys.argv[1])

            # resize les cellules
            if cellSize*len(vivante) > 1820:
                cellSize = 1820/len(vivante)
            if cellSize*len(vivante[0]) > 980:
                cellSize = 980 / len(vivante[0])

            # recalcule n fois la grille
            n_gen = int(sys.argv[2])
            for e in range(n_gen):
                recalculer_grille()

            # lance l'affichage
            app = QApplication(sys.argv)
            f = FenetreDessin()
            f.resize(len(vivante[0]) * cellSize + 1, len(vivante) * cellSize + 1)
            f.setWindowTitle("Jeu de la Vie")
            f.show()
            sys.exit(app.exec_())


    run_app()
