"""
Ce programme enregistre dans strategie_choix_tirer_IA.json la stratégie suivi par une IA si celle-ci a
choisi de tirer car on ne sait pas coder de json.
Maintenant strategie_choix_tirer_IA.json rempli, ce programme ne sert à rien mais est conservé au cas où
strategie_choix_tirer_IA.json devait être altéré, auquel cas lancer ce programme permettrait de le re-générer.

La stratégie à adopter dépend de 3 facteurs:

    - la structure du jeu de l'IA:
        - 'AS' s'il contient un AS
        - 'normal' dans les autres cas

    - le score de l'IA
        - score minimal du jeu de l'IA
        - retirer 1 à ce score si on est dans la cas 'AS'

    - ls score du croupier (valeur de la carte visible du croupier)
        - 10 si c'est un valet, une dame ou un ace
        - la valeur nominale de la carte sinon (donc ace vaut 1)


Pour accéder à l'action à choisir en fonction pour une situation donnée:

    action = strategie_choix_tirer_IA [ structure ] [ score_IA ] [ score_croupier ]
"""

import json as js
L1, L2, = [], []

I = 'impossible'
T = 'tirer'
R = 'rester'


# Remplissage de L1
for i in range(22):

    L1.append([])
    L1[i].append(I)


    if i == 0:

        for a in range(10):
            L1[i].append(I)


    elif i <= 6:

        for a in range(10):
            L1[i].append(T)


    elif i == 7:

        for a in range(2):
            L1[i].append(R)

        for a in range(4):
            L1[i].append(T)

        for a in range(5):
            L1[i].append(R)


    else:

        for a in range(10):
            L1[i].append(R)



# Remplissage de L2
for i in range(22):

    L2.append([])
    L2[i].append(I)


    if i == 0:

        for a in range(10):
            L2[i].append(I)


    elif i <= 11:

        for a in range(10):
            L2[i].append(T)


    elif i == 12:

        for a in range(3):
            L2[i].append(T)

        for a in range(3):
            L2[i].append(R)

        for a in range(4):
            L2[i].append(T)


    elif i <= 16:

        L2[i].append(T)

        for a in range(5):
            L2[i].append(R)

        for a in range(5):
            L2[i].append(T)


    else:

        for a in range(10):

            L2[i].append(R)


strategie_choix_tirer_IA = {'AS': L1, 'normal': L2}

strategie_choix_tirer_IA_json = open('strategie_choix_tirer_IA.json', 'w')
js.dump(strategie_choix_tirer_IA, strategie_choix_tirer_IA_json, sort_keys=True, indent=4)
strategie_choix_tirer_IA_json.close()
