import network
import urequests
import json
import time
from machine import Pin
from secrets import secrets
import machine
import neopixel

print("starting connection")
wlan = network.WLAN(network.STA_IF)

wlan.active(True)


print("connecting ...")
wlan.connect(secrets['ssid'], secrets['pw'])

# Wait for connect or fail
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('wifi connection failed')
else:
    print('connected')
    
status = wlan.ifconfig()
print( 'ip = ' + status[0] )

pixels = neopixel.NeoPixel(machine.Pin(22), 60)

def get_colour():
    url = "http://api.thingspeak.com/channels/1417/field/2/last.json"
    try:
        r = urequests.get(url)
        print(r.status_code)
        if r.status_code > 199 and r.status_code < 300:
            cheerlights = json.loads(r.content.decode('utf-8'))
            print(cheerlights['field2'])
            red_str = '0x' + cheerlights['field2'][1:3]
            green_str = '0x' + cheerlights['field2'][3:5]
            blue_str = '0x' + cheerlights['field2'][5:7]
            colour = (int(red_str), int(green_str), int(blue_str))
            
            r.close()
            return colour
        else:
            return None
    except Exception as e:
        print(e)
        return None
    return colour

while True:
    print("getting colour")
    colour = get_colour()
    if colour is not None:
        pixels.fill(colour)
        pixels.write()
    time.sleep(5)
