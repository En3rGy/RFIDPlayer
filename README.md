# RFIDPlayer
Python &amp; Raspebrry Pi base player for SONOS triggered by RFID-Chips

## Inbetriebnahme RPi
### GPIO Boot-Verhalten konfigurieren:
- Auf SD-Karte, Datei config.txt editieren
- GPIO an Pin 5(=GPIO3)  auf high:  
`# Set GPIO3 to be an output set to 1` 
`gpio=3=op,dh`

### WLAN einrichten
- Aus SD-Karte, Datei wpa_supplicant.conf erstellen:  
`country=DE`  
`ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev`  
`update_config=1`  
`network={`  
`   ssid="YOURSSID"`  
`   scan_ssid=1`  
`   psk="YOURPASSWORD"`  
`   key_mgmt=WPA-PSK`  
`}`

### SSH aktivieren
- Auf SD-Karten, neue Datei ssh anlegen (leer, ohne Endung)

## System einrichten

### RFID einrichten

- Ausführen  
`sudo apt-get install python3-pip python3-dev build-essential`  
`sudo pip install RPi.GPIO`  
- Config.txt bearbeiten:  
`sudo nano /boot/config.txt`  
Folgendes ergänzen:  
`dtparam=spi=on`
- Neustarten  
`sudo reboot`
- Bibliothek laden  
`sudo apt-get install git --yes`  
`git clone https://github.com/lthiery/SPI-Py.git`  
`cd SPI-Py`  
`sudo python3 setup.py install`   
`cd ..`  
`git clone https://github.com/pimylifeup/MFRC522-python.git && cd MFRC522-python`  
`sudo python3 setup.py install`  
- `sudo adduser pi spi`

### lighttpd
- Installieren:  
`sudo apt-get update`  
`sudo apt-get upgrade`  
`sudo apt-get install lighttpd`  
`sudo apt-get install php-common php-cgi php`  
`sudo lighty-enable-mod fastcgi`  
`sudo lighty-enable-mod fastcgi-php`  
`sudo service lighttpd force-reload`  
- Dateien nach /var/www/html kopieren
- Benutzer pi zur Gruppe www-data hinzufügen  
`sudo usermod -aG www-data pi`
- Rechte für config-Datei setzen (www-data)  
`sudo chown www-data:www-data /var/www/html/*`

### Python soco 
- Soco installieren  
`sudo pip3 install soco`

## SW installieren

### Dateien kopieren

### Autostart
- Datei /etc/rc.local bearbeiten:  
`sudo nano /etc/rc.local`
- *Markierten* Eintrag ergänzen:  
`_IP=$(hostname -I) || true`  
`if [ "$_IP" ]; then`  
`printf "My IP address is %s\n" "$_IP"` 
`fi`  
*`sudo python3 /home/pi/rfidPlayer.py &`*  
`exit 0`
- Datei ausführbar machen  
`sudo chmod +x /etc/rc.local`

