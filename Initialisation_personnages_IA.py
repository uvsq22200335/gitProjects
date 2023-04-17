"""
Ce programme enregistre dans personnages_IA.json la stratégie suivi par une IA si celle-ci a
choisi de tirer car on ne sait pas coder de json.
Une fois personnages_IA.json.json créé, ce programme ne sert à rien mais est conservé au cas où
personnages_IA.json.json devait être altéré, auquel cas lancer ce programme permettrait de le re-générer.
"""
import json as js

# personnages_IA = {nom du personnage: risques pris par l'IA}
personnages_IA = {'René': 0.1,
                  'Gisèle': 0.05,
                  'Elisa': 0.06,
                  'Juliette': 0.07,
                  'Eloa': 0.08,
                  'Maïmouna': 0.08,
                  'Raphaël': 0.09,
                  'Roman': 0.1,
                  'Quentin': 0.11,
                  'Kévin': 0.12,
                  'Anne': 0.03,
                  'Félix': 0.14,
                  'Sylvie': 0.1,
                  'Antoine': 0.06}


personnages_IA_json = open('personnages_IA.json', 'w')
js.dump(personnages_IA, personnages_IA_json, sort_keys=True, indent=4)
personnages_IA_json.close()
