Technologies et langages
========================

Langages
--------

- **Python** 3.11 pour l'application et les tests ;
- **HTML** avec le moteur de gabarits de Django, **CSS** et **JavaScript** pour les
  pages (dossier ``static``) ;
- **reStructuredText** pour cette documentation ;
- **YAML** pour le pipeline GitHub Actions.

Application
-----------

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Outil
     - Version
     - Rôle
   * - Django
     - 3.0
     - Framework web de l'application
   * - SQLite
     - fichier ``oc-lettings-site.sqlite3``
     - Base de données
   * - WhiteNoise
     - 5.3.0
     - Service des fichiers statiques en production, y compris ceux de l'administration
   * - python-dotenv
     - 1.2.4
     - Lecture des variables d'environnement depuis le fichier ``.env``
   * - sentry-sdk
     - 2.71.0
     - Envoi des erreurs et des logs vers Sentry

Qualité du code
---------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Outil
     - Version
     - Rôle
   * - flake8
     - 3.7.0
     - Analyse du style et des erreurs (configuration dans ``setup.cfg``)
   * - pytest et pytest-django
     - pytest-django 3.9.0
     - Tests unitaires et d'intégration
   * - pytest-cov
     - 7.1.0
     - Mesure de la couverture de test

Déploiement
-----------

- **Docker** : image du site, construite à partir du ``Dockerfile``
  (base ``python:3.11-slim``) ;
- **GitHub Actions** : pipeline défini dans ``.github/workflows/ci.yml`` ;
- **Docker Hub** : registre où l'image est publiée ;
- **Render** : hébergeur qui exécute l'image.

Documentation
-------------

- **Sphinx** : génération de la documentation à partir des fichiers ``.rst`` ;
- **Read the Docs** : publication et mise à jour automatique de la documentation.
