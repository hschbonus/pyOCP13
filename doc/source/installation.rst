Installation
============

Cette page décrit l'installation du projet pour le développement local.

Prérequis
---------

- un compte GitHub avec accès en lecture au dépôt ;
- Git ;
- Python 3.11. Les dépendances sont figées à des versions anciennes (Django 3.0,
  ``flake8`` 3.7.0) : Python 3.14 est incompatible avec elles.

Récupérer le code
-----------------

.. code-block:: bash

   git clone https://github.com/hschbonus/pyOCP13.git
   cd pyOCP13

Créer l'environnement virtuel
-----------------------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

Sous Windows (PowerShell), l'activation se fait avec ``.\venv\Scripts\Activate.ps1``.
Pour désactiver l'environnement : ``deactivate``.

Installer les dépendances
-------------------------

.. code-block:: bash

   pip install --requirement requirements.txt

Variables d'environnement
-------------------------

Les données sensibles ne sont jamais écrites dans le code. Elles sont lues dans un
fichier ``.env`` à la racine du projet, ignoré par git. Le fichier ``.env.example``
en est le modèle.

.. code-block:: bash

   cp .env.example .env

Sous Windows : ``Copy-Item .env.example .env``. Renseigner ensuite les variables :

``SECRET_KEY``
   Clé secrète de Django, propre à chaque installation. Pour en générer une :

   .. code-block:: bash

      python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

   Sans cette variable, Django refuse de démarrer, y compris pour lancer les tests.

``DEBUG``
   ``True`` pour le développement local (valeur présente dans ``.env.example``).
   Sans cette variable, le mode production est actif (``False``) et le serveur de
   développement ne sert plus les fichiers statiques.

``ALLOWED_HOSTS``
   Facultatif en local, ``localhost,127.0.0.1`` par défaut.

``SENTRY_DSN``
   Facultatif : adresse du projet Sentry. Sans elle, l'envoi vers Sentry est désactivé.

Le fichier ``.env`` ne doit jamais être commité.
