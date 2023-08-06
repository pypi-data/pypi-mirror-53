zpov
====

.. image:: screenshot.png

A minimalist note engine
------------------------

* ~500 lines of code
* no javascript
* usable on any browser, including on mobile
* no database, just a bare git repo for storage and sync
* http basic auth
* pages are markdown files in the git repo. earch "directory" *must* have
  an ``index.md`` at the top
* title of each page is the top line of the markdown file
* sub-pages are sorted alphabetically
* edition is a text area containing the markdown

Usage
-----

``zpov`` is a python application built using ``flask``. refer to the flask
documentation to learn about developement and/or debugging.

``zpov`` needs a git repository and a configuration file to work. If public access is
not wanted, users and passwords must be stored in the configuration file too.

To ease up installation, a ``zpov-admin`` CLI is provided in the ``zpov`` package:

.. code-block:: console

    zpov-admin init [--public-access ] /path/to/empty/directory
    zpov-admin add-user --login LOGIN --name NAME --email EMAIL --password PASSWORD

