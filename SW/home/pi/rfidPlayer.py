#!/usr/bin/env python

import RPi.GPIO as GPIO
import soco
from soco import SoCo
import sys
import time
import json
from threading import Thread

sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

#### definitions ###############################################

# storage for previously detected rfid tag
id_old = 0

GPIO.setmode(GPIO.BOARD)

pin_wifi = 7
pin_rfid = 12

t1 = 0
t2 = 0

GPIO.setup(pin_wifi, GPIO.OUT)
GPIO.setup(pin_rfid, GPIO.OUT)

GPIO.output(pin_wifi, GPIO.HIGH)
GPIO.output(pin_rfid, GPIO.LOW)

#### functions #################################################

def flash(pin, cont):
    log("Start flashing")
    GPIO.setmode(GPIO.BOARD)
    while(True):
        if not cont():
            break
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.5)
        if not cont():
            break
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.5)

    log("Stop flashing")

def log(msg):
    print(str(time.time()) + ": " + str(msg))

def sonosAvailable():
    sonos_available = False
    log("Waiting for SONOS")
    while not sonos_available:
        try:
            sonos_speakers =  soco.discover()
            if len(sonos_speakers) > 0:
                sonos_available = True
                log("SONOS available")
                return True

        except:
            pass

    return False


def writeSonosData():
    # get sonos data
    log("Getting SONOS data")
    try:
        # Speaker
        data = {}
        speakers = []
        sonos_speakers = soco.discover()
        for speaker in sonos_speakers:
            speaker_set = {"name" : speaker.player_name, "ip_address" : speaker.ip_address}
            speakers.append(speaker_set)
        data["speaker"]= speakers

        # Albums
        libSpeaker = SoCo(sonos_speakers.pop().ip_address)
        sonos_albums = libSpeaker.music_library.get_music_library_information("albums", 0, 100, False, None, None, True)

        albums=[]
        for album in sonos_albums:
            album_set = {"title" : album.title , "uri" : album.get_uri()}
            albums.append(album_set)

        data["albums"]= albums

        #write file
        with open("/var/www/html/sonos.json", 'w') as sonos_file:
            json.dump(data, sonos_file, indent=4)

    except Exception as e:
        log("Exception trying read SONOS data; " + str(e))

    log("SONOS data written to file.")

#### main #################################################

print("\n")
log("**** Starting Programm ****")
print(" ")
run = True
t1 = Thread(target=flash, args=(pin_wifi, lambda : run,))
t1.start()

sonosAvailable()
run = False
GPIO.output(pin_wifi, GPIO.HIGH)

t2 = Thread(target=writeSonosData())
t2.start()

# load config
with open('/var/www/html/rfid.json', 'r') as cfgfile:
    data = cfgfile.read()
    cfgObj = json.loads(data)

sonosIP = cfgObj["sonos_ip"]
tagTimeout = cfgObj["timeout"]
volume = cfgObj["volume"]

mySonos = SoCo(sonosIP)
reader = SimpleMFRC522()

log("Starting main loop")

try:
    while True:
        print(" ")
        log("Waiting for rfid")

        GPIO.output(pin_rfid, GPIO.LOW)

        # Wait for RFID and read it, measure time, it takes to read,
        # usually detection of rfid lying on the sensor takes < 1s.
        t1 = time.time()
        id = reader.read_id()
        t2 = time.time()
        log("**** Rfid detected ****")

        # Update cfg
        log("Updating config data")
        with open('/var/www/html/rfid.json', 'r') as cfgfile:
            data = cfgfile.read()

        rfids = cfgObj["rfid"]
        cfgObj = json.loads(data)
        volume = int(cfgObj["volume"])
        tagTimeout = int(cfgObj["timeout"])
        mySonos = SoCo(cfgObj["sonos_ip"])

        # check if same rfid is identified; accept only after $tagTimeout
        if t2 - t1 > tagTimeout:
            id_old = 0

        # new rfid detected?
        if id != id_old:
            id_old = id

            with open("/var/www/html/last_rfid.txt", "w") as file:
                file.write(str(id))

            if str(id) in rfids:
                GPIO.output(pin_rfid, GPIO.HIGH)

                log("RFID " + str(id) + ", requested album: " + rfids[str(id)]["album"].encode("utf8"))
                try:
                    albums = mySonos.music_library.get_albums(search_term = rfids[str(id)]["album"])
                    if albums is not None:
                        mySonos.unjoin()
                        mySonos.clear_queue()
                        mySonos.volume = volume
                        if rfids[str(id)]["random"]:
                            mySonos.play_mode = "SHUFFLE_NOREPEAT"
                        else:
                            mySonos.play_mode = "NORMAL"
                        mySonos.add_to_queue(albums[0])
                        mySonos.play_from_queue(0)
                        log("Playing")

                    else:
                        log("Album not found: " + rfids[str(id)])

                except Exception as e:
                    log("Exception trying to play; " + str(e))

            else:
                log("RFID not found: " + str(id))
                GPIO.output(pin_rfid, GPIO.LOW)

                cfgObj["rfid"][str(id)] = {'album' : '', 'random' : False}
                with open("/var/www/html/rfid.json", 'w') as cfg_file:
                    json.dump(cfgObj, cfg_file)

except KeyboardInterrupt:
    pass

finally:
    log("**** Clean up and exit ****")
    GPIO.output(pin_wifi, GPIO.HIGH)
    GPIO.output(pin_rfid, GPIO.LOW)

    GPIO.cleanup()
