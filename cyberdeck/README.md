# Luma Workshop

http://luma.link/lKMKnueRLJ

## Commands

```bash
minicom -o -D /dev/cu.usbmodem101
# or
screen /dev/cu.usbmodem101 115200

export PICO_SDK_PATH=/home/pi/pico/pico-sdk


rshell -p /dev/ttyACM0 --buffer-size 512 cp blink.py /pyboard/main.py

rshell --buffer-size=512 -p /dev/cu.usbmodem101 


rshell -p /dev/cu.usbmodem101 --buffer-size 512 cp scripts/blink.py /pyboard/main.py


%Run -c $EDITOR_CONTENT
```

where the rpi "machine" lives
```pip install micropython-stm32-stubs``` 



## Link
- [website](https://cyberdeck-course.lovable.app)

