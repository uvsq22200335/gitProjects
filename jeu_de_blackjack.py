"""
Ce jeu permet de jouer au Black Jack:
    - seul, en multijoueur ou avec des IA
    - avec des mises
    - avec le split

le dictionnaire joueurs est de la forme:

{
nom du premier joueur :{
                        'intelligence: 'humaine' ou 'artificielle',
                        'mains': [
                                    {
                                        'mise': mise associée,
                                        'jeu': [
                                                    {
                                                        'valeur': valeur de la carte (str),
                                                        'couleur': couleur de la carte (str)
                                                    }
                                                    , ...
                                                ],
                                    },
                                    {...}
                                    ]
                        'richesse': richesse actuelle, dont on a déjà déduit la mise (int)
                        },

nom du deuxième joueur:...
}

mains contient plusieurs mains car split possible

croupier est de la forme: [{'valeur': valeur de la carte, 'couleur': couleur de la carte}, ...]
"""

import random as rd
import json as js


def sauvegarde():
    """ sauvegarde le dictionnaire joueurs dans le fichier sauvegarde_partie.json """
    global joueurs
    sauvegarde_json = open("sauvegarde_partie.json", 'w')
    js.dump(joueurs, sauvegarde_json, sort_keys=True, indent=4)
    sauvegarde_json.close()


def recuperation_dictionnaire(fichier: str):
    """ retourne le dictionnaire contenu dans le fichier """
    fichier_json = open(fichier, 'r')
    fichier_str = fichier_json.read()
    fichier_json.close()
    fichier = js.loads(fichier_str)
    return fichier


def creation_sabot():
    """ retourne une liste contenant toutes les cartes du sabot mélangées """
    valeurs = [str(i) for i in range(1, 11)] + ['J', 'Q', 'K']
    couleurs = ['pique', 'coeur', 'carreau', 'trefle']
    sabot = 6 * [{'valeur': valeur, 'couleur': couleur} for couleur in couleurs for valeur in valeurs]
    rd.shuffle(sabot)
    return sabot


def mise_totale(mains: list):
    """
    Renvoie la mise totale de la main
    """
    S = 0
    for main in mains:
        S += main['mise']

    return S


def score(jeu: list):
    """
    calcule la valeur totale d'un jeu et renvoie {min, max}
    (deux éléments car valeur dépend des AS et 2 valeurs idéales possibles selon le contexte)
    """
    AS = 0
    total = 0
    for carte in jeu:
        if carte['valeur'] in ['10', 'J', 'Q', 'K']:
            total += 10

        elif carte['valeur'] == '1':
            AS += 1

        else:
            total += int(carte['valeur'])

    total_min = total + AS

    if AS == 0:
        total_max = total
    else:
        total_max = total + 11 * AS - AS + 1

    return {'min': total_min, 'max': total_max}


def detect_black_jack(main: list):
    """
    Renvoie True si la main a black jack, False sinon
    """
    return ((main[0]['valeur'] in ['10', 'J', 'Q', 'K'] and main[1]['valeur'] == '1')
            or (main[1]['valeur'] in ['10', 'J', 'Q', 'K'] and main[0]['valeur'] == '1'))


def choix(texte: str, alternatives: list):
    """
    Remplace les boutons en attendant une interface graphique,
    permet de simuler la sélection d'un bouton
    """
    action = input('\n' + texte)
    while action not in alternatives:

        action = input('\n' + texte)

    return action


def entree_valeur(texte: str):
    """
    Remplace temporairement la sélection de valeurs
    par jetons en attendant l'interface graphique
    """
    valeur = 1
    while valeur % 5 != 0 or valeur <= 0:
        valeur = int(input('\n' + texte))

    return valeur


def tirer(jeu: list):
    """ Fait tirer une carte au jeu """
    global sabot, joueurs
    jeu.append(sabot[-1])
    del sabot[-1]


def affichage(joueur: str):
    """ affiche clairement la situation de joueur en attendant l'interface graphique"""
    global joueurs
    print('\n' + joueur + ": ")
    print("richesse", joueurs[joueur]['richesse'])

    for indice_main in range(len(joueurs[joueur]['mains'])):
        print("\n", "main", indice_main, ":")
        print("   jeu:", joueurs[joueur]['mains'][indice_main]['jeu'])
        print("   mise associée", joueurs[joueur]['mains'][indice_main]['mise'])


def choix_nb_joueurs():
    """ retourne le nombre de joueurs demandé par l'utilisateur """
    nombre_de_joueurs = int(input("Indiquez le nombre de joueurs désiré (IA + joueurs réels) "))
    while not 0 < nombre_de_joueurs <= 7:
        nombre_de_joueurs = int(input("Indiquez le nombre de joueurs désiré (IA + joueurs réels) "))

    return nombre_de_joueurs


def creation_joueurs():
    """ Fait entrer leurs noms aux utilisateurs """
    joueurs = {}
    i = 0
    while i < nb_joueurs:
        joueur = str(input('\n' + 'Nom du nouveau joueur (si fin des joueurs humains ne rien écrire): '))

        if joueur == "":
            i = nb_joueurs

        elif joueur not in joueurs.keys():
            joueurs[joueur] = {'intelligence': 'humaine'}
            i += 1

    return joueurs


def creation_IA():
    """ Complète la liste de joueurs avec des IA pour qu'il y ait le bon nombre de joueurs """
    global joueurs, nb_joueurs
    liste_IA = [nom for nom in personnages_IA.keys()]
    rd.shuffle(liste_IA)
    for nom_IA in liste_IA:
        if not(nom_IA in joueurs.keys()) and len(joueurs) < nb_joueurs:
            joueurs[nom_IA] = {'intelligence': 'artificielle'}


def initialisation_richesses():
    """ Demande la richesse de départ à l'utilisateur, puis l'assigne à chaque joueur """
    global joueurs
    richesse_initiale = entree_valeur("Richesse initiale? ")
    for joueur in joueurs.keys():
        joueurs[joueur]['richesse'] = richesse_initiale


def initialisation_mains():
    """ associe une main vide à chaque joueur et une liste vide au croupier"""
    global croupier, joueurs
    croupier = []
    for joueur in joueurs.keys():
        joueurs[joueur]['mains'] = [{'mise': 0, 'jeu': []}]


def distribution():
    """
    distribue les cartes aux joueurs et au croupier
    dans le même ordre que dans la vraie vie au cas où ça pourrait aider pour l'interface graphique
    """
    global croupier, joueurs
    for repet in range(2):
        for joueur in joueurs.keys():
            tirer(joueurs[joueur]['mains'][0]['jeu'])

        tirer(croupier)


def mise_artificielle(joueur: str):
    """
    Fait miser l'intelligence artificielle correspondant au joueur
    (différentes prises de risque en fonction des IA)
    composante aléatoire dans la mise pour donner une illusion d'humanité
    """
    global joueurs, IA
    mise = int(rd.uniform(0.5, 1.5) * personnages_IA[joueur] * joueurs[joueur]['richesse']) + 5
    mise += 5 - mise % 5
    joueurs[joueur]['mains'][0]['mise'] = min(mise, joueurs[joueur]['richesse'])


def mise_joueur(joueur: str):
    """ Fait choisir au joueur une mise compatible avec sa richesse """
    global joueurs
    valeur = entree_valeur(joueur + ", que voulez-vous miser? (votre richesse: " + str(joueurs[joueur]['richesse']) + ") ")
    while valeur > joueurs[joueur]['richesse']:
        valeur = entree_valeur("Cette mise est au-dessus de vos moyens. " +
                               joueur + ", que voulez-vous miser? ")

    joueurs[joueur]['mains'][0]['mise'] = valeur


def mise():
    """ Fait miser tout le monde """
    global joueurs
    for joueur in joueurs.keys():
        if joueurs[joueur]['intelligence'] == 'artificielle':
            mise_artificielle(joueur)

        else:
            mise_joueur(joueur)

        joueurs[joueur]['richesse'] -= joueurs[joueur]['mains'][0]['mise']


def black_jack():
    """
    après le début du tour, gére les cas où :
    - un joueur fait black jack
    - le croupier fait black jack
    - les deux à la fois

    L'arrondi pour congruence à 5 de la division d'une mise
    lorsqu'un joueur remporte 3/2 de sa mise avantage le le joueur
    """
    global joueurs, croupier
    if detect_black_jack(croupier):
        print('\n', "le croupier a réalisé un black jack:", croupier)

        for joueur in list(joueurs):

            if detect_black_jack(joueurs[joueur]['mains'][0]['jeu']):
                joueurs[joueur]['richesse'] += joueurs[joueur]['mains'][0]['mise']
                print('\n', joueur, "a réalisé un black jack (",
                      joueurs[joueur]['mains'][0]['jeu'], "),", joueur, "réccupère donc sa mise")

            else:
                print('\n', joueur, "n'a pas réalisé de black jack (",
                      joueurs[joueur]['mains'][0]['jeu'], "),", joueur, "ne réccupère donc pas sa mise")

            joueurs[joueur]['mains'][0]['mise'] = 0
            joueurs[joueur]['mains'][0]['jeu'] = []

        croupier = []

    else:
        # la variable nb_black_jack sert à détecter le cas où tous les joueurs ont black jack
        for joueur in list(joueurs):
            if detect_black_jack(joueurs[joueur]['mains'][0]['jeu']):
                print('\n', "contrairement au croupier,", joueur, "a réalisé un black jack (", joueurs[joueur]['mains'][0]['jeu'],
                      ")", joueur, "réccupère donc 3/2 de sa mise soit", (3*joueurs[joueur]['mains'][0]['mise'] + joueurs[joueur]['mains'][0]['mise'] % 10) // 2)

                joueurs[joueur]['richesse'] += (3*joueurs[joueur]['mains'][0]['mise'] + joueurs[joueur]['mains'][0]['mise'] % 10) // 2
                joueurs[joueur]['mains'][0]['mise'] = 0
                joueurs[joueur]['mains'][0]['jeu'] = []

        if [joueur for joueur in joueurs.keys() if joueurs[joueur]['mains'][0]['mise'] != 0] == []:
            croupier = []


def explosion_joueur(joueur: str, indice_main: int):
    """
    Met à 0 la mise et la main du joueur s'il dépasse 21
    """
    global joueurs
    affichage(joueur)
    if score(joueurs[joueur]['mains'][indice_main]['jeu'])['min'] > 21:
        print('\n' + joueur + ", vous avez dépassé 21, votre main", indice_main, "perd donc la manche")
        joueurs[joueur]['mains'][0]['mise'] = 0
        joueurs[joueur]['mains'][indice_main]['jeu'] = []


def choix_IA(joueur: str, indice_main: int, liste_actions: list):
    """
    Si 'abandonner' in liste_actions (<=> on est dans choix_action)
        retourne le meilleur choix d'action possible en se référant à la stratégie
        de base qui est contenue dans le dictionnaire strategie_choix_action_IA si

    Si 'abandonner' not in liste_actions (<=> on est dans choix_tirer)
        retourne le meilleur choix d'action possible en se référant à la stratégie
        contenue dans le dictionnaire strategie_choix_tirer_IA
    """
    global joueurs, croupier, strategie_choix_action_IA, strategie_choix_tirer_IA

    jeu = joueurs[joueur]['mains'][indice_main]['jeu']
    score_jeu = score(jeu)['min']

    if croupier[0]['valeur'] in ['J', 'Q', 'K']:
        score_croupier = 10

    else:
        score_croupier = int(croupier[0]['valeur'])

    if 'split' in liste_actions:
        structure = 'doublon'
        score_jeu //= 2

    # s'il y a un as dans la main
    elif score(jeu)['min'] != score(jeu)['max']:
        structure = 'AS'
        score_jeu -= 1

    else:
        structure = 'normal'


    # si la fonction ayant appelé choix_IA est choix_action
    if 'abandonner' in liste_actions:
        dico_strategie = strategie_choix_action_IA

    # si la fonction ayant appelé choix_IA est choix_tirer
    else:
        dico_strategie = strategie_choix_tirer_IA

    action = dico_strategie[structure][score_jeu][score_croupier]

    # si action == doubler et doubler impossible
    if action not in liste_actions:
        action = 'tirer'

    print(joueur, "choisit de", action, "avec sa main", indice_main)

    return action


def choix_action(joueur: str, indice_main: int):
    """
    Permet à joueur de décider de ce qu'il fait (rester, tirer...)
    contrairement à choix(joueur: str, txt: str), prend en compte que certains
    choix ne peuvent être faits que sous conditions:
        - doubler: richesse suffisante
        - split: cartes de la main similaires et richesse suffisante
    """
    global joueurs
    liste_actions = ['rester', 'tirer', 'abandonner']
    doubler = ""
    split = ""

    if joueurs[joueur]['richesse'] >= joueurs[joueur]['mains'][0]['mise']:
        doubler = ", 'doubler"
        liste_actions.append('doubler')

        if joueurs[joueur]['mains'][indice_main]['jeu'][0]['valeur'] == joueurs[joueur]['mains'][indice_main]['jeu'][1]['valeur']:
            split = ", 'split'"
            liste_actions.append('split')

    if joueurs[joueur]['intelligence'] == 'humaine':
        return choix(joueur + ", voulez-vous 'rester', 'tirer'" + doubler + split + " ou 'abandonner' avec votre main " + str(indice_main) + " ?", liste_actions)

    else:
        return choix_IA(joueur, indice_main, liste_actions)


def choix_tirer(joueur: str, indice_main: int):
    """
    Distribue une carte au joueur,
    puis lui propose jusqu'à ce que celui-ci atteigne 21 de tirer une carte ou de rester
    """
    global joueurs
    action = 'tirer'
    while action == 'tirer':
        tirer(joueurs[joueur]['mains'][indice_main]['jeu'])

        if score(joueurs[joueur]['mains'][indice_main]['jeu'])['min'] <= 21:
            affichage(joueur)
            if joueurs[joueur]['intelligence'] == 'humaine':
                action = choix(joueur + ', écrivez "tirer" pour tirer une carte, et "rester" pour rester avec votre main ', ['tirer', 'rester'])

            else:
                action = choix_IA(joueur, indice_main, ['tirer', 'rester'])

        else:
            action = 'rester'

    explosion_joueur(joueur, indice_main)


def abandonner(joueur: str, indice_main: int):
    """
    Le joueur perd sa main et récupère la moitié de la mise qui lui était associée
    L'arrondi pour congruence à 5 de la division de la mise avantage le croupier
    pour empêcher qu'un joueur misant 5 ne puisse garder l'intégralité de sa mise
    """
    global joueurs
    print(joueur, "abandonne avec sa main", indice_main,", il récupère donc la moitié de sa mise soit",
          (joueurs[joueur]['mains'][indice_main]['mise'] - joueurs[joueur]['mains'][indice_main]['mise'] % 10) // 2)

    joueurs[joueur]['richesse'] += (joueurs[joueur]['mains'][0]['mise'] - joueurs[joueur]['mains'][0]['mise'] % 10) // 2
    joueurs[joueur]['mains'][indice_main]['mise'] = 0
    joueurs[joueur]['mains'][indice_main]['jeu'] = []


def split(joueur: str):
    """
    sépare la main du joueur en deux mains et distribue une carte par main.
    Diminue de 1 le prochain indice de main de la prochaine action
    (pour que main[indice_main] repasse dans la boucle du tour du joueur
    si la paire n'est pas d'AS), et l'augmente d'un sinon
    (pour que main[indice_main] et main[indice_main] ne repassent/passent
    pas dans la boucle du tour du joueur si la paire est d'AS)
    """
    global joueurs, indice_main

    # 3 lignes compliquées car il faut bien que les deux jeux soient des listes indépendantes
    jeu_bis = [{'valeur': joueurs[joueur]['mains'][indice_main]['jeu'][1]['valeur'], 'couleur': joueurs[joueur]['mains'][indice_main]['jeu'][1]['couleur']}]
    main_bis = {'mise': joueurs[joueur]['mains'][indice_main]['mise'], 'jeu': jeu_bis}
    joueurs[joueur]['mains'].insert(indice_main + 1, main_bis)

    del joueurs[joueur]['mains'][indice_main]['jeu'][1]
    # del joueurs[joueur]['mains'][indice_main + 1]['jeu'][0]

    tirer(joueurs[joueur]['mains'][indice_main]['jeu'])
    tirer(joueurs[joueur]['mains'][indice_main + 1]['jeu'])

    if joueurs[joueur]['mains'][indice_main]['jeu'][0]['valeur'] == '1':
        indice_main += 1

    else:
        indice_main -= 1
    # remarque: pas d'explosion possible à 2 cartes


def doubler(joueur: str, indice_main: int):
    """ Double la mise du joueur puis lui fait tirer une carte et le fait exploser si nécessaire"""
    global joueurs
    joueurs[joueur]['richesse'] -= joueurs[joueur]['mains'][indice_main]['mise']
    joueurs[joueur]['mains'][indice_main]['mise'] *= 2
    tirer(joueurs[joueur]['mains'][0]['jeu'])
    explosion_joueur(joueur, indice_main)


def tour_croupier():
    """Fait tirer le croupier jusqu'à ce qu'il etteigne 17"""
    global sabot, croupier, joueurs
    print('\n', "Cartes du croupier:", croupier)
    while score(croupier)['max'] < 17:
        croupier.append(sabot[-1])
        del sabot[-1]
        print('\n', "Cartes du croupier:", croupier)

    if score(croupier)['max'] > 21:
        print("Le croupier a dépassé 21, il perd donc face à tous les joueurs restants")

        for joueur in joueurs.keys():
            for indice_main in range(len(joueurs[joueur]['mains'])):
                if joueurs[joueur]['mains'][indice_main]['mise'] != 0:
                    print('\n', joueur, "a récupère deux fois la mise associée à sa main", indice_main, "soit", 2 * joueurs[joueur]['mains'][indice_main]['mise'])
                    joueurs[joueur]['richesse'] += 2 * joueurs[joueur]['mains'][indice_main]['mise']
                    joueurs[joueur]['mains'][indice_main]['mise'] = 0


def resultats():
    """compare les résultats des joueurs à ceux du croupier puis répartit les gains

            Si main_croupier > main_joueur:
                Croupier réccupère la mise du joueur

            Sinon:
                le joueur réccupère 2 fois sa mise

    """
    global joueurs, croupier
    for joueur in joueurs.keys():
        for indice_main in range(len(joueurs[joueur]['mains'])):
            if joueurs[joueur]['mains'][indice_main]['mise'] != 0:

                total_cartes = score(joueurs[joueur]['mains'][indice_main]['jeu'])['max']
                if total_cartes > 21:
                    total_cartes = score(joueurs[joueur]['mains'][indice_main]['jeu'])['min']

                if total_cartes < score(croupier)['min']:
                    print('\n', "la main", indice_main, "de", joueur, "perd face au croupier")

                else:
                    print('\n', "la main", indice_main, "de", joueur, "gagne face au croupier,", joueur,
                          "récupère le double de la mise associée à sa main soit", 2 * joueurs[joueur]['mains'][indice_main]['mise'])

                    joueurs[joueur]['richesse'] += 2 * joueurs[joueur]['mains'][indice_main]['mise']

                print("croupier", croupier)
                print(joueur, joueurs[joueur]['mains'][indice_main])

                joueurs[joueur]['mains'][indice_main] = []

        joueurs[joueur]['mains'] = [{'mise': 0, 'jeu':  []}]

    croupier = []


def eliminations():
    """Elimine joueur et l'annonce si celui-ci n'a plus de richesse"""
    global joueurs
    noms = [nom for nom in joueurs.keys()]
    for joueur in noms:

        if joueurs[joueur]['richesse'] == 0:
            print('\n' + joueur + " n'a plus rien à miser,", joueur, "est éliminé de la partie")
            del joueurs[joueur]


# Initialisation des IA
personnages_IA = recuperation_dictionnaire('personnages_IA.json')
strategie_choix_action_IA = recuperation_dictionnaire('strategie_choix_action_IA.json')
strategie_choix_tirer_IA = recuperation_dictionnaire('strategie_choix_tirer_IA.json')


reprendre_partie = choix('Voulez-vous reprendre la partie précédente? Répondez "oui" ou "non": ', ['oui', 'non'])

if reprendre_partie == 'non':
    # Paramétrage du croupier, des joueurs et des IA
    croupier = []
    print()
    nb_joueurs = choix_nb_joueurs()
    joueurs = creation_joueurs()

    creation_IA()

    # Initialisation des richesses (au choix des joueurs)
    initialisation_richesses()


else:
    joueurs = recuperation_dictionnaire("sauvegarde_partie.json")

# Initialisation du sabot
sabot = creation_sabot()

# Boucle while des manches:
continuer = 'oui'

while continuer == 'oui':

    # Initialisation des mains
    initialisation_mains()

    # sauvegarde, faite ici et non uniquement après la boucle pour sauvegarder en cas de bug
    sauvegarde()

    # Initialisation du sabot s'il ne reste plus assez de cartes dedans
    # Le sabot n'est pas réinitialisé à chaque fois car cela est interdit aux
    # casinos pour permettre aux joueurs de compter les cartes
    if len(sabot) < 200:
        sabot = creation_sabot()

    # Première mise des joueurs
    mise()

    # Distribution des cartes
    distribution()

    # Black Jack
    black_jack()

    if croupier != []:

        # Boucle des joueurs
        for joueur in joueurs.keys():

            # Si ni le croupier, ni le joueur n'a fait Black Jack, le joueur, pour chacun de ses jeux, fait un seul choix:
                # Tirer
                # Abandonner
                # Doubler (uniquement possible si richesse >= mise)
                # split (uniquement possible si le joueur possède une paire et richesse >= mise)
                # Rester (pas de fonction associée au bouton car rien à faire)

            indice_main = 0
            while indice_main < len(joueurs[joueur]['mains']):

                if joueurs[joueur]['mains'][indice_main]['mise'] == 0:
                    pass

                else:
                    print('\n', 'Carte croupier:', croupier[0])
                    affichage(joueur)
                    action = choix_action(joueur, indice_main)

                    if action == 'tirer':
                        choix_tirer(joueur, indice_main)

                    elif action == 'abandonner':
                        abandonner(joueur, indice_main)

                    elif action == 'doubler':
                        doubler(joueur, indice_main)

                    elif action == 'split':
                        split(joueur)

                indice_main += 1

        # s'il reste des joueurs en lice:
        if [joueur for joueur in joueurs.keys() if mise_totale(joueurs[joueur]['mains']) != 0] != []:

            # Le croupier tire ses cartes et perd s'il a plus de 21
            tour_croupier()

            # Boucle des résultats:
            resultats()

    # les joueurs à richesse nulle sont éliminés de la partie
    eliminations()

    if joueurs == {}:
        print('\n', "Tous les joueurs sont éliminés, la partie est terminée")
        break

    continuer = choix('Voulez-vous continuer? Répondez "oui" ou "non": ', ['oui', 'non'])
    print()

initialisation_mains()
sauvegarde()
