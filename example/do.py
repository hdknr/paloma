#!/usr/bin/env python
# this filed creaed by do.py command of "djado"
# https://github.com/hdknr/djado

# 1j $ pip install -e git+https://github.com/hdknr/djado.git#egg=djado
# 2) $ do.py /path/to/manage.py

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

    from django.core.management import execute_from_command_line

    from django.conf import settings
    settings.INSTALLED_APPS = settings.INSTALLED_APPS + (
        'djado',
        'django_extensions',
    )
    execute_from_command_line(sys.argv)
