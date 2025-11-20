# btp-projet-container
# 🎵 InfraMusicStore

API REST pour la gestion d'un disquaire en ligne, basée sur la base de données Chinook.
Ce projet a été réalisé dans le cadre du Bachelor BTP (Bloc DevOps & Conteneurisation).

L'application est entièrement conteneurisée via Docker et dispose d'un pipeline CI/CD automatisé.

---

## 🏗️ Architecture du Projet

Le projet repose sur une architecture micro-services orchestrée par Docker Compose :

1.  **API Backend (`music_store_api`)** : Développée en **Python (Flask)**. Elle expose les endpoints REST.
2.  **Base de Données (`music_store_db`)** : Serveur **MariaDB** contenant le schéma Chinook.
3.  **Administration (`adminer`)** : Interface graphique web pour visualiser et manipuler la base de données.
4.  **Documentation** : Swagger UI intégré directement à l'API.

## 🚀 Installation et Démarrage

### Prérequis
* Docker Desktop installé et lancé.
* Git.

### 1. Cloner le projet
```bash
git clone [https://github.com/TON_PSEUDO/btp-projet-container.git](https://github.com/TON_PSEUDO/btp-projet-container.git)
cd btp-projet-container

# 🎵 InfraMusicStore

API REST pour la gestion d'un disquaire en ligne, basée sur la base de données Chinook.
Ce projet a été réalisé dans le cadre du Bachelor BTP (Bloc DevOps & Conteneurisation).

L'application est entièrement conteneurisée via Docker et dispose d'un pipeline CI/CD automatisé.

---

##Architecture du Projet

Le projet repose sur une architecture micro-services orchestrée par Docker Compose :

1.  **API Backend (`music_store_api`)** : Développée en **Python (Flask)**. Elle expose les endpoints REST.
2.  **Base de Données (`music_store_db`)** : Serveur **MariaDB** contenant le schéma Chinook.
3.  **Administration (`adminer`)** : Interface graphique web pour visualiser et manipuler la base de données.
4.  **Documentation** : Swagger UI intégré directement à l'API.

## 🚀 Installation et Démarrage

### Prérequis
* Docker Desktop installé et lancé.
* Git.

### 1. Cloner le projet
```bash
git clone [https://github.com/TON_PSEUDO/btp-projet-container.git](https://github.com/TON_PSEUDO/btp-projet-container.git)
cd btp-projet-container

3. Lancer l'application
Utilisez Docker Compose pour construire et lancer les conteneurs en arrière-plan :

Bash

docker compose up --build -d

Accès aux ServicesUne fois les conteneurs lancés, voici les URLs pour accéder aux différents services :ServiceURLDescriptionDocumentation APIhttp://localhost:5000/docsInterface Swagger interactive pour tester l'APIAPI (JSON)http://localhost:5000/api/artistsExemple de route (Liste des artistes)Adminer (BDD)http://localhost:8080Gestionnaire de base de donnéesIdentifiants Adminer :Système : MySQLServeur : dbUtilisateur : userMot de passe : passwordBase de données : chinook

Commandes Docker Utiles
Voici quelques commandes pour gérer le projet au quotidien :

Arrêter les services :

Bash

docker compose down

Voir les logs (pour le débogage) :

Bash

docker compose logs -f
Vérifier l'état des conteneurs :

Bash

docker ps
Nettoyer tout (conteneurs et volumes) :

Bash

docker compose down -v
✅ Fonctionnalités
API REST (CRUD)
L'API permet d'effectuer les opérations suivantes sur les ressources (Artistes, Pistes, Albums...) :

GET : Récupération des listes ou d'un élément par ID.

POST : Création d'une nouvelle entrée.

PUT/PATCH : Modification d'une entrée existante.

DELETE : Suppression d'une entrée.

Automatisation (CI/CD)
Un pipeline GitHub Actions est configuré (.github/workflows/main.yml). À chaque push ou pull_request sur la branche main, il effectue automatiquement :

L'installation de l'environnement Python.

L'installation des dépendances (requirements.txt).

L'analyse du code (Linting) pour vérifier la qualité.

👤 Auteur
Projet réalisé par Dina Zeddam.
