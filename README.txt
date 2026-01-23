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

Le gameplay repose sur l'alternance obligatoire entre trois modes de vision simulés via des palettes colorimétriques scientifiques.

| Touche | Mode Visuel | Altération Perception | Danger Masqué (Invisible) |
| :--- | :--- | :--- | :--- |
| **1** | **Deutéranopie** | Rouge/Vert confondus | Lave (Rouge) |
| **2** | **Tritanopie** | Bleu/Jaune confondus | Eau (Bleu) |
| **3** | **Achromatopsie** | Niveaux de gris | Boue (Orange) |

**Condition de défaite :** Si le joueur oublie de vérifier un filtre et entre en collision avec un obstacle invisible, la partie est immédiatement perdue.

---

## 3. Aperçu Visuel

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
