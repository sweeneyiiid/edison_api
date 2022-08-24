# Vitalite SQL test plan

This folder contains the implementation of a class designed to test the translation of JSON in the SHS ESS API format into the MySQL data base records.

It contains pre-condition queries for DB, JSON payloads to insert, and post-condition queries.

See [ROCKS](https://rocks.reeep.org/display/NERD/SQL+Test+plan) page for note on logical setup.

*** NOTE: Execute payload creation from this directory, contains relative paths. ***

# Incorporation into automated testing

I am going to attempt to integrate these tests in the the automated testing conducted during the deployment process.

Based on work Saminu did in importing microgrid data, from `../test_microgrid.py`:

```
import unittest
import os
import base64
from app import application
from app.services.microgrid_service import MicroGridImport

"""
Pytest with  flask_restful: https://stackoverflow.com/questions/47042078/pytest-fails-to-import-module-installed-via-pip-and-containing-underscores/47099712#47099712
"""
```



