import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
import math as math
from  PIL import Image

## Algorithme de ZHANG

def transfo(im): #transformer l'image en tableau de 01
    im=np.array(im[:,:,0])  #on selectionne le canal rouge d'une image
    im=np.array(im/255)     #on divise toutes les valeurs de l'array par 255 pour avoir un tableau de 01
    return(im)              #on retourne le tableau avec donc 0=noir et 1=blanc
    
        
def transition(i,j,im): #comptage du nombre de transitions noir-blanc dans le sens anti-horaire
    K=0                                                      #on initie le compteur de transition
    X=im                                                     #plus facile a manipuler
    if X[[j+1],[i]]!=X[[j+1],[i+1]] and X[[j+1],[i]]==0:     # on verifie que le pixel A est noir et que le pixel voisin sens horaire B soit blanc
        K=K+1                                                #le compteur de transitions prend la valeur K+1
    if X[[j+1],[i+1]]!=X[[j],[i+1]] and X[[j+1],[i+1]]==0:   #idem, mais on continue dans le sens horaire
        K=K+1
    if X[[j],[i+1]]!=X[[j-1],[i+1]] and X[[j],[i+1]]==0:     #idem
        K=K+1
    if X[[j-1],[i+1]]!=X[[j-1],[i]]  and X[[j-1],[i+1]]==0:
        K=K+1
    if X[[j-1],[i]]!=X[[j-1],[i-1]] and X[[j-1],[i]]==0:
        K=K+1
    if X[[j-1],[i-1]]!=X[[j],[i-1]] and X[[j-1],[i-1]]==0:
        K=K+1
    if X[[j],[i-1]]!=X[[j+1],[i-1]] and X[[j],[i-1]]==0:
        K=K+1 
    if X[[j+1],[i-1]]!=X[[j+1],[i]] and X[[j+1],[i-1]]==0:   #on boucle le tour en revenant au point de depart
        K=K+1
    return(K)
    
def comptage_noir(X,Y,im): #comptage du nombre de pixels noirs voisins du pixel de coordonnees (X,Y) 
    K=0
    if im[[Y+1],[X]]==0:    #on verifie que le pixel de coordonnees Y+1,X est noir
        K=K+1
    if im[[Y+1],[X+1]]==0:  #idem pour Y+1,X+1
        K=K+1
    if im[[Y],[X+1]]==0:    #etc.
        K=K+1
    if im[[Y-1],[X+1]]==0:   
        K=K+1
    if im[[Y-1],[X]]==0:
        K=K+1
    if im[[Y-1],[X-1]]==0:
        K=K+1
    if im[[Y],[X-1]]==0:
        K=K+1
    if im[[Y+1],[X-1]]==0:
        K=K+1
    return (K)
    
        
#verification de Zhang1        
        
def P246(i,j,im): 
    return(im[[j+1],[i]]==1 or im[[j],[i+1]]==1 or im[[j-1],[i]]==1) #on verifie qu'au moins un des pixels S,E,N est blanc

def P468(i,j,im):
    return( im[[j],[i+1]]==1 or im[[j-1],[i]]==1 or im[[j],[i-1]]==1) #idem mais N,W,E

#verification de Zhang2
        
def P248(i,j,im):
    return(im[[j+1],[i]]==1 or im[[j],[i+1]]==1 or im[[j],[i-1]]==1) #idem mais S,W,E
        
def P628(i,j,im):
    return(im[[j+1],[i]]==1 or im[[j-1],[i]]==1 or im[[j],[i-1]]==1)  #idem mais S,W,N


#Les 2 sous  iterations qui suivent prennent pour argument un tableau de 0 et de 1. Elles notent les pixels frontiere 
#dans une liste puis la balaye  et les pixels qui y sont inscrits deviennent blancs. Les 2 fonctionnent de 
#manieres similaires et retournent un tableau de plus en plus proche  du squelette.

def Zhang1(im): #premiere sous iteration 
    X1,Y1=[],[]                              #on cree une liste vide dans laquelle on met les abscisses des pixels a eliminer,idem pour les ordonees
    for i in range(1, np.size(im,1)-1):      #on fait un balayage du tableau en verifiant la condition : le pixel n'appartient pas au bord en x 
        for j in range(1,np.size(im,0)-1):   # idem en y
            if im[[j],[i]]==0:               #on verifie que le pixel est noir
                if 2<=comptage_noir(i,j,im)<=6  and transition(i,j,im)==1 and P246(i,j,im) and P468(i,j,im):
                #on verifie que le pixel est de type frontiere
                #on verifie qu'il est connecte a un ensemble
                #on verifie qu'il valide les conditions de premiere iteration
                    X1.append(i)    #on fait rentrer son abscisse dans une liste
                    Y1.append(j)   #on fait rentrer son ordonnee dans une liste
    print(X1)                  #controle
    for k in range (len(X1)):
        im[[(Y1[k])],[(X1[k])]]=1 #tout les pixels dont les coordonnees sont dans la liste deviennent blancs
    return(im, len(X1)!=0)   


    
def Zhang2(im): #deuxieme sous iteration 
    X2,Y2=[],[]
    for i in range(1,np.size(im,1)-1):
        for j in range(1,np.size(im,0)-1):
            if im[[j],[i]]==0:
                if 2<=comptage_noir(i,j,im)<=6 and transition(i,j,im)==1 and P248(i,j,im) and P628(i,j,im):
                #idem mais conditions differentes
                        X2.append(i)
                        Y2.append(j)
    print(X2)
    for k in range (len(X2)):
        im[[Y2[k]],[X2[k]]]=1
    return(im, len(X2)!=0)


#assembler

def Squelettisation(adresse): #algorithme de squelettisation
    im=transfo(img.imread(adresse))     #on transforme l'image en un array de 0 et de 1
    U=Zhang1(im)                        #on effectue une première iteration
    V=Zhang2(im)                        #... une deuxieme
    while U[1] and V[1] :               #tant que les listes des 2 sous iterations ne sont pas vide on itere
        U=Zhang1(im)                    #on itere
        V=Zhang2(im)                    #on affiche l'image squelettisee
    return(im)                          #on retourne le tableau de 0 et de 1 squelettise
    
def retransfo(im):#transformer tableau de 01 en image squelettisee
    im=im*255
    img = Image.fromarray(im)   #obtenir une image noir / blanc a partir du tableau
    plt.xlim(0,np.size(im,1))   #on delimite le graphe : en x
    plt.ylim(0,np.size(im,0))
    plt.gca().invert_yaxis()   #....................... en y
    plt.imshow(img)    
    
##Extraction Minuties 

def position_minuties(im): #extraction des minuties 
    Liste_minuties=[]                                    #on cree une liste pour les abscisses et les ordonees
    for i in range (1, np.size(im,1)-1):    #on fait un balayage de l'image
        for j in range (1,np.size(im,0)-1):
            if transition(i,j,im)==3:       #un pixel de minutie est connecte a 3 ensembles
                Liste_minuties+=[[i,j]]
    return Liste_minuties   # liste des coordonnees de chaque minuties [[x1,y1],[.,.]]

##analyse des cartes de minuties

def tri_rapide(L): #on trie ces coordonnees de haut en bas par tri rapide
    if L == []:
        return []
    else:
        L1=[]
        L2=[]
        for k in range (1,len(L)):
            if L[k][1]<=L[0][1]:
                L1.append(L[k])
            else:
                L2.append(L[k])
    return tri_rapide(L1)+[L[0]]+tri_rapide(L2) # tri la liste L pour avoir les y dans l'ordre croissant 
    


def Pythagore(l): # distance entre les minuties voisines
    D=[]                                                            #on cree une liste vide que l'on remplit avec ces distances
    for k in range (len(l)-1):
        D+=[np.sqrt((l[k][0]-l[k+1][0])**2+(l[k][1]-l[k+1][1])**2)] #d'apres pythagore
    return D                                                        #liste des distance entre les minuties

    

def angle(l):
    A=[]                                     #on cree une liste vide dans laquelle on inscrira les "demi-angles"
    Angles=[]                                #on cree une liste vide dans laquelle on inscrira les angles               
    for k in range (len(l)-1):               #on balaye les coordonnes des  minuties
        deltaX = (l[k+1][0] - l[k][0])       #on calcule la difference entre les abscisses
        deltaY = (l[k+1][1] - l[k][1])       #...................................ordonnees
        if deltaX != 0:                      
            if l[k][0] < l[k+1][0]:
                teta = math.atan(deltaY/deltaX) 
            else:
                teta = math.pi + math.atan(deltaY/deltaX)
        else:                              
            if l[k][1] < l[k+1][1]:        
                teta = - math.pi/2          
            else:
                teta = math.pi/2           
        A+=[teta]                           
    for a in range(len(A)-1):                
        Angles+=[A[a]+A[a+1]]              
    return Angles                                   #on retourne la liste des angles entre les segments


def tolerance(L,i):              #programme qui retourne la liste des arondis a i pres
    l=[]                         #on cree une liste vide
    for k in L :                 #on balaye la liste
        l.append(round(k,i))     #on rempli la liste vide avec les arrondis
    return(l)                    #on retourne la liste des arrondis
  
    
def assoc(A,P):                     #programme qui retourne la liste de couples d'angles(A)/longueurs(P)
    L=[]                            #on cree une liste vide
    for l in range(len(A)):         #on balaye la liste
            L.append([A[l],P[l]])   #on rempli la liste vide avec les couples de variables
    return(L)                       #on retourne la liste des couples
      
       
def compar(L1,L2):                  #programme qui retourne le nombre d'elements communs de 2 listes
    k=0
    for w in range(len(L1)):        #on balaye la premiere liste couple angle/longeur des 2 images
        for i in range(len(L2)):    #on balaye la seconde liste
            if L1[w]==L2[i]:        #si 2 elements de la listes sont identiques...
                L2[i]=None          #... l'element de la liste prend la valeur None
                L1[w]=False         #... l'element de la seconde liste prend la valeur False de telle façon que 2 elements identiques ne le soient plus avec aucun autre element de la liste
                k=k+1
    return(k)                       #on retourne le nombre d'elements identiques
    
def decompo_liste(Liste_minuties): #on decompose une liste de liste en 2 listes separees pour les plots
    x,y=[],[]                                #on cree 2 listes vides a remplir
    for k in range(len(Liste_minuties)):     #on balaye la liste a decomposer
        x=x+[Liste_minuties[k][0]]           #on ajoute dans les listes les elements interessants
        y=y+[Liste_minuties[k][1]]
    return(x,y)                              #on retourne les 2 listes

def comparaison_empreintes():
    adresse1,adresse2=input('first picture adress : '),input('second picture adress : ') #on charge la premiere image
    im1,im2=Squelettisation(adresse1),Squelettisation(adresse2)                                        #on les squelettise
    Liste_minuties1,Liste_minuties2=position_minuties(im1),position_minuties(im2)                      #on en extraie les minuties                      
    l1,l2=tri_rapide(Liste_minuties1),tri_rapide(Liste_minuties2)                                      #on tri ces listes de minuties
    X1, Y1 =decompo_liste(l1)                                                              #on les decompose en listes pour le plot
    X2, Y2= decompo_liste(l2)

    plt.subplot(2,3,1)          #1er plot
    img1 = img.imread(adresse1) #on charge la 1ere image
    plt.imshow(img1)            #on montre cette image
   
    plt.subplot(2,3,4)          #2eme plot
    img2 = img.imread(adresse2) #on charge la 2eme image
    plt.imshow(img2)            #on montre cette image
    
    
    plt.subplot(2,3,2)          #3eme plot
    retransfo(im1)              #on charge la 1ere image squelettise
   
    
    plt.subplot(2,3,5)          #4eme plot
    retransfo(im2)              #idem pour la 2eme image
   
    
    plt.subplot(2,3,3)          #5eme plot
    retransfo(im1)              #on montre l'image squelettisée
    plt.plot(X1,Y1,'o')         #on plot des points le sur les minuties
    plt.plot(X1,Y1)             #on plot les vecteurs entre les differentes minuties
    plt.draw()                  #on le montre
    
    plt.subplot(2,3,6)          #6eme plot
    retransfo(im2)              #idem mais pour la seconde image
    plt.plot(X2,Y2,'o')
    plt.plot(X2,Y2)
    plt.draw()
   
    P1,P2=Pythagore(l1),Pythagore(l2)                #on determine les distances
    A1,A2=angle(l1),angle(l2)                        #on determine les angles
    a1,a2=tolerance(A1,0),tolerance(A2,0)            #on arrondit les listes
    p1,p2=tolerance(P1,-1),tolerance(P2,-1)
    l1,l2=assoc(a1,p1),assoc(a2,p2)
    if abs(len(l1)-len(l2))>10:                 #si les 2 empreintes on un nombre de 'vecteurs' trop different.....
        return ('it is not  match')             #... alors elles sont differentes
    else:
        if compar(l1,l2)>=10:                    #si 2 empreintes ont plus de 10 'vecteurs' communs
            resultat = 'it is a match'           #...alors elles sont identiques
        else:
            resultat= 'it is not  match'         #... autrement, elles sont differentes
    plt.suptitle(resultat)
    plt.show()
    
##instructions pour faire fonctionner le programme
#lalaunch comparaison_empreintes()
#follow the instructions
#NB: it's quite slow