# erasme radio

Based on:
- https://aiyprojects.withgoogle.com/voice/
- https://www.pygame.org/docs/
- https://github.com/MAKIO135/sensorShieldLib


Download and burn Raspberry Pi image from https://aiyprojects.withgoogle.com/voice/  
Then copy aiy Python package from `/home/pi/AIY-projects-python/src` to `/usr/lib/python2.7/dist-packages`

Clone repo in `/home/pi` 


###  Start script on boot
- Edit `/etc/rc.local` file:
```
sudo nano /etc/rc.local
```
- Add the following line before `exit 0`:
```
su pi -c 'cd /home/pi/radio && python main.py < /dev/null &'
```
