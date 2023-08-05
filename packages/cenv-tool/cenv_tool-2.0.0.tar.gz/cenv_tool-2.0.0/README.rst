
conda-env-manager: cenv
=======================


.. image:: https://github.com/skallfass/cenv_tool/blob/master/docs/_static/coverage.svg
   :target: https://github.com/skallfass/cenv_tool/blob/master/docs/_static/coverage.svg
   :alt: coverage


.. image:: https://badge.fury.io/py/cenv-tool.svg
   :target: https://pypi.python.org/pypi/cenv-tool/
   :alt: PyPI version fury.io


.. image:: https://img.shields.io/pypi/pyversions/cenv-tool.svg
   :target: https://pypi.python.org/pypi/cenv-tool/
   :alt: PyPI pyversions


.. image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://lbesson.mit-license.org/
   :alt: MIT license


.. image:: https://readthedocs.org/projects/cenv-tool/badge/?version=latest
   :target: https://cenv-tool.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://github.com/dephell/dephell/blob/master/assets/badge.svg
   :target: https://github.com/dephell/dephell
   :alt: Powered by DepHell


.. image:: https://github.com/skallfass/cenv_tool/blob/master/docs/img/logo.png
   :target: https://github.com/skallfass/cenv_tool/blob/master/docs/img/logo.png
   :alt: logo


Due to the redundant dependency information inside the ``meta.yaml`` (required
to create the conda-package) and the ``environment.yml`` (as definition file
for the conda-environment during development and for production), ``cenv``
(short form for ``conda-env-manager``\ ) was created to make the ``meta.yaml``
the only relevant file and to create and update conda-environment from the
definition inside this ``meta.yaml``.
The name of the conda-environment to create / update is defined in the section
``extra`` and the variable ``env_name`` inside the ``meta.yaml``.
The python version must be defined in ``extra`` inside the key ``python``.

The steps run by cenv:


* creation of a backup if the environment already exists followed by the
  removal of the previous environment.
* creation of the environment as defined in the ``meta.yaml``.
  If any failures occurred during creation and the backup was created, the
  command to reset the backup-version can be used.
* if enabled in the config file the environment.yml is exported after creation
  / update of the environment.

The usage of cenv reduces the conda commands to use to the following:


* ``conda activate ...`` to activate the environment
* ``conda deactivate`` to deactivate an environment
* ``conda info`` to show information about the currently activated environment
* ``conda search ...`` to search for availability of a package in the conda
  channels.
* ``conda remove -n ... --all`` to remove an environment
* ``cenv`` to create / update an environment


Documentation
-------------

For complete documentation see
`readthedocs <https://cenv-tool.readthedocs.io/en/latest/>`_.


Installation
------------

Install ``cenv`` using pip:

.. code-block:: bash

   pip install cenv_tool

Now run ``init_cenv`` to create the relevant config-files and add the
autoactivate- and autoupdate-shell-function to your ``.bashrc`` / ``.zshrc``.


autoactivate and autoupdate
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Per default these features are deactivated, even if added to your shell by
running ``init_cenv``.


autoactivate-feature
~~~~~~~~~~~~~~~~~~~~

The autoactivate-feature activates the conda-environment as named
``extra``\ -section in the meta.yaml located at ``conda-build/meta.yaml``\ , if the
environment exists.
To activate the autoactivate-features run:

.. code-block:: bash

   autoactivate_toggle


autoupdate-feature
~~~~~~~~~~~~~~~~~~

The autoupdate checks if the content of the meta.yaml changed.
The current state is stored as a md5sum in ``conda-build/meta.md5``.
If it changed the cenv-process is called.

For the autoupdate-feature run:

.. code-block:: bash

   autoupdate_toggle


Usage
-----

All steps required to create or update the projects conda environment are
run automatically running:

.. code-block:: bash

   cenv

**ATTENTION**\ :

..

      If you use cenv, each environment should only be created, updated and
      modified using ``cenv``\ !
      This means the commands ``conda install``\ , ``conda remove`` are not used
      anymore.
      Changes of the dependencies of the environment are defined inside the
      ``meta.yaml`` and are applied by using ``cenv``.

      This means:


   * new dependency required => add it in ``meta.yaml`` and run ``cenv``.
   * dependency not needed anymore => remove it from ``meta.yaml`` and run
     ``cenv``.
   * need of another version of dependency => change the version of dependency
     in ``meta.yaml`` and run ``cenv``.


The required information about the projects conda environment are extracted
from the meta.yaml.
This meta.yaml should be located inside the project folder at
``./conda-build/meta.yaml``.
The project-configuration is defined in the ``extra`` section of the
``meta.yaml``.
There you can define the name of the projects conda-environment at
``env_name``.
The python version has to be defined here at ``python``, too.
Also you can define requirements only needed during development but not to be
included into the resulting conda package.
These requirements have to be defined in the ``dev_requirements`` -section.

All other parts of the ``meta.yaml`` have to be defined as default.

A meta.yaml valid for cenv should look like the following:

.. code-block:: yaml

       {% set data = load_setup_py_data() %}

       package:
           name: "example_package"
           version: {{ data.get("version") }}

       source:
           path: ..

       build:
           build: {{ environ.get('GIT_DESCRIBE_NUMBER', 0) }}
           preserve_egg_dir: True
           script: python -m pip install --no-deps --ignore-installed .

       requirements:
           build:
             - python 3.6.8
             - pip
             - setuptools
           run:
             - python 3.6.8
             - attrs >=18.2
             - jinja2 >=2.10
             - ruamel.yaml >=0.15.23
             - six >=1.12.0
             - yaml >=0.1.7
             - marshmallow >=3.0.0rc1*

       test:
           imports:
               - example_package

       extra:
           env_name: example
           python: 3.6
           dev_requirements:
               - ipython >=7.2.0

**ATTENTION**\ :

..

      In the ``requirements-run-section`` the minimal version of each package
      has to be defined!
      The same is required for the ``dev_requirements``\ -section.
      Not defining a version will not create or update a conda-environment,
      because this is not the purpose of the conda-usage.
      The validity of the ``meta.yaml`` is checked in ``cenv`` using the
      ``marshmallow`` package.
      You can additionally add upper limits for the version like the following:
      ``- package >=0.1,<0.3``


If cenv is run the environment is created / updated from the definition inside
this ``meta.yaml``.
The creation of the backup of the previous environment ensures to undo changes
if any error occurs during recreation of the environment.

**ATTENTION**\ :

..

      ``cenv`` can only update the environment if it is not activated.
      So ensure the environment to be deactivated before running ``cenv``.


Per default exporting the conda environment definition into an environment.yml
is turned off.
If you want to turn this functionality on you need to modify your
``~/.config/cenv.yml`` as described in the configuration-part.

Example for the output of the ``cenv`` command:

On create:

.. code-block:: bash

   Creating cenv_dev
      ├── Create environment
      │   └── Created
      ├── write md5sum of meta.yaml
      │   └── updated
      └── Done

On update:

.. code-block:: bash

   Updating cenv_dev
      ├── Create backup
      │   └── Created
      ├── Remove existing env
      │   └── Removed
      ├── Create environment
      │   ├── Clear backup
      │   │   └── Cleared
      │   └── Created
      ├── write md5sum of meta.yaml
      │   └── updated
      └── Done


Development of cenv
-------------------


Develop cenv
^^^^^^^^^^^^

To create / update the dev environment to develop cenv run the pre-commit hooks
manually:

.. code-block:: bash

   pyenv local 3.7.3
   dephell venv shell --env=dev
   dephell deps install
   pre-commit run --all-files


Running tests
^^^^^^^^^^^^^

To create / update the test environment run:

.. code-block:: bash

   dephell venv shell --env=pytest
   dephell deps install


To run all tests run the following command:

.. code-block:: bash

   dephell project test --env=pytest


Updating the docs
^^^^^^^^^^^^^^^^^

To create / update the docs environment run:

.. code-block:: bash

   dephell venv shell --env=docs
   dephell deps install --env=docs


To create / update the docs first run the tests as described above.
Then run:

.. code-block:: bash

   dephell venv shell --env=docs
   sphinx-apidoc -f -o docs cenv_tool && sphinx-build -W docs docs/build
