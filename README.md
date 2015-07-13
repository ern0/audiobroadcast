# audiobroadcast
Simple web app for playing netradio streams on a Raspberry PI (or any Linux systems)

### Project Scope ###

**Problem:** 
- There is a radio set in the kitchen
- I want to listen net radios (like D.I.)
- I can connect my Android device to the radio set (it has AV in), but the router is too far, drops WiFi every 2 minutes

**Solution:**
- I have a Rasbperry PI
- I've installed MPD (Music Player Daemon)
- I've bought a cheap Chinese FM transmitter - <img src="http://s896.photobucket.com/user/Blarneyjon/media/Blarney-jon%203/Jwin_JACK702W_FM_Transmitter.jpg.html" width="200" />
- I've written this script to access my favourite stations from mobile

### Instructions ###

Install MPD
```
sudo apt-get install mpd mpc
```

Download and copy files to a folder, e.g. `/opt/audiobroadcast`. Edit `playlist.txt`, one item per line, fields are separated with caret ('^'):
```
My Fav Radio^http://example.com/icon.png^http://example.com/stream.m3u
Another One^http://example.com/icon.jpg^http://example.com:9900/stream2.m3u
```

Launch Python app:
```
cd /opt/audiobroadcast
./radio.py
```

Point your browser to `http://raspi:8888/` where "raspi" is your Raspberry PI's hostname or IP address. Connect your transmitter or amp to Raspberry PI. Push up the volume!
