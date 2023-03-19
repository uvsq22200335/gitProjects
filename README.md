<h1 align="center"> Projet IN200 : Jeu du Black Jack </h1>
<p align="center">
Maïmouna BA
- Eloa 
-Roman
-Raphael </p>

<h2 align="center">
REGLES ET DEROULEMENT D’UNE PARTIE </h2>
  
  
<div>  
L’intérêt est ici de coder un jeu de Blackjack. On s’intéresse ici à une version simplifiée du jeu, ne comprenant pas l’existence de mises secondaires (« side bets », existantes dans plusieurs casinos).<br>
Le jeu se joue avec plusieurs paquets de 52 cartes, constituant ensemble une pioche. Comme on le sait, chaque paquet est divisé en 4 couleurs : pique, cœur, trèfle et carreau, avec 13 cartes par couleur, allant de 1 (l’as) à 10, suivi du valet, de la dame et du roi. <br>
L’objectif de la partie est simple : il faut s’approcher le plus possible de 21 points, sans dépasser. <br>
Ci-dessous, les valeurs numériques associées aux cartes : <br>
<ul>
  <li>De 2 à 9 : valeur nominale de la carte ;</li>
  <li>De 10 au roi (surnommées « bûche ») : 10 points ;</li>
  <li>As : 1 ou 11 points (au choix du joueur)</li>
</ul>
Une partie va opposer individuellement chaque joueur à la banque (représentée par le croupier). Nous choisissons dans notre projet de faire intervenir des joueurs virtuels (ordinateur), que l’utilisateur pourra affronter, en plus s’il le désire, du croupier (cf. Mode Multijoueur). <br>
</div>

<div>
Le croupier distribue deux cartes à chaque joueur, faces visibles. Il demande au premier joueur l’option qu’il désire choisir. Selon la situation : 

<ul>  
<li>Si le joueur a « blackjack », il est dans la situation où il reçoit dès le début du jeu un as et une bûche. Il est alors directement vainqueur du tour. Dans tout autre cas, le joueur reste en jeu. </li>
  <li>Sinon, il peut : </li>
<ul>
  <li> « hit » : demander une (ici) carte supplémentaire</li>	
  <li> "stand" : il s'arrête et conserve ses cartes jusqu'au dépouillement . </li>
  <li>« double down » : doubler sa mise, mais il ne recevra qu’une seule carte après cela, une troisième carte finale. </li>
  <li>« surrender » : le joueur abandonne, perd la moitié de sa mise. </li>
  </ul>
</ul>
  
 
Dès qu’un joueur fait plus de 21, on dit qu’il « brûle » (« burst ») et il perd sa mise. <br>
Quant au croupier, une fois tous les joueurs servis, il joue pour son compte selon une règle universelle : « la banque tire à 16, reste à 17 ». Ainsi, le croupier tire des cartes jusqu'à atteindre un nombre supérieur ou égal à 179 (cf. Service du Croupier)
</div>
 




