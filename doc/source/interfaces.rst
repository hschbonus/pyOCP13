Interfaces de programmation
===========================

Le site n'expose pas d'API de données (pas de JSON) : ses interfaces sont des routes
HTTP qui renvoient des pages HTML. Cette page décrit chaque route et la vue Django
qui la traite.

Routes du site
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - URL
     - Nom de la route
     - Vue
   * - ``/``
     - ``index``
     - ``oc_lettings_site.views.index`` : page d'accueil
   * - ``/lettings/``
     - ``lettings:lettings_index``
     - ``lettings.views.index`` : liste des locations
   * - ``/lettings/<id>/``
     - ``lettings:letting``
     - ``lettings.views.letting`` : détail d'une location
   * - ``/profiles/``
     - ``profiles:profiles_index``
     - ``profiles.views.index`` : liste des profils
   * - ``/profiles/<username>/``
     - ``profiles:profile``
     - ``profiles.views.profile`` : détail d'un profil
   * - ``/admin/``
     - (administration de Django)
     - Interface d'administration

Les routes des applications sont rattachées au site par ``include()`` dans
``oc_lettings_site/urls.py``. Chaque application déclare un espace de noms
(``app_name``), d'où les noms de route préfixés ``lettings:`` et ``profiles:``.

Vues
----

``lettings.views.index(request)``
   Affiche la liste de toutes les locations. Gabarit : ``lettings/index.html``.

``lettings.views.letting(request, letting_id)``
   Affiche le titre et l'adresse d'une location. ``letting_id`` est un entier pris
   dans l'URL. Gabarit : ``lettings/letting.html``. Si aucune location ne correspond,
   un avertissement est écrit dans les logs et la vue lève ``Http404``, ce qui
   affiche la page 404 personnalisée.

``profiles.views.index(request)``
   Affiche la liste de tous les profils. Gabarit : ``profiles/index.html``.

``profiles.views.profile(request, username)``
   Affiche le profil d'un utilisateur. ``username`` est le nom d'utilisateur pris
   dans l'URL. Gabarit : ``profiles/profile.html``. Si aucun profil ne correspond,
   le comportement est le même que pour une location inconnue (log et 404).

Pages d'erreur
--------------

- ``templates/404.html`` : page affichée pour une URL ou une ressource inconnue.
  Elle étend le gabarit de base du site.
- ``templates/500.html`` : page affichée en cas d'erreur du serveur. Elle est
  autonome (sans ``extends``, ``url`` ni ``static``), car elle s'affiche quand le
  système est déjà en échec.

Ces pages ne s'affichent que lorsque ``DEBUG`` vaut ``False`` ; en mode ``DEBUG``,
Django affiche à la place sa page technique d'erreur.

Journalisation et surveillance
------------------------------

Le module ``logging`` est configuré dans ``LOGGING`` (``settings.py``) : les
journaux des applications ``lettings`` et ``profiles`` sont écrits dans la console à
partir du niveau ``INFO``. Si la variable ``SENTRY_DSN`` est définie, le SDK Sentry
envoie les erreurs : les journaux de niveau ``ERROR`` et plus créent une *issue*
dans le projet Sentry, les niveaux ``INFO`` et plus servent de contexte.
