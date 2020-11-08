# empreinteDigitales
# 2018-Hippolyte CORDIER

Ce code rudimnentaire permet de recconnaitre des empreintes digitales en noir et blanc au format .bmp
Il squelettise une image et identifie des point d'interret appelé minutie.

Les minuties sont :
-des lacs
-des divergence
-des fourche

Ces points sont caractérisés par une connectivité >2.
C'est à dire qu'un pixel et connecté à plus de 2 pixels.

Ces minuties forment ensuite un pattern de vecteur et c'est ce pattern qui est recconnu entre deux images.


Amélioration:
-Parallèlisation
-implémentaion d'anti-crénelage
-pré-traitement automatique
-réorganisation
