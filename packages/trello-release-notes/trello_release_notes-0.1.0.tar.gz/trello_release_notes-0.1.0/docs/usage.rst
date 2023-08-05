=====
Usage
=====

Make sure that you've gotten an API key and a token or api-secret by following `the instructions on the Trello developers site <https://developers.trello.com/docs/api-introduction#section--a-name-auth-authentication-and-authorization-a->`_. 

Copy your api-key and api-secret into a config in your home directory called `.trello_release_settings.ini`.

.. literalinclude:: ../sample_trello_release_settings.ini

Make sure to protect this file so only you can read it! If you're in a unix or linux environment::

    chmod g-rwx,o-rwx ~/.trello_release_settings.ini

Now you're ready to create a release! I do it every week, but you do what suits you. If you've pip installed this, you can run perform a release::

    trello-release

To get more advanced, explore the options listed in the help::

    trello-release --help

To use Trello Release Notes in a project::

    import trello_release_notes

