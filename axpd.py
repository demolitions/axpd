#!/bin/python
import os
import smbus
import time

def readFromBus(busn, addr, bytenum):
    bus = smbus.SMBus(busn)
    return bus.read_byte_data(addr, bytenum)

def writeToDevice(devname, data):
    dev = os.open('/sys/module/test_power/parameters/'+devname, os.O_RDWR)
    written = os.write(dev, data.encode('utf-8'))
    os.close(dev)
    return written

busnumber = -1
for busn in range(0,13):
    rep = readFromBus(busn, 0x34, 0x00)
    if rep > -1 :
        busnumber = busn
        break

while busnumber > -1 :
    # Charger status
    chargerconn = readFromBus(busnumber, 0x34, 0x00)
    # chargerconn = 250 when connected to USB, 0 when disconnected
    if chargerconn > 0 :
        writeToDevice('usb_online','on')
        charging = readFromBus(busnumber, 0x34, 0x01)
        # charging = 112 when charging, 48 when connected but not charging
        if charging > 48 :
            writeToDevice('battery_status','charging')
        else :
            writeToDevice('battery_status','not-charging')
    else :
        writeToDevice('usb_online','off')
        writeToDevice('battery_status','discharging')
    
    # Battery charge capacity
    #chargeqty = readFromBus(busnumber, 0x34, 0xb9)
    #print(chargeqty)

    time.sleep(1)
        
    
