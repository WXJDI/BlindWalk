# BLIND WALK
**"Voir l'invisible, survivre au handicap"**

> SYSTEM STATUS: COMPLETED
> PROJECT TYPE: SERIOUS GAME / ACCESSIBILITY
> AUTHOR: WAJDI BEN OUIRANE (BUT3 INFO)

---

## 1. Concept et Objectifs

Blind Walk est un projet de "Serious Game" développé dans un but de sensibilisation. Environ 300 millions de personnes dans le monde vivent avec une vision altérée. Ce projet vise à transformer ce handicap en une mécanique de jeu centrale et punitive.

Le joueur doit traverser un terrain miné d'obstacles, mais souffre de "Cécité Sélective". Il ne peut jamais percevoir la réalité dans son ensemble. Il doit constamment alterner entre différents filtres visuels pour construire une carte mentale du terrain et survivre.

---

## 2. Mécaniques de Jeu et Filtres

Le gameplay repose sur l'alternance obligatoire entre trois modes de vision (simulés via des palettes colorimétriques scientifiques). Chaque mode révèle certains dangers tout en masquant d'autres.

| Touche | Mode Visuel | Altération Perception | Danger Masqué (Invisible) |
| :--- | :--- | :--- | :--- |
| **1** | **Deutéranopie** | Rouge/Vert confondus | Lave (Rouge) |
| **2** | **Tritanopie** | Bleu/Jaune confondus | Eau (Bleu) |
| **3** | **Achromatopsie** | Niveaux de gris | Boue (Orange / Iso-luminant) |

**Condition de défaite :** Si le joueur oublie de vérifier un filtre et entre en collision avec un obstacle invisible, la partie est immédiatement perdue (Game Over).

---

## 3. Aperçu Visuel

Les captures d'écran ci-dessous illustrent l'interface et les différences de perception selon le filtre activé.

### Interface Principale
![Menu Principal](assets/captures/accueil.png)

### Simulation : Mode Deutéranopie
*Notez l'absence de distinction sur les obstacles rouges.*
![Gameplay Deuteranopie](assets/captures/1.png)

### Simulation : Mode Tritanopie
*Notez l'absence de distinction sur les obstacles bleus.*
![Gameplay Tritanopie](assets/captures/2.png)

### Simulation : Mode Achromatopsie
*Vision basée uniquement sur la luminosité.*
![Gameplay Achromatopsie](assets/captures/3.png)

---

## 4. Installation et Lancement

Ce projet nécessite Python 3.10 ou supérieur.

### Prérequis
* Python 3.x
* Bibliothèque Pygame

### Procédure d'installation
Ouvrez un terminal dans le dossier racine du projet et exécutez les commandes suivantes :

```bash
# 1. Installation des dépendances
pip install -r requirements.txt

# 2. Lancement du jeu
python main.py
5. Architecture Technique
Le projet est développé en Python suivant le paradigme de Programmation Orientée Objet (POO).

main.py : Point d'entrée du programme. Gère l'initialisation et la boucle principale.

settings.py : Contient les constantes globales et les dictionnaires de palettes colorimétriques (RGB).

classes/game.py : Moteur du jeu (Game Engine). Gère la machine à états (MENU, PLAYING, VICTORY) et la logique de rendu.

Logique de Rendu (Rendering Logic)
Le système de cécité n'utilise pas de simple filtre post-traitement (overlay), mais un rendu conditionnel strict.

La méthode draw() interroge l'état du filtre actif. Si un filtre correspond à la couleur d'un obstacle (ex: Deutéranopie et obstacle rouge), le moteur graphique ne dessine pas l'objet. L'objet existe physiquement (sa "hitbox" de collision est active), mais il est invisible pour le joueur, simulant ainsi la perte d'information visuelle réelle.

Python
# Extrait technique (Logique de rendu conditionnel)
if self.current_filter != 0:
    # Si le mode Deutéranopie n'est PAS actif, on dessine les obstacles rouges.
    # Sinon, ils ne sont pas rendus à l'écran.
    for trap in self.traps_a:
        pygame.draw.rect(self.screen, color, trap.rect)
6. Auteur
Wajdi Ben Ouirane BUT3 Informatique - Parcours Programmation Multimédia Université Sorbonne Paris Nord - IUT de Villetaneuse