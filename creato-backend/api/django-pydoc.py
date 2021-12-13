import os
import django
import pydoc

# Prepare Django before executing pydoc command
# Change the value according to your django settings path
os.environ['DJANGO_SETTINGS_MODULE'] = 'apiServer.settings'
django.setup()

# Now executing pydoc
pydoc.cli()
