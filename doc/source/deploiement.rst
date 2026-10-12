Déploiement et gestion
======================

Le site est déployé automatiquement sur `Render <https://render.com>`_ à chaque
modification de la branche ``master``, par un pipeline GitHub Actions qui passe par
une image Docker publiée sur Docker Hub.

.. code-block:: text

   git push sur master  ->  GitHub Actions  ->  Docker Hub  ->  Render
                            (tests, build)      (image)         (site en ligne)

Pipeline
--------

Le pipeline est défini dans ``.github/workflows/ci.yml``. Il comporte trois jobs :

.. list-table::
   :header-rows: 1
   :widths: 20 50 30

   * - Job
     - Rôle
     - Quand
   * - ``build-and-test``
     - Installe Python 3.11 et les dépendances, lance ``flake8``, puis ``pytest``
       avec la couverture (échec sous 80 %)
     - Toutes les branches et les pull requests
   * - ``containerize``
     - Construit l'image Docker et la publie sur Docker Hub
     - ``master`` seulement, si ``build-and-test`` a réussi
   * - ``deploy``
     - Demande à Render de déployer l'image qui vient d'être publiée
     - ``master`` seulement, si ``containerize`` a réussi

L'image est publiée avec deux étiquettes : le hash du commit
(``<utilisateur>/oc-lettings:<hash>``) et ``latest``. Le job ``deploy`` déploie
l'étiquette du hash, donc exactement l'image construite à partir du commit fusionné.
Si les tests échouent, aucune image n'est publiée et rien n'est déployé.

Configuration requise
---------------------

**Secrets GitHub** (*Settings, Secrets and variables, Actions*) :

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Nom
     - Contenu
   * - ``DOCKERHUB_USERNAME``
     - Nom d'utilisateur Docker Hub
   * - ``DOCKERHUB_TOKEN``
     - Jeton d'accès Docker Hub avec les droits *Read & Write*
   * - ``RENDER_DEPLOY_HOOK_URL``
     - URL du *Deploy Hook* du service Render (secrète)

**Variables d'environnement Render** (onglet *Environment* du service) :

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Nom
     - Contenu
   * - ``SECRET_KEY``
     - Clé secrète de Django, propre à la production
   * - ``ALLOWED_HOSTS``
     - Nom de domaine du site, par exemple ``pyocp13.onrender.com``
   * - ``SENTRY_DSN``
     - Facultatif : adresse du projet Sentry

``DEBUG`` ne doit pas être défini en production : sa valeur par défaut est ``False``.
Aucune de ces valeurs ne doit apparaître dans le code ni dans le dépôt.

Mise en place initiale
----------------------

À faire une seule fois :

1. **Docker Hub** : créer un jeton d'accès (*Account settings, Personal access
   tokens*) avec les droits *Read & Write* et le copier immédiatement ; le placer
   dans le secret ``DOCKERHUB_TOKEN``.
2. **Première image** : fusionner une pull request dans ``master``. Le job
   ``containerize`` crée le dépôt ``oc-lettings`` sur Docker Hub, public.
3. **Render** : créer un *Web Service* de type *Existing Image* avec l'image
   ``docker.io/<utilisateur>/oc-lettings:latest``, sur l'instance gratuite, puis
   renseigner ``SECRET_KEY`` et ``ALLOWED_HOSTS``. Désactiver le déploiement
   automatique (*Auto-Deploy* sur *Off*).
4. Copier l'URL du *Deploy Hook* (*Settings* du service) dans le secret
   ``RENDER_DEPLOY_HOOK_URL``.

Déployer une modification
-------------------------

1. Créer une branche, commiter, puis pousser. Le job ``build-and-test`` s'exécute.
2. Ouvrir une pull request vers ``master`` de ce dépôt (vérifier que le dépôt de base
   est bien celui-ci et non le dépôt d'origine d'OpenClassrooms).
3. Quand ``build-and-test`` est vert, fusionner : ``containerize`` puis ``deploy``
   se lancent.
4. Vérifier : les trois jobs sont verts dans l'onglet *Actions*, Render affiche un
   déploiement « Triggered via Deploy Hook » puis « Deploy live », et le site ainsi
   que ``/admin`` s'affichent avec leur mise en forme.

Fichiers statiques
------------------

Le ``Dockerfile`` exécute ``collectstatic`` à la construction de l'image. WhiteNoise,
déclaré dans les middlewares, sert ensuite ces fichiers sans serveur supplémentaire,
y compris ceux de l'interface d'administration.

Gestion et points d'attention
-----------------------------

- **Mise en veille** : sur l'offre gratuite de Render, le site s'endort après
  15 minutes sans visite et met environ une minute à se réveiller.
- **Base de données** : la base SQLite est copiée dans l'image. Les modifications
  faites en production sont perdues au déploiement suivant.
- **Serveur** : le conteneur lance ``runserver``, le serveur de développement de
  Django. Une charge réelle demanderait un serveur d'application adapté.
- **Surveillance** : si ``SENTRY_DSN`` est défini, les erreurs de production
  apparaissent dans la liste *Issues* du projet Sentry.
- **Déploiement automatique de Render** : désactivé, le service est piloté par le
  deploy hook. Le bouton *Manual Deploy* redéploie l'étiquette configurée dans le
  service, qui peut ne pas être la plus récente.
