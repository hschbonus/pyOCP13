Description du projet
=====================

Orange County Lettings est un site web de location immobilière. Il présente une
liste de biens à louer (*lettings*) et une liste de profils d'utilisateurs, chacun
avec sa page de détail. Une interface d'administration permet de gérer les données.

Contexte
--------

Le projet est le dernier de la formation Python RNCP d'OpenClassrooms. Le point de
départ est un site existant, fourni par le dépôt
`OpenClassrooms-Student-Center/Python-OC-Lettings-FR
<https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR>`_,
qui a été amélioré en cinq étapes :

1. refonte de l'architecture en applications modulaires (``lettings`` et ``profiles``) ;
2. réduction de la dette technique (``flake8``, docstrings, pages d'erreur 404 et 500,
   tests avec une couverture supérieure à 80 %) ;
3. surveillance des erreurs et journalisation avec Sentry ;
4. pipeline d'intégration et de déploiement continus avec conteneurisation Docker ;
5. documentation technique, qui est la présente documentation.

Organisation du code
--------------------

Le projet Django ``oc_lettings_site`` contient la configuration et la page d'accueil.
Deux applications portent les fonctionnalités :

``lettings``
   Biens à louer et leurs adresses.

``profiles``
   Profils des utilisateurs.

Site en production
------------------

Le site est en ligne à l'adresse https://pyocp13.onrender.com. Il est hébergé sur
l'offre gratuite de Render, qui met le site en veille après 15 minutes sans visite :
le premier chargement peut prendre environ une minute.
