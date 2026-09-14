# Pipeline CI - SunuSanté

Nom / Groupe : Khardiata Ndiaye / Groupe 4

## 1. Le workflow d'intégration continue (chapitre 4, partie 1)

Le cours décrit 6 étapes, du commit au feedback. Remplissez la colonne de
droite avec le nom exact du stage Jenkins qui correspond, tel qu'il
apparaît dans votre `Jenkinsfile` et dans la Stage View de Jenkins.

| Étape du cours | Stage Jenkins correspondant |
|---|---|
| 1. Commit & push | *(se passe avant Jenkins, sur ma machine : `git commit` + `git push` vers GitHub)* |
| 2. Notification (Jenkins est prévenu) | Declarative: Checkout SCM / Récupération du code |
| 3. Build | Build |
| 4. Feedback build | Résultat affiché dans la Stage View (vert/rouge) juste après le stage Build |
| 5. Tests automatiques | Tests |
| 6. Feedback tests | Résultat affiché dans la Stage View (vert/rouge) juste après le stage Tests, complété par le message dans Post Actions ("Pipeline vert : build, lint, tests et sécurité tous OK.") |

Comment Jenkins est-il informé qu'un nouveau commit existe, dans votre
configuration (polling SCM, webhook, déclenchement manuel) ?

**Déclenchement manuel** : dans ma configuration, je clique moi-même sur
**Build Now** après chaque `git push`. Je n'ai pas mis en place de webhook
GitHub (cela demanderait d'exposer mon Jenkins local, installé nativement
sur Windows, à Internet) ni de polling SCM (vérification périodique du
dépôt). Dans un contexte professionnel avec Jenkins hébergé sur un serveur
accessible, un webhook GitHub serait préférable : le build se lancerait
automatiquement à chaque `push`, sans action manuelle, ce qui correspond
mieux à l'esprit du feedback "en quelques minutes" du cours.

## 2. Les prérequis d'une bonne CI (chapitre 4, partie 3)

| Prérequis | Statut sur SunuSanté | Détail |
|---|---|---|
| Dépôt avec versioning | ✅ | Git, dépôt distant sur GitHub : `https://github.com/Saratou316/sunusante-tp4` |
| Standard de code vérifié | ✅ | flake8 (fichier de config `.flake8` à la racine), exécuté dans le stage "Standard de code (lint)" |
| Serveur d'intégration continue | ✅ | Jenkins installé nativement sur Windows (installeur `.msi`, tourne comme service Windows), agent `any` (les stages s'exécutent directement sur la machine hôte, avec Python 3.12 installé localement) |

## 3. Pourquoi Jenkins, ici (chapitre 4, partie 4)

Le cours compare GitLab CI/CD, Jenkins et GitHub Actions. Remplissez ce
comparatif avec vos propres mots, puis justifiez en 2-3 phrases pourquoi
Jenkins convient (ou pas) à ce projet précis.

| Outil | Avantage principal | Inconvénient principal |
|---|---|---|
| GitLab CI/CD | Intégré directement à GitLab (dépôt + CI au même endroit, config `.gitlab-ci.yml` simple) | Suppose que le code est hébergé sur GitLab ; moins pertinent si le dépôt est sur GitHub |
| Jenkins | Open source, très personnalisable (des centaines de plugins), s'installe où l'on veut (local, serveur perso, Docker) | Configuration plus lourde à maintenir soi-même (installation, plugins, mises à jour, sécurité) comparé à une solution intégrée |
| GitHub Actions | Intégré directement à GitHub, zéro serveur à gérer, déclenchement automatique natif sur push/PR | Moins de contrôle sur l'environnement d'exécution ; dépendant de GitHub et de ses quotas de minutes gratuites |

**Justification du choix pour SunuSanté :**

Pour ce TP, Jenkins a du sens pédagogiquement car il permet de comprendre
concrètement ce qu'un serveur CI fait "sous le capot" (agents, stages,
plugins, PATH système) plutôt que de dépendre d'une plateforme qui gère
tout automatiquement. En revanche, pour un vrai projet SunuSanté hébergé
sur GitHub comme le mien, **GitHub Actions serait plus pertinent en
pratique** : pas de serveur à maintenir, déclenchement automatique
natif sur chaque `push`, et une configuration qui vit directement dans le
dépôt (`.github/workflows/`).

## 4. CI, Continuous Delivery, déploiement continu

Sur les 3 périmètres vus en cours (CI : code source + tests + build ·
Continuous Delivery : + qualité + release manuelle · déploiement continu :
tout automatisé), lequel votre `Jenkinsfile` couvre-t-il aujourd'hui ?
Qu'est-ce qui manquerait pour passer au périmètre suivant ?

**Périmètre couvert :**

Le pipeline actuel couvre le périmètre **Intégration Continue (CI)** :
récupération du code source, build (vérification Django + collecte des
fichiers statiques), tests automatisés (18 tests : unitaires,
intégration, système, performance), et contrôle qualité (lint flake8,
SAST avec semgrep, SCA avec pip-audit). À chaque build, on sait
immédiatement si le code est fonctionnel et sain.

**Ce qui manquerait pour aller plus loin :**

Pour passer à la **Continuous Delivery**, il faudrait ajouter une étape
de packaging (par exemple construire une image Docker de l'application)
et un mécanisme de release contrôlée manuellement par une personne
(un bouton "Deploy" dans Jenkins, par exemple, après validation humaine
des résultats du pipeline).

Pour aller jusqu'au **déploiement continu**, il faudrait en plus
automatiser complètement la mise en production : un stage supplémentaire
qui déploierait automatiquement l'application sur le serveur cible dès
que le pipeline est vert, sans aucune intervention manuelle - ce qui
suppose aussi un environnement de production déjà en place (serveur,
base de données, nom de domaine), que ce TP n'a pas mis en œuvre.

## 5. Tests non fonctionnels hors scope

Le chapitre 4 liste aussi les tests capacitaires et de compatibilité,
absents de ce pipeline. Pourquoi, à l'échelle de ce TP, est-ce un choix
raisonnable plutôt qu'un oubli (indice : YAGNI, chapitre 2) ? Que
faudrait-il ajouter si SunuSanté grandissait réellement ?

À ce stade, SunuSanté est une application pédagogique avec une poignée
d'utilisateurs simulés et pas de trafic réel. Mettre en place des tests
capacitaires (charge, montée en charge avec des outils comme Locust ou
k6) ou de compatibilité (tester sur plusieurs navigateurs, résolutions,
systèmes d'exploitation) demanderait un investissement disproportionné
par rapport au risque actuel : c'est le principe **YAGNI** ("You Aren't
Gonna Need It") vu au chapitre 2 - on n'ajoute pas une capacité tant
qu'on n'a pas de preuve concrète qu'elle sera nécessaire.

Si SunuSanté grandissait réellement (vraie clinique, vrais patients,
plusieurs praticiens connectés en même temps), il faudrait alors ajouter :
- des **tests capacitaires** simulant plusieurs centaines d'utilisateurs
  simultanés sur le formulaire de prise de rendez-vous, pour vérifier que
  la base de données et le serveur tiennent la charge ;
- des **tests de compatibilité** sur les navigateurs et appareils
  réellement utilisés par le personnel médical et les patients (mobile
  compris, vu que beaucoup de patients consulteraient depuis leur
  téléphone).