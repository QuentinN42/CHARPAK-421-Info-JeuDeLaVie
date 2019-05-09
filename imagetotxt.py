# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 17:49:45 2019

@author: Quentin Lieumont
"""

import cv2 
import sys


def run(nom_image):
    img = cv2.imread(nom_image)
    
    nom_fichier = nom_image.split(".")[0]
    
    f = open(nom_fichier + ".txt","w")
    
    for l in img:
        for px in l:
            if px[0]>128:
                f.write(".")
            else:
                f.write("O")
        f.write("\n")
    f.close()


if __name__=="__main__":
    run(sys.argv[1])
