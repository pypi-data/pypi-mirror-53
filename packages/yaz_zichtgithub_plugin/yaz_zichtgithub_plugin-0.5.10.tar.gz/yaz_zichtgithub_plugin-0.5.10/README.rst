=======================
A github plugin for YAZ
=======================

This YAZ plugin provides three tools:

**yaz-zicht-dependency-matrix**: this tool connects to https://github.com/zicht
and uses the composer.lock and package-lock.json files to determine the dependencies
that a project has.  These dependencies are then stored in the associated google sheet
document.

**yaz-zicht-github-finder**: this tool connects to https://github.com/zicht
and allows a regexp search on a given file in all available repositories.

**yaz-zicht-deployed-version**: this tool connects to https://github.com/zicht
and scans for deployment tags with patterns `FLAVOR_ENVIRONMENT-env` where
`FLAVOR_` is optional and `ENVIRONMENT` is either testing, staging, or production.
The corresponding version tags (`1.2.3` or `1.2.3-DISTANCE-HASH`) are then stored in
the associated google sheet document.

**yaz-zicht-repository-list**: this tool connects to https://github.com/zicht
and uses the repository descriptions to determine if the repo represents a library,
website, utility, or is obsolete.  It when scans the readme file to performs some checks.
The results are stored in the associated google sheet document.

Installing
----------

    .. code-block:: bash

        # Install or upgrade from the main repository
        pip3 install --upgrade yaz_zichtgithub_plugin

        # Configure ~/.yaz/yaz_extension/__init__.py to include Github.token,
        # and settings for DependencyMatrix and RepositoryList (these contain
        # personal information and will not be included here)

        # Call one of the installed scripts
        yaz-zicht-dependency-matrix

        # Or
        yaz-zicht-deployed-version

        # Or
        yaz-zicht-github-finder

        # Or
        yaz-zicht-repository-list


Configuration
-------------

You will need to provide an access token for authentication with github, as
well as a key file to access the various google sheets.  These must be configured
in the ~/.yaz/yaz_extension/__init__.py file as so:

    .. code-block:: python

        import yaz

        class Github(yaz.CustomPlugin):
            token = "GITHUB-TOKEN"

        class DependencyMatrix(yaz.CustomPlugin):
            json_key_file = "~/.yaz/dependency-matrix-key-file.json"
            sheet_key = "1vEAqgWz4DROS09r1mnODoxbaybOIlBpc2m9wSN98gf0"

        class DeployedVersion(yaz.CustomPlugin):
            json_key_file = "~/.yaz/deployed-version-key-file.json"
            sheet_key = "1pOZ0_Hm904XXvcRj4b7nU8H6cRKxmcJxLgGVVlYogFc"

        class RepositoryList(yaz.CustomPlugin):
            json_key_file = "~/.yaz/repository-list-key-file.json"
            sheet_key = "1M6qFEy_i6M_QqGRG1Y4nx3TTv2EU-nGHeyukBXSi8o8"

The referenced key-file.json files contain the private keys obtained through google
that allow access to the associated sheet_keys.  See:
https://console.developers.google.com/apis/dashboard?project=zicht-dependency-matrix&duration=PT1H


Developing
----------

    .. code-block:: bash

        # Get the code
        git clone git@github.com:boudewijn-zicht/yaz_zichtgithub_plugin.git
        cd yaz_zichtgithub_plugin

        # Ensure you have python 3.5 or higher and yaz installed
        python3 --version
        pip3 install --upgrade yaz

        # Setup your virtual environment
        virtualenv --python=python3 env
        source env/bin/activate
        python setup.py develop

        # Run one of the scripts
        ./bin/yaz-zicht-github-finder search boudewijn --verbose

        # Upload a new release to pypi
        python setup.py tag
        python setup.py publish

        # Once you are done... exit your virtual environment
        deactivate


Maintainer
----------

- Boudewijn Schoon <boudewijn@zicht.nl>
