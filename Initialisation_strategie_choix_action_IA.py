"""
Ce programme enregistre dans strategie_choix_action_IA.json la stratégie de base car on ne sait pas coder de json.
Maintenant strategie_choix_action_IA.json rempli, ce programme ne sert à rien mais est conservé au cas où
strategie_choix_action_IA.json devait être altéré, auquel cas lancer ce programme permettrait de le re-générer.

La stratégie à adopter dépend de 3 facteurs:

    - la structure du jeu de l'IA:
        - 'doublon' s'il contient une paire
        - 'AS' s'il contient un AS
        - 'normal' dans les autres cas

    - le score de l'IA
        - score minimal du jeu de l'IA
        - retirer 1 à ce score si on est dans la cas 'AS'

    - ls score du croupier (valeur de la carte visible du croupier)
        - 10 si c'est un valet, une dame ou un ace
        - la valeur nominale de la carte sinon (donc ace vaut 1)

        
Pour accéder à l'action à choisir en fonction pour une situation donnée:

    action = strategie_choix_action_IA [ structure ] [ score_IA ] [ score_croupier ]

"""

import json as js
L1, L2, L3 = [], [], []

I = 'impossible'
T = 'tirer'
A = 'abandonner'
D = 'doubler'
S = 'split'
R = 'rester'


# Remplissage de L1
for i in range(11):

    L1.append([])
    L1[i].append(I)


    if i == 0:

        for a in range(10):
            L1[i].append(I)


    elif i == 1:

        L1[i].append(T)

        for a in range(9):
            L1[i].append(S)


    elif i == 2:

        L1[i].append(T)

        for a in range(6):
            L1[i].append(S)

        for a in range(3):
            L1[i].append(T)


    elif i == 3:

        L1[i].append(A)

        for a in range(6):
            L1[i].append(S)

        for a in range(3):
            L1[i].append(S)


    elif i == 4:

        for a in range(4):
            L1[i].append(T)

        for a in range(2):
            L1[i].append(S)

        for a in range(4):
            L1[i].append(T)


    elif i == 5:

        L1[i].append(T)

        for a in range(8):
            L1[i].append(D)

        L1[i].append(T)


    elif i == 6:

        L1[i].append(T)

        for a in range(5):
            L1[i].append(S)

        for a in range(4):
            L1[i].append(T)


    elif i == 7:

        L1[i].append(A)

        for a in range(6):
            L1[i].append(S)

        for a in range(2):
            L1[i].append(S)

        L1[i].append(A)


    elif i == 8:

        L1[i].append(A)

        for a in range(8):
            L1[i].append(S)

        L1[i].append(A)


    elif i == 9:

        L1[i].append(R)

        for a in range(5):
            L1[i].append(S)

        L1[i].append(R)

        for a in range(2):
            L1[i].append(S)

        L1[i].append(R)


    else:

        L1[i].append(T)

        for a in range(9):
            L1[i].append(S)



# Remplissage de L2
for i in range(11):

    L2.append([])
    L2[i].append(I)


    if i == 0:

        for a in range(10):
            L2[i].append(I)


    elif i <= 3:

        for a in range(4):
            L2[i].append(T)

        for a in range(2):
            L2[i].append(D)

        for a in range(4):
            L2[i].append(T)


    elif i <= 5:
        
        for a in range(3):
            L2[i].append(T)

        for a in range(3):
            L2[i].append(D)

        for a in range(4):
            L2[i].append(T)


    elif i == 6:

        for a in range(2):
            L2[i].append(T)

        for a in range(4):
            L2[i].append(D)

        for a in range(4):
            L2[i].append(T)


    elif i == 7:

        L2[i].append(T)

        L2[i].append(R)

        for a in range(4):
            L2[i].append(D)

        for a in range(2):
            L2[i].append(R)

        for a in range(2):
            L2[i].append(T)


    elif i <= 10:

        for a in range(10):
            L2[i].append(R)



# remplissage de L3
for i in range(22):

    L3.append([])
    L3[i].append(I)


    if i <= 3:

        for a in range(10):
            L3[i].append(I)


    elif  i <= 7:

        L3[i].append(A)

        for a in range(9):
            L3[i].append(T)


    elif i == 8:

        for a in range(10):
            L3[i].append(T)


    elif i == 9:

        for a in range(2):
            L3[i].append(T)
        
        for a in range(4):
            L3[i].append(D)

        for a in range(4):
            L3[i].append(T)


    elif i <= 11:

        L3[i].append(T)

        for a in range(8):
            L3[i].append(D)

        L3[i].append(T)


    elif i == 12:

        L3[i].append(A)

        for a in range(2):
            L3[i].append(T)

        for a in range(3):
            L3[i].append(R)

        for a in range(4):
            L3[i].append(T)

    
    elif i <= 15:

        L3[i].append(I)

        for a in range(5):
            L3[i].append(R)

        for a in range(3):
            L3[i].append(T)

        L3[i].append(A)


    elif i == 16:

        L3[i].append(A)

        for a in range(5):
            L3[i].append(R)

        for a in range(2):
            L3[i].append(T)

        for a in range(2):
            L3[i].append(A)


    elif i == 17:

        L3[i].append(A)

        for a in range(9):
            L3[i].append(R)


    else:
        for a in range(10):
            L3[i].append(R)


strategie_choix_action_IA = {'doublon': L1, 'AS': L2, 'normal': L3}

strategie_choix_action_IA_json = open('strategie_choix_action_IA.json', 'w')
js.dump(strategie_choix_action_IA, strategie_choix_action_IA_json, sort_keys=True, indent=4)
strategie_choix_action_IA_json.close()
