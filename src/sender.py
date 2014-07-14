#!/usr/bin/env python

import serial
import time
import re

def send(job=None,sname='/dev/ttyACM0'):
    # Open grbl serial port
    
    if job == None:
        return 'Invalid Job'
    
    try:
        s = serial.Serial(sname,9600)
    except Exception, e:
        return 'Serial Init Fail:\n{0}'.format(e)
	
    # Wake up grbl
    s.write("\r\n\r\n")
    time.sleep(2) # Wait for grbl to initialize
    s.flushInput() # Flush startup text in serial input

	#set units
    g = "G21" if job['unit'] == 'mm' else "G20"
    s.write(g + '\n')
    
    #regex the gcode
    job['gcode'] = str(job['gcode']).split('\n')
    
    r = 0
    while r < int(job['repeat']):
	    # Stream g-code to grbl
	    for line in job['gcode']:
	        l = line.strip() # Strip all EOL characters for consistency
	        print 'Sending: ' + l,
	        s.write(l + '\n') # Send g-code block to grbl
	        grbl_out = s.readline() # Wait for grbl response with carriage return
	        print ' : ' + grbl_out.strip()
	    print r
	    print r < job['repeat']
	    r+=1

    # Wait here until grbl is finished to close serial port and file.

    # Close serial port
    s.close()
    print 'here'
    return "G-Code Sent"
