#flaskapp.wsgi
import sys
sys.path.insert(0, '/var/www/html/ftor')
 
from app import app as application