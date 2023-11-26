import sys
import logging

sys.path.insert(0, '/var/www/ftor')
sys.path.insert(0, '/var/www/ftor/venv/lib/python3.8/site-packages/')

logging.basicConfig(stream = sys.stderr, level = logging.DEBUG)

from main import app as application