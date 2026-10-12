Base de données et modèles
==========================

Le site utilise une base SQLite, stockée dans le fichier ``oc-lettings-site.sqlite3``
à la racine du projet. Trois modèles Django portent les données, répartis sur deux
applications. Les tables de Django (utilisateurs, sessions, etc.) s'y ajoutent.

Application ``lettings``
------------------------

``Address``
~~~~~~~~~~~

Adresse postale d'un bien.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Champ
     - Type
     - Contrainte
   * - ``number``
     - entier positif
     - 9999 au maximum
   * - ``street``
     - texte
     - 64 caractères au maximum
   * - ``city``
     - texte
     - 64 caractères au maximum
   * - ``state``
     - texte
     - exactement 2 caractères
   * - ``zip_code``
     - entier positif
     - 99999 au maximum
   * - ``country_iso_code``
     - texte
     - exactement 3 caractères

Représentation textuelle : le numéro suivi du nom de rue. Dans l'administration,
le modèle s'affiche sous le nom « Address » (pluriel « Addresses »).

``Letting``
~~~~~~~~~~~

Bien disponible à la location.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Champ
     - Type
     - Contrainte
   * - ``title``
     - texte
     - 256 caractères au maximum
   * - ``address``
     - relation un-à-un vers ``Address``
     - suppression en cascade : supprimer l'adresse supprime la location

Représentation textuelle : le titre.

Application ``profiles``
------------------------

``Profile``
~~~~~~~~~~~

Informations complémentaires sur un utilisateur.

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - Champ
     - Type
     - Contrainte
   * - ``user``
     - relation un-à-un vers ``User`` (modèle d'authentification de Django)
     - suppression en cascade
   * - ``favorite_city``
     - texte
     - 64 caractères au maximum, peut être vide

Représentation textuelle : le nom d'utilisateur.

Relations
---------

.. code-block:: text

   Address  1 --- 1  Letting
   User     1 --- 1  Profile

Une adresse correspond à une seule location, et un utilisateur à un seul profil.

Migrations
----------

Les modèles ``Address``, ``Letting`` et ``Profile`` se trouvaient à l'origine dans
l'application ``oc_lettings_site``. Ils ont été déplacés vers ``lettings`` et
``profiles`` par des migrations Django qui copient les données existantes
(``RunPython``), puis les anciennes tables ont été supprimées. Les migrations sont
dans le dossier ``migrations`` de chaque application.
