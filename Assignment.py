from microbit import *
import math
##Define midiCC
def midiControlChange(chan, n, value):
    MIDI_CC = 0xB0
    if chan > 15:
        return
    if n > 127:
        return
    if value > 127:
        return
    msg = bytes([MIDI_CC | chan, n, value])
    uart.write(msg)

def Start():
    uart.init(baudrate=31250, bits=8, parity=None, stop=1, tx=pin0)

Start()
last_tilt_x = 0
last_tilt_z = 0
last_pot_1 = 0
last_pot_2 = 0
while True:
    ##Right potensiometer used for the pointer's velocity in the map
    pot_1 = pin1.read_analog()
    if last_pot_1 != pot_1:
        velocity = math.floor(pot_1 / 1024 * 127)
        ##Send velocity to MIDI_CC = 24
        midiControlChange(0, 24, velocity)
    last_pot_1 = pot_1
    ##Left potensiometer used for the sound amplitude
    pot_2 = pin2.read_analog()
    if last_pot_2 != pot_2:
        amplitude = math.floor(pot_2 / 1024 * 127)
        ##Send amplitude to MIDI_CC = 25
        midiControlChange(0, 25, amplitude)
    last_pot_2 = pot_2

    ##Get X and Z accelerations used for the pointer's direction
    current_tilt_x = accelerometer.get_x()
    current_tilt_z = accelerometer.get_z()

    #Define the max values as 512 (min as -512)
    if current_tilt_x > 512:
        current_tilt_x = 512
    elif current_tilt_x < -512:
        current_tilt_x = -512

    if current_tilt_z > 512:
        current_tilt_z = 512
    elif current_tilt_z < -512:
        current_tilt_z = -512

    #convert tilts into MIDI numbers (0-127)
    if current_tilt_x != last_tilt_x or current_tilt_z != last_tilt_z:
        mod_x = math.floor(math.fabs((current_tilt_x + 512)/1024*127))
        mod_z = math.floor(math.fabs((current_tilt_z + 512)/1024*127))
        ##Send mod_x to MIDI_CC = 22
        ##Send mod_z to MIDI_CC = 23
        midiControlChange(0, 22, mod_x)
        midiControlChange(0, 23, mod_z)
        last_tilt_x = current_tilt_x
        last_tilt_z = current_tilt_z
    ##Take values every 50 ms
    sleep(50)