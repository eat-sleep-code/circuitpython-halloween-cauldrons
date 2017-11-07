from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
import board
import busio
import time


# On-board red LED and Dotstar
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT
dotstar = busio.SPI(board.APA102_SCK, board.APA102_MOSI)

# Input from proximity sensor and voltage threshold where something is considered in-range
proximitySensor = AnalogIn(board.D0)
proximityThresholdVoltage = 1.5    # Adjust as needed.

# Output to AudioFX board
audioFX = DigitalInOut(board.D2)
audioFX.direction = Direction.OUTPUT


# Some useful functions...
def getVoltage(pin):
        return (pin.value * 3.3) / 65536

def setPixel(red, green, blue):
    if not dotstar.try_lock():
        return
    print("Setting dotstar to: %d %d %d" % (red, green, blue))
 
    data = bytearray([0x00, 0x00, 0x00, 0x00,
                      0xff, blue, green, red,
                      0xff, 0xff, 0xff, 0xff])
    dotstar.write(data)
    dotstar.unlock()
    time.sleep(0.01)


#Let's go scare people...
audioFX.value = True
time.sleep(0.1)

while True:
    proximitySensorVoltage = getVoltage(proximitySensor)
    print("D1: %0.2f" % (proximitySensorVoltage))
    if proximitySensorVoltage >= proximityThresholdVoltage:
        audioFX.value = False
        setPixel(255, 165, 0)
        print("Someone is raiding the candy bowl...")
    else: 
        audioFX.value = True  
        setPixel(148, 0, 211)
        print("What? Nobody wants free candy?")   
    time.sleep(0.1)
