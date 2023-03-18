# TKINTER BLACKJACK
from tkinter import *


def start_solo_game():
    print("Partie en mode solo lancée!")


def start_multi_game():
    print("Partie en mode multijoueurs lancée!")


def start_game():

    fenetre = Tk()
    fenetre.title("BLACK JACK")
    # construction du tapis
    h, l = 600, 800
    tapis = Canvas(fenetre, width=l, height=h, background="#006400")
    tapis.pack()

    # cree un canvas pour afficher le texte de la question
    question_canvas = Canvas(fenetre, width=50, height=50)
    question_canvas.create_text(250, 25, text="Choisissez le mode de jeu")
    question_canvas.pack()

    # crée deux boutons pour choisir le mode solo ou multijoueur(le mode multijoueur n'étant pas encore codé)
    solo_button = Button(fenetre, text="Solo", command=start_solo_game, width=50, height=30)

    multi_button = Button(fenetre, text="Multijoueur", command=start_multi_game, width=50, height=30)

    # place les boutons sous le canevas
    solo_button.grid(column=0, row=1, padx=10, pady=10)
    multi_button.grid(column=1, row=1, padx=10, pady=10)

    fenetre.mainloop()


# lance la fonction pour commencer la partie
start_game()
