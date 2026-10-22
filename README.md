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
- Ouvrir `.env` et renseigner les variables :
  - `SECRET_KEY` : une clé secrète propre à votre installation. Pour en générer une :
    `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
    puis coller le résultat entre apostrophes : `SECRET_KEY='...'`.
  - `SENTRY_DSN` : l'adresse du projet Sentry (voir la section « Surveillance et logs avec Sentry »).
  - `DEBUG` : `True` pour le développement local (déjà présent dans `.env.example`). Sans cette variable, `DEBUG` vaut `False` (mode production) et `runserver` ne sert plus les fichiers statiques : le site s'affiche sans mise en forme.
  - `ALLOWED_HOSTS` : facultatif en local, `localhost,127.0.0.1` par défaut (voir la section « Déploiement » pour la production).
- Sans `SECRET_KEY`, Django refuse de démarrer, y compris pour lancer `pytest`.
- Sans `SENTRY_DSN`, le site fonctionne normalement : l'envoi vers Sentry est simplement désactivé.
- Ne jamais commiter le fichier `.env`.

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- Vérifier que le fichier `.env` existe (voir la section précédente)
- `python manage.py migrate` (le repository contient la base d'origine : cette commande crée les tables des applications `lettings` et `profiles` et y copie les données. À relancer après chaque nouvelle migration)
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

## Déploiement

Le site est déployé automatiquement sur [Render](https://render.com) à chaque modification de la branche `master`, par un pipeline GitHub Actions qui passe par une image Docker publiée sur Docker Hub. Site en production : https://pyocp13.onrender.com

### Fonctionnement

```
git push sur master  ->  GitHub Actions  ->  Docker Hub  ->  Render
                         (tests, build)     (image)         (site en ligne)
```

Le pipeline est défini dans `.github/workflows/ci.yml`. Il contient trois jobs :

| Job | Rôle | Quand |
|---|---|---|
| `build-and-test` | Installe Python 3.11 et les dépendances, lance `flake8`, puis `pytest` avec la couverture (échec sous 80 %) | Sur toutes les branches et les pull requests |
| `containerize` | Construit l'image Docker à partir du `Dockerfile` et la publie sur Docker Hub | Sur `master` seulement, et seulement si `build-and-test` a réussi |
| `deploy` | Demande à Render de déployer l'image qui vient d'être publiée | Sur `master` seulement, et seulement si `containerize` a réussi |

- L'image est publiée avec deux étiquettes (*tags*) : le hash du commit (`<utilisateur>/oc-lettings:<hash>`) et `latest`. Le job `deploy` déploie l'étiquette du hash, donc exactement l'image construite à partir du commit qui vient d'être fusionné.
- Si les tests échouent, aucune image n'est publiée et rien n'est déployé.
- Le `Dockerfile` part de `python:3.11-slim`, installe `requirements.txt`, copie le code et exécute `collectstatic` pour rassembler les fichiers statiques. Ils sont servis par [WhiteNoise](https://whitenoise.readthedocs.io), sans serveur supplémentaire, y compris ceux de l'interface d'administration.
- Au démarrage de chaque conteneur, le script `entrypoint.sh` (déclaré par `ENTRYPOINT` dans le `Dockerfile`) s'arrête à la première erreur, applique les migrations (`migrate`), relance `collectstatic`, puis lance le site avec [Gunicorn](https://gunicorn.org) sur le port 8000. Le serveur applique donc lui-même les migrations à chaque déploiement : le repository contient la base d'origine, jamais une base déjà migrée sur un poste local.
- La version de Python du pipeline (3.11) doit rester identique à celle du `Dockerfile` et de l'environnement local : `flake8` 3.7.0 ne fonctionne pas avec Python 3.14.

### Configuration requise

**Comptes** : GitHub (ce repository), [Docker Hub](https://hub.docker.com) et [Render](https://render.com), tous trois gratuits.

**Secrets GitHub** (*Settings, Secrets and variables, Actions, New repository secret*) :

| Nom | Contenu |
|---|---|
| `DOCKERHUB_USERNAME` | Nom d'utilisateur Docker Hub |
| `DOCKERHUB_TOKEN` | Jeton d'accès Docker Hub avec les droits *Read & Write* (voir l'étape 1 ci-dessous) |
| `RENDER_DEPLOY_HOOK_URL` | URL du *Deploy Hook* du service Render (voir l'étape 3 ci-dessous) |

**Variables d'environnement Render** (onglet *Environment* du service) :

| Nom | Contenu |
|---|---|
| `SECRET_KEY` | Clé secrète de Django, propre à la production. Pour en générer une : `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` puis coller la valeur sans guillemets ni apostrophes |
| `ALLOWED_HOSTS` | Nom de domaine du site, par exemple `pyocp13.onrender.com` (plusieurs valeurs séparées par des virgules) |
| `SENTRY_DSN` | Facultatif : adresse du projet Sentry (voir la section « Surveillance et logs avec Sentry ») |

Ne pas définir `DEBUG` en production : sa valeur par défaut est `False`. En local, `DEBUG=True` se règle dans le fichier `.env`.

Aucune de ces valeurs ne doit être écrite dans le code ni dans le repository.

### Mise en place initiale

À faire une seule fois.

1. **Docker Hub** : *Account settings, Personal access tokens, Generate new token*, avec les droits *Read & Write*. Copier le jeton immédiatement, il n'est affiché qu'une fois. Le coller dans le secret GitHub `DOCKERHUB_TOKEN`, et renseigner `DOCKERHUB_USERNAME`.
2. **Première image** : fusionner une pull request dans `master` (voir « Déployer une modification »). Le job `containerize` crée le dépôt `oc-lettings` sur Docker Hub. Il est public, donc Render peut le récupérer sans identifiants.
3. **Render** : *New, Web Service, Existing Image*.
   - Image URL : `docker.io/<utilisateur Docker Hub>/oc-lettings:latest`.
   - Instance : *Free*.
   - Variables d'environnement : `SECRET_KEY` et `ALLOWED_HOSTS` (voir ci-dessus).
   - Après la création, désactiver le déploiement automatique (*Auto-Deploy* sur *Off*) : le déploiement est piloté par le pipeline.
   - Dans *Settings, Deploy Hook*, copier l'URL et la coller dans le secret GitHub `RENDER_DEPLOY_HOOK_URL`. Cette URL est secrète : quiconque la possède peut déclencher un déploiement. En cas de fuite, utiliser *Regenerate Hook* dans Render et mettre à jour le secret.

### Déployer une modification

1. Créer une branche, commiter, puis pousser : `git switch -c ma-branche`, `git push -u origin ma-branche`. Le job `build-and-test` s'exécute.
2. Ouvrir une pull request vers `master` **de ce repository**. Dans le formulaire, vérifier que la base (*base repository*) est bien ce repository et non le repository d'origine d'OpenClassrooms.
3. Quand `build-and-test` est vert, fusionner la pull request. Les jobs `containerize` puis `deploy` se lancent.
4. Vérifier le résultat :
   - onglet *Actions* de GitHub : les trois jobs sont verts ;
   - Render, onglet *Events* : un déploiement « Triggered via Deploy Hook » apparaît, puis « Deploy live » ;
   - ouvrir https://pyocp13.onrender.com et contrôler que le site et l'interface d'administration (`/admin`) s'affichent avec leur mise en forme.

### Lancer l'image en local

Aucun code ni environnement virtuel n'est nécessaire, seulement Docker :

```
docker run --rm -p 8000:8000 -e SECRET_KEY=une-valeur-quelconque hschbonus/oc-lettings:latest
```

Aller ensuite sur `http://localhost:8000`. Pour utiliser une version précise, remplacer `latest` par le hash du commit voulu.

### Points d'attention

- **Mise en veille** : sur l'offre gratuite de Render, le site s'endort après 15 minutes sans visite, et le réveil prend environ une minute. Ouvrir le site avant une démonstration.
- **Base de données** : la base SQLite (`oc-lettings-site.sqlite3`) est copiée dans l'image dans son état d'origine, puis migrée par `entrypoint.sh` à chaque démarrage du conteneur. Les modifications faites en production, par exemple depuis l'interface d'administration, sont perdues au déploiement suivant. Les données de démonstration sont restaurées à chaque déploiement. Avec une base persistante (PostgreSQL par exemple), seules les nouvelles migrations seraient appliquées.
- **Serveur** : le conteneur lance Gunicorn, un serveur d'application WSGI adapté à la production, et non `runserver`, le serveur de développement de Django.
- **Fichiers de l'image** : `.dockerignore` exclut `.env`, `venv`, `.git` et les documents du projet : aucun secret n'entre dans l'image.
- **Déploiement automatique de Render** : désactivé, car le service est piloté par le deploy hook. Un bouton *Manual Deploy* dans Render redéploie l'étiquette configurée dans le service, qui peut ne pas être la plus récente.
