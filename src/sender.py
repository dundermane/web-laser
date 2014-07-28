#!/usr/bin/env python

import serial
import re
import time
import sys
import argparse
# import threading

RX_BUFFER_SIZE = 128


def send(job=None,sname='/dev/ttyACM0'):

    if job == None:
        return 'Invalid Job'
    
    try:
        s = serial.Serial(sname,9600)
    except Exception, e:
        return 'Serial Init Fail:\n{0}'.format(e)

    # Wake up grbl
    print "Initializing grbl..."
    s.write("\r\n\r\n")

    # Wait for grbl to initialize and flush startup text in serial input
    time.sleep(.3)
    s.flushInput()

    #set units
    g = "G21" if job['unit'] == 'mm' else "G20"
    s.write(g + '\n')
    
    #set defaults
    s.write('\n')

    #regex the gcode
    job['gcode'] = str(job['gcode']).split('\n')
    print job['gcode']

    # Stream g-code to grbl
    r = 0
    while r < int(job['repeat']):
        print "Streaming gcode to "+sname
        l_count = 0
        g_count = 0
        c_line = []
        # periodic() # Start status report periodic timer
        for line in job['gcode']:
            l_count += 1 # Iterate line counter
        #     l_block = re.sub('\s|\(.*?\)','',line).upper() # Strip comments/spaces/new line and capitalize
            l_block = line.strip()
            c_line.append(len(l_block)+1) # Track number of characters in grbl serial read buffer
            grbl_out = '' 
            
            while sum(c_line) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
                out_temp = s.readline().strip() # Wait for grbl response
                if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
                    print "  Debug: ",out_temp # Debug response
                else :
                    grbl_out += out_temp;
                    g_count += 1 # Iterate g-code counter
                    grbl_out += str(g_count); # Add line finished indicator
                    del c_line[0]
            print "SND: " + str(l_count) + " : " + l_block,
            s.write(l_block + '\n') # Send block to grbl
            print "BUF:",str(sum(c_line)),"REC:",grbl_out
        r+=1;

    # Wait for user input after streaming is completed
    print 'G-code streaming finished!'
    # Close file and serial port
    time.sleep(2)
    s.close()
    return 'Streaming Complete'
