from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

#Couleur de la fenêtre racine
root_color = "#2E7D32"
#Couleur jaune style casino
yellow_color = "#FDD835"
#Couleur rouge pourpre
pourpre = "#8B0000"
#Hauteur et largeur de la fenetre racine
hauteur = 800
largeur = 1200
#Hauteur et largeur des boutons 
hauteur_bouton = 10
largeur_bouton = 35


#CREATION DE LA FENETRE RACINE 
root = Tk()
root.title( "Jeu de Blackjack")
root.configure(height=hauteur, width=largeur, bg=root_color)


# fonction stand
def stand():
	global joueur_total, croupier_total, score_joueur, score_croupier
	# compter les scores totaux
	joueur_total = 0
	croupier_total = 0

	# compter le score total du croupier 
	for score in score_croupier:
		# Add up score
		croupier_total += score

	# boucler dans la boucle de score du joueur et modification
	for score in score_joueur:
		# ajouter le score
		joueur_total += score

	# desactiver les boutons 
	bouton_carte.config(state="disabled")
	bouton_stand.config(state="disabled")

	# logique du croupier 
	if croupier_total >= 17:
		# verification si bust
		if croupier_total > 21:
			# Bust
			messagebox.showinfo("Le joueur a gagné!!", f"Le joueur a gagné!  croupier: {croupier_total}  joueur: {joueur_total}")
		elif croupier_total == joueur_total:
			# Tie - ex aequo
			messagebox.showinfo("Tie!!", f"Vous êtes à ex-aequo!!  croupier: {croupier_total}  joueur: {joueur_total}")
		elif croupier_total > joueur_total:
			# croupier gagne
			messagebox.showinfo("Le croupier gagne!!", f"Le croupier gagne!  croupier: {croupier_total}  joueur: {joueur_total}")
		else:
			# Le joueur gagne!
			messagebox.showinfo("Le joueur gagne!!", f"Le joueur gagne!  croupier: {croupier_total}  joueur: {joueur_total}")
	else:
		# continue d'ajouter une carte au croupier 
		croupier_hit()
		# recalcule
		stand()


# test s'il y a blackjack lors du melange
def blackjack_shuffle(joueur):
	global joueur_total, croupier_total, score_joueur, score_croupier
	
	# compter les scores
	joueur_total = 0
	croupier_total = 0
	if joueur == "croupier":
		if len(score_croupier) == 2:
			if score_croupier[0] + score_croupier[1] == 21:
				# mettre a jour le statut
				statut_blackjack["croupier"] = "yes"
				

	if joueur == "joueur":
		if len(score_joueur) == 2:
			if score_joueur[0] + score_joueur[1] == 21:
				# mettre a jour le statut
				statut_blackjack["joueur"] = "yes"
		else:
			
			for score in score_joueur:
				# ajout des scores
				joueur_total += score

			if joueur_total == 21:
				statut_blackjack["joueur"] = "yes"
			
			elif joueur_total > 21:
				# souhait de convertir l'as en 1 ou 11? 
				for card_num, card in enumerate(score_joueur):
					if card == 11:
						score_joueur[card_num] = 1

						# effacer le total du joueur et recalcul
						joueur_total = 0
						for score in score_joueur:
							# ajout du score
							joueur_total += score
						
						# verification si au dessus de 21, donc si bust
						if joueur_total > 21:
							statut_blackjack["joueur"] = "bust"

				else:
					# verification des nouveaux totaux
					if joueur_total == 21:
						statut_blackjack["joueur"] = "yes"
					if joueur_total > 21:
						statut_blackjack["joueur"] = "bust"



	if len(score_croupier) == 2 and len(score_joueur) == 2:
		# verification s'il y a partie nulle
		if statut_blackjack["croupier"] == "yes" and statut_blackjack["joueur"] == "yes":
			# It's a push - tie
			messagebox.showinfo("Push!", "C'est un Tie!")
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")
		
		# victoire du croupier
		elif statut_blackjack["croupier"] == "yes":
			messagebox.showinfo("Le croupier gagne!", "Blackjack! Le croupier gagne!")
			# désactive les boutons 
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")

		# victoire du joueur 
		elif statut_blackjack["joueur"] == "yes":
			messagebox.showinfo("Le joueur gagne!", "Blackjack! Le joueur gagne!")
			# désactive les boutons 
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")
	#verification s'il y a blackjack pendant le jeu 
	else:
		# verification ex-aequo
		if statut_blackjack["croupier"] == "yes" and statut_blackjack["joueur"] == "yes":
			# ex-aequo
			messagebox.showinfo("Push!", "It's a Tie!")
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")
		
		# verification victoire du croupier
		elif statut_blackjack["croupier"] == "yes":
			messagebox.showinfo("Le croupier gagne!", "21! Le croupier gagne!")
			# désactiver les boutons 
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")

		# Check For joueur Win
		elif statut_blackjack["joueur"] == "yes":
			messagebox.showinfo("Le joueur gagne!", "21! Le joueur gagne!")
			# désactiver les boutons 
			bouton_carte.config(state="disabled")
			bouton_stand.config(state="disabled")

	# verification bust pour le joueur 
	if statut_blackjack["joueur"] == "bust":
		messagebox.showinfo("joueur Busts!", f"joueur Loses! {joueur_total}")
		# désactiver les boutons 
		bouton_carte.config(state="disabled")
		bouton_stand.config(state="disabled")

#REDIMENSIONNER LES CARTES
def redim_cartes(carte):
    #ouvrir l'image
    image_carte = Image.open(carte)

    #redimmensionner
    image_carte_redimmensionnee = image_carte.resize((150, 218))

    #affichage de la carte
    global img_carte
    img_carte = ImageTk.PhotoImage(image_carte_redimmensionnee)

    #retourner cette carte
    return img_carte

# Mélanger les cartes
def mélanger():
    # Mettre la situation à jour
    global statut_blackjack, joueur_total, croupier_total

    # Mettre à jour les scores
    joueur_total = 0
    croupier_total = 0

    statut_blackjack = {"croupier": "non", "joueur": "non"}

    # Activer les boutons
    bouton_carte.config(state="normal")
    bouton_stand.config(state="normal")

    # Enlever toutes les cartes d'une partie précédente
    croupier_label_1.config(image='')
    croupier_label_2.config(image='')
    croupier_label_3.config(image='')
    croupier_label_4.config(image='')
    croupier_label_5.config(image='')

    joueur_label_1.config(image='')
    joueur_label_2.config(image='')
    joueur_label_3.config(image='')
    joueur_label_4.config(image='')
    joueur_label_5.config(image='')

    # Créer un nouveau deck
    tetes = ["diamonds", "clubs", "hearts", "spades"]
    valeurs = range(2, 15)
    # 11 = Jack, 12=Queen, 13=King, 14 = Ace

    global deck
    deck = []


    for tete in tetes: 
        for valeur in valeurs:
            deck.append(f'{valeur}_of_{tete}')

    #creation des joueurs
    global croupier, joueur, spot_croupier, spot_joueur, score_croupier, score_joueur
    croupier = []
    joueur = []
    score_croupier = []
    score_joueur = []
    spot_croupier = 0
    spot_joueur = 0


    #mélanger et distribuer deux cartes pour le joueur et le crouppier
    croupier_hit()
    croupier_hit()
    joueur_hit()
    joueur_hit()

    #indiquer le nombre de cartes restantes dans la bar d'évolution
    root.title(f'Il reste {len(deck)} cartes')

def croupier_hit():
    global spot_croupier
    global joueur_total, croupier_total, score_joueur

    if spot_croupier <= 5:
        try:
            # récupérer la carte du joueur
            carte_croupier = random.choice(deck)

            # retirer la carte de la pioche
            deck.remove(carte_croupier)

            # ajouter la carte à la liste du croupier
            croupier.append(carte_croupier)

            # ajouter la carte au score du croupier et convertir
            dcard = int(carte_croupier.split("_", 1)[0])

            if dcard == 14:
                score_croupier.append(11)
            elif dcard == 11 or dcard == 12 or dcard == 13:
                score_croupier.append(10)
            else:
                score_croupier.append(dcard)

            # afficher la carte à l'écran
            global croupier_image1, croupier_image2, croupier_image3, croupier_image4, croupier_image5

            if spot_croupier == 0:
                # redimmensionner la carte
                croupier_image1 = redim_cartes(f'images/{carte_croupier}.png')
                # afficher la carte à l'écran
                croupier_label_1.config(image=croupier_image1)
                # ajouter 1 au compteur de notre joueur
                spot_croupier += 1
            elif spot_croupier == 1:
                # redimmensionner la carte
                croupier_image2 = redim_cartes(f'images/{carte_croupier}.png')
                # afficher la carte à l'écran
                croupier_label_2.config(image=croupier_image2)
                # ajouter 1 au compteur de notre joueur
                spot_croupier += 1
            elif spot_croupier == 2:
                # redimmensionner la carte
                croupier_image3 = redim_cartes(f'images/{carte_croupier}.png')
                # afficher la carte à l'écran
                croupier_label_3.config(image=croupier_image3)
                # ajouter 1 au compteur de notre joueur
                spot_croupier += 1
            elif spot_croupier == 3:
                # redimmensionner la carte
                croupier_image4 = redim_cartes(f'images/{carte_croupier}.png')
                # afficher la carte à l'écran
                croupier_label_4.config(image=croupier_image4)
                # ajouter 1 au compteur de notre joueur
                spot_croupier += 1
            elif spot_croupier == 4:
                # redimmensionner la carte
                croupier_image5 = redim_cartes(f'images/{carte_croupier}.png')
                # afficher la carte à l'écran
                croupier_label_5.config(image=croupier_image5)
                # ajouter 1 au compteur de notre joueur
                spot_croupier += 1

            # Vérifier si le croupier a dépassé 5 cartes
            joueur_total = 0
            croupier_total = 0

            # obtenir le score du joueur 
            for score in score_joueur:
                joueur_total += score

            # obtenir le score du joueur 
            for score in score_croupier:
                croupier_total += score

            # en dessous de 21?
            if croupier_total <= 21:
                # on gagne!!
                # désactiver les boutons
                bouton_carte.config(state="disabled")
                bouton_stand.config(state="disabled")

                #faire apparaitre le message box
                messagebox.showinfo("Le croupier gagne!!", f"Le croupier gagne! croupier:{croupier_total}   joueur: {joueur_total}")

            #indiquer le nombre de cartes restantes dans la bar d'évolution
            root.title(f'il reste {len(deck)} cartes')

        except:
            root.title(f'Plus de cartes dans la pioche')


def joueur_hit():
    global spot_joueur
    if spot_joueur < 5:
        try:
            # récupérer la carte du joueur
            carte_joueur = random.choice(deck)
            # retirer la carte de la pioche
            deck.remove(carte_joueur)
            # ajouter la carte à la liste du joueur
            joueur.append(carte_joueur)
            # afficher la carte à l'écran
            global joueur_image1, joueur_image2, joueur_image3, joueur_image4, joueur_image5

            if spot_joueur == 0:
                # redimmensionner la carte
                joueur_image1 = redim_cartes(f'images/{carte_joueur}.png')
                # afficher la carte à l'écran
                joueur_label_1.config(image=joueur_image1)
                #ajouter 1 au compteur de notre joueur
                spot_joueur += 1
            elif spot_joueur == 1:
                # redimmensionner la carte
                joueur_image2 = redim_cartes(f'images/{carte_joueur}.png')
                # afficher la carte à l'écran
                joueur_label_2.config(image=joueur_image2)
                #ajouter 1 au compteur de notre joueur
                spot_joueur += 1
            elif spot_joueur == 2:
                # redimmensionner la carte
                joueur_image3 = redim_cartes(f'images/{carte_joueur}.png')
                # afficher la carte à l'écran
                joueur_label_3.config(image=joueur_image3)
                #ajouter 1 au compteur de notre joueur
                spot_joueur += 1
            elif spot_joueur == 3:
                # redimmensionner la carte
                joueur_image4 = redim_cartes(f'images/{carte_joueur}.png')
                # afficher la carte à l'écran
                joueur_label_4.config(image=joueur_image4)
                #ajouter 1 au compteur de notre joueur
                spot_joueur += 1
            elif spot_joueur == 4:
                # redimmensionner la carte
                joueur_image5 = redim_cartes(f'images/{carte_joueur}.png')
                # afficher la carte à l'écran
                joueur_label_5.config(image=joueur_image5)
                #ajouter 1 au compteur de notre joueur
                spot_joueur += 1

            #indiquer le nombre de cartes restantes dans la bar d'évolution
            root.title(f'il reste {len(deck)} cartes')
	
        except:
            root.title(f'Plus de cartes dans la pioche')


#distribution des cartes
def distribuer_cartes():
    try:
        # récupérer la carte du croupier
        card = random.choice(deck)
        # retirer la carte de la pioche
        deck.remove(card)
        # ajouter la carte a la liste du croupier
        croupier.append(card)
        # affichage
        global croupier_image
        croupier_image = redim_cartes(f'images/{card}.png')
	
        croupier_label.config(image=croupier_image)
        #croupier_label.config(text=carte)

        # récupérer la carte du joueur
        card = random.choice(deck)
        # retirer la carte de la pioche
        deck.remove(card)
        # 
        joueur.append(card)
        # affichage
        global joueur_image
        joueur_image = redim_cartes(f'images/{card}.png')
	
        joueur_label.config(image=joueur_image)
        #joueur_label.config(text=card)

        #indiquer le nombre de cartes restantes dans la bar d'évolution
        root.title(f'il reste {len(deck)} cartes')
    except:
        root.title(f'Plus de cartes dans la pioche')

frame = Frame(root, bg="green")
frame.pack(pady=20)

# crée un cadre pour les cartes
frame_croupier = LabelFrame(frame, text="croupier", bd=0)
frame_croupier.pack(padx=20, ipadx=20)

joueur_frame = LabelFrame(frame, text="joueur", bd=0)
joueur_frame.pack(ipadx=20, pady=10)

# mets les cartes du croupier dans les cadres
croupier_label_1 = Label(frame_croupier, text='')
croupier_label_1.grid(row=0, column=0, pady=20, padx=20)

croupier_label_2 = Label(frame_croupier, text='')
croupier_label_2.grid(row=0, column=1, pady=20, padx=20)

croupier_label_3 = Label(frame_croupier, text='')
croupier_label_3.grid(row=0, column=2, pady=20, padx=20)

croupier_label_4 = Label(frame_croupier, text='')
croupier_label_4.grid(row=0, column=3, pady=20, padx=20)

croupier_label_5 = Label(frame_croupier, text='')
croupier_label_5.grid(row=0, column=4, pady=20, padx=20)

# mets les cartes du joueur dans les cadres
joueur_label_1 = Label(joueur_frame, text='')
joueur_label_1.grid(row=1, column=0, pady=20, padx=20)

joueur_label_2 = Label(joueur_frame, text='')
joueur_label_2.grid(row=1, column=1, pady=20, padx=20)

joueur_label_3 = Label(joueur_frame, text='')
joueur_label_3.grid(row=1, column=2, pady=20, padx=20)

joueur_label_4 = Label(joueur_frame, text='')
joueur_label_4.grid(row=1, column=3, pady=20, padx=20)

joueur_label_5 = Label(joueur_frame, text='')
joueur_label_5.grid(row=1, column=4, pady=20, padx=20)

# crée un bouton pour le cadre
button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

# Quelques boutons
shuffle_button = Button(button_frame, text="Mélanger la pioche", font=("Helvetica", 14), command=mélanger)
shuffle_button.grid(row=0, column=0)

bouton_carte = Button(button_frame, text="Hit!", font=("Helvetica", 14), command=joueur_hit)
bouton_carte.grid(row=0, column=1, padx=10)

bouton_stand = Button(button_frame, text="Stand!", font=("Helvetica", 14))
bouton_stand.grid(row=0, column=2)


#mélanger les cartes au commencement
mélanger()


root.mainloop()

