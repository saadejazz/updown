## Steps to install and configure 

1. Clone the repository  
```
git clone https://github.com/saadejazz/updown.git
```

2. Install python3, apache, and the requirements:  
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3.8 python3-pip python3-venv
sudo apt-get install apache2 libapache2-mod-wsgi-py3
python3 -m venv venv 
source venv/bin/activate
pip3 install -r requirements.txt
```

3. Initialize the db using:  
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Add a user by providing the email, password, and name in the ```generate_user.py``` file, then run:  
```
python generate_user.py
```

5. Move the project ```updown``` to the required directory:  
```
sudo mkdir -p /var/www/
sudo mv updown /var/www/ftor
```

6. Add the configuration in ```sites-available``` by:  
```
sudo nano /etc/apache2/sites-available/ftor.com.conf
``` 
Then paste the following configuration:  
```bash
<VirtualHost *:80>
        ServerName  ftor.com
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/ftor
 
        WSGIDaemonProcess ftor threads=5
        WSGIScriptAlias / /var/www/ftor/main.wsgi
        WSGIApplicationGroup %{GLOBAL}
        <Directory ftor>
             WSGIProcessGroup ftor
             WSGIApplicationGroup %{GLOBAL}
             Order deny,allow
             Allow from all
        </Directory>
 
        ErrorLog ${APACHE_LOG_DIR}/ftor-error.log
        CustomLog ${APACHE_LOG_DIR}/ftor-access.log combined
</VirtualHost>
```
Then enable the new configuration:  
```
sudo a2ensite ftor.com
```
Finally, give permissions to directories that need it  
```
sudo mkdir /uploads
sudo chown -R www-data:www-data /uploads
sudo chown -R www-data:www-data /var/www/ftor
sudo chmod 756 /var/www/ftor/instance/db.sqlite
```

Restart the apache2 service:  
```
sudo systemctl reload apache2
```

7. Install tor and key generation tools using:  
```
sudo apt-get install tor openssl basez
```

8. Add/uncomment the following configuration in torrc 
```
HiddenServiceDir /var/lib/tor/ftor/
HiddenServicePort 80 127.0.0.1:80
```

9. Restart the tor service 
```
sudo systemctl reload tor
```

10. Get the generated hostname from the file  
 ```
sudo cat /var/lib/tor/ftor/hostname
```

11. Generate the keys and copy the public key for the next step
```
openssl genpkey -algorithm x25519 -out /tmp/k1.prv.pem
cat /tmp/k1.prv.pem | grep -v " PRIVATE KEY" | base64pem -d | tail --bytes=32 | base32 | sed 's/=//g' > /tmp/k1.prv.key
openssl pkey -in /tmp/k1.prv.pem -pubout | grep -v " PUBLIC KEY" | base64pem -d | tail --bytes=32 | base32 | sed 's/=//g' > /tmp/k1.pub.key
cat /tmp/k1.pub.key
```

12. Create an authorized client by pasting ```descriptor:x25519:<pub-key>``` into ```/var/lib/tor/ftor/authorized_clients/john.auth```, and then restart the tor service - wait for it to reload:  
```
sudo systemctl reload tor
```

13. The password to the onion site can be copied:  
```
cat /tmp/k1.prv.key
```
