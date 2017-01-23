#!/usr/bin/env python
import os
import sys

__VERSION__ = '1.0.1'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings.dev.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
