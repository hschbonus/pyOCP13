# Orange County Lettings

Projet 13 de la formation Python RNCP (OpenClassrooms) : refonte et outillage du site Orange County Lettings, fourni initialement par [OpenClassrooms-Student-Center/Python-OC-Lettings-FR](https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR).

## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Variables d'environnement

Les données sensibles (clé secrète de Django, clé Sentry) ne sont jamais écrites dans le code. Elles sont lues dans un fichier `.env` à la racine du projet, ignoré par git. Le fichier `.env.example` en est le modèle.

- `cd /path/to/Python-OC-Lettings-FR`
- `cp .env.example .env`
- Ouvrir `.env` et renseigner les deux variables :
  - `SECRET_KEY` : une clé secrète propre à votre installation. Pour en générer une :
    `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
    puis coller le résultat entre apostrophes : `SECRET_KEY='...'`.
  - `SENTRY_DSN` : l'adresse du projet Sentry (voir la section « Surveillance et logs avec Sentry »).
- Sans `SECRET_KEY`, Django refuse de démarrer, y compris pour lancer `pytest`.
- Sans `SENTRY_DSN`, le site fonctionne normalement : l'envoi vers Sentry est simplement désactivé.
- Ne jamais commiter le fichier `.env`.

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- Vérifier que le fichier `.env` existe (voir la section précédente)
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`
- Avec la couverture de test : `pytest --cov=. --cov-report=term-missing` (configuration dans `.coveragerc`, fichiers de tests et migrations exclus du calcul, rapport HTML avec `--cov-report=html`)
- Les tests désactivent Sentry (`conftest.py`) : ils n'envoient rien au projet Sentry.

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

#### Surveillance et logs avec Sentry

Les erreurs et les logs de l'application sont envoyés à [Sentry](https://sentry.io), un service de suivi d'erreurs.

**Mise en place**

1. Créer un compte Sentry, puis un projet avec la plateforme **Django**.
2. Récupérer le DSN du projet : *Settings, Client Keys (DSN)*.
3. Le coller dans le fichier `.env` : `SENTRY_DSN=<le DSN>`.
4. Installer les dépendances (`pip install --requirement requirements.txt` installe `sentry-sdk` et `python-dotenv`) et relancer le serveur.

**Fonctionnement**

- Le SDK est initialisé au début de `oc_lettings_site/settings.py` avec le DSN lu dans l'environnement.
- Le logging est configuré dans `LOGGING` (`settings.py`) : les loggers `lettings` et `profiles` écrivent dans la console à partir du niveau `INFO`, avec la date, le niveau et le nom du module.
- Selon la documentation de Sentry, les logs de niveau `INFO` et plus sont conservés comme contexte d'une erreur, et les logs de niveau `ERROR` et plus créent une issue.
- Les vues `lettings.views.letting` et `profiles.views.profile` écrivent un `warning` quand l'identifiant ou le nom demandé n'existe pas, puis renvoient une page 404.

**Vérifier que Sentry reçoit les erreurs**

1. Ajouter temporairement une vue qui écrit un `logger.error(...)` puis lève une exception (par exemple `1 / 0`), et une route qui y mène (voir le guide Django de la documentation Sentry).
2. Visiter cette route avec le serveur lancé.
3. Dans Sentry, ouvrir la liste **Issues** : l'erreur et le log doivent apparaître en quelques secondes.
4. Supprimer la vue et la route de test.

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Pour créer le fichier `.env`, `Copy-Item .env.example .env`
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`
