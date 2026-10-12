Guide d'utilisation
===================

Ce guide présente les principaux usages du site, avec l'adresse locale
http://localhost:8000 (ou https://pyocp13.onrender.com pour la version en ligne).

Cas d'usage 1 : consulter les locations
---------------------------------------

1. Ouvrir la page d'accueil, puis le lien vers les locations (``/lettings/``).
2. La liste affiche le titre de chaque bien.
3. Cliquer sur un titre : la page de détail (``/lettings/<id>/``) affiche le titre
   et l'adresse du bien.

Cas d'usage 2 : consulter un profil
-----------------------------------

1. Depuis la page d'accueil, ouvrir la liste des profils (``/profiles/``).
2. Cliquer sur un nom d'utilisateur : la page ``/profiles/<nom>/`` affiche le profil,
   dont la ville préférée.

Cas d'usage 3 : gérer les données depuis l'administration
---------------------------------------------------------

1. Aller sur ``/admin/`` et se connecter avec un compte administrateur.
2. Les sections *Addresses*, *Lettings*, *Profiles* et *Users* permettent d'ajouter,
   modifier ou supprimer des enregistrements.
3. Les modifications sont visibles immédiatement sur le site public.

Un compte administrateur se crée avec la commande ``python manage.py createsuperuser``
en local.

.. note::

   En production, la base SQLite est copiée dans l'image Docker : les modifications
   faites depuis l'administration en ligne sont perdues au déploiement suivant
   (voir :doc:`deploiement`).

Cas d'usage 4 : page introuvable
--------------------------------

Une URL qui n'existe pas, ou un identifiant de location ou un nom de profil inconnu,
affiche la page 404 personnalisée. L'événement est consigné dans les logs.
