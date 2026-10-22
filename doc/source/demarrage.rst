Démarrage rapide
================

Une fois le projet installé (voir :doc:`installation`), le site se lance avec les
commandes suivantes, depuis la racine du projet, avec l'environnement virtuel activé :

.. code-block:: bash

   source venv/bin/activate
   python manage.py migrate
   python manage.py runserver

Le dépôt contient la base d'origine : ``migrate`` crée les tables des applications
``lettings`` et ``profiles`` et y copie les données. Ouvrir ensuite http://localhost:8000 dans un navigateur. La page d'accueil donne
accès à la liste des locations et à la liste des profils.

Vérifier la qualité du code
---------------------------

.. code-block:: bash

   flake8
   pytest

``flake8`` ne doit afficher aucune erreur. ``pytest`` lance la suite de tests
(20 tests) ; pour afficher la couverture :

.. code-block:: bash

   pytest --cov=. --cov-report=term-missing

La couverture doit rester supérieure à 80 %. Les fichiers de tests et les migrations
sont exclus du calcul (fichier ``.coveragerc``).

Lancer l'image Docker
---------------------

Une autre façon de démarrer le site, sans environnement Python, est d'utiliser
l'image publiée sur Docker Hub :

.. code-block:: bash

   docker run --rm -p 8000:8000 -e SECRET_KEY=une-valeur-quelconque hschbonus/oc-lettings:latest
