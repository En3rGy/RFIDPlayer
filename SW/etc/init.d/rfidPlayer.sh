#! /bin/bash

### BEGIN INIT INFO
# Provides:          rfidPlayer
# Required-Start:    $local_fs $network
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Sonos RFID Remote
# Description:       Sonos play albums based on rfid tag
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting rfidPlayer..."
    sudo python /home/pi//MFRC522-python/Read.py &
    #sudo -u pi bash -c 'cd /home/pi/MFRC522-python && ./rfidplayer.sh' &
    ;;
  stop)
    echo "Stopping Foo..."
    sleep 2
    ;;
  *)
    echo "Usage: /etc/init.d/rfidPlayer {start|stop}"
    exit 1
    ;;
esac

exit 0
