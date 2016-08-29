#!/usr/bin/python
# encoding: utf-8
'''
boblightwifi -- shortdesc
boblightwifi connects the flux_led wifi controller to boblightd
@author:     Christian Fenzl

@copyright:  2016 Christian Fenzl, based on boblighthue from Christian Völlinger. All rights reserved.

@license:    GNU GENERAL PUBLIC LICENSE v3
@contact:    christiantf@gmx.at
@deffield    updated: Updated
'''

import os
import sys
import atexit
import time
import socket
from socket import AF_INET, SOCK_DGRAM
from select import select

from colormath.color_objects import sRGBColor, xyYColor
from colormath.color_conversions import convert_color

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


# pip install colormath

__all__ = []
__version__ = 0.1
__date__ = '2016-08-23'
__updated__ = '2016-08-23'

class boblightwifi(object):
    def __init__(self, ip, port, timeout, sock=None):
        self._ip = ip
        self._port = port
        self._timeout = timeout
        self._scaled = 0
        if sock is None:
            print time.strftime("%H:%M:%S") + " Create new socket"
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def connect(self):
        print time.strftime("%H:%M:%S") + " Connect"
        self.sock.settimeout(self._timeout)
        self.sock.connect((self._ip, self._port))
        # self.switch_on()
        self.sock.settimeout(0.2)
		
    def popen(self):
        # switch off at script exit
        def cleanup():
            print time.strftime("%H:%M:%S") + " Switchoff"
            # self.switch_off()

        print time.strftime("%H:%M:%S") + " atexit.register(cleanup)"
        atexit.register(cleanup)

        while True:
            rlist, _, _ = select([sys.stdin], [], [], self._timeout)
            if rlist:
                input = sys.stdin.readline()
                self.set_color(input)
            else:
                print time.strftime("%H:%M:%S") + " timeout, no data..."
                self.switch_off()

    def switch_off(self):
        
		msg = bytearray([0x71, 0x24, 0x0f])
		self.__write(msg)

    def switch_on(self):
        
		msg = bytearray([0x71, 0x23, 0x0f])
		self.__write(msg)

    def set_color(self, rgb):
		# print "Set_Color", rgb
		if len(rgb) > 0:

			rgb = rgb.split(' ')

			r = rgb[0]
			g = rgb[1]
			b = rgb[2]
		
			# print time.strftime("%H:%M:%S") + "Colors: R" + r + " G" + g + " B"+ b

			msg = bytearray([0x31])
			msg.append(int(255*float(r)))
			msg.append(int(255*float(g)))
			msg.append(int(255*float(b)))
			msg.append(0x00)
			msg.append(0xf0)
			msg.append(0x0f)
			self.__write(msg)
			
    def __writeRaw(self, bytes):
        if self.sock.sendall(bytes) <> None:
            print time.strftime("%H:%M:%S") + " -->Sendall failed" 
            
    def __write(self, bytes):
		# calculate checksum of byte array and add to end
		csum = sum(bytes) & 0xFF
		bytes.append(csum)
		#print "-------------",utils.dump_bytes(bytes)
		self.__writeRaw(bytes)
		# time.sleep(.01)		
		 
def main(argv=None):
    '''Command line options.'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s
    Forked by christiantf on %s
	Main code based on boblighthue by chriszero.
	Wifi byte protocol digged from flux_led code.
    Copyright 2016 All rights reserved.

    Licensed under the GNU GENERAL PUBLIC LICENSE v3
    https://www.gnu.org/licenses/gpl-3.0.de.html

    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.
    USAGE
    ''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-H", "--host", type=str,  required=True, help="Host (ip) of the FLUX LED Controller")
    parser.add_argument("-P", "--port", type=int,  default=5577, help="Port of the FLUX LED Controller (default 5577)")
    parser.add_argument("-t", "--timeout", type=int, default=30, help='If no data is received for "Timeout", light is switched off')
    parser.add_argument("--testcolor", help='Test color, you have to quote "R G B"')
    parser.add_argument("--off", action='store_true', help='Switch off')
    parser.add_argument("--on", action='store_true', help='Switch on')
    parser.add_argument('--version', action='version', version=program_version_message)
    parser.add_argument("-v", "--verbose", action='store_true', help='Verbose output of colors')

    # Process arguments
    args = parser.parse_args()

    while True:
        try:
            con = boblightwifi(args.host, args.port, args.timeout)
            con.connect()
            
            
            if args.verbose:
                verbose = True

            if args.off:
                con.switch_off()
                return 0
        
            if args.on:
                con.switch_on()
                return 0
            
            if args.testcolor:
                con.set_color(args.testcolor)
            else:
                con.popen()
        except socket.timeout:
           print time.strftime("%H:%M:%S") + " --> Timeout Exception"
           continue
        except Exception as e:
            print time.strftime("%H:%M:%S") + " --> Other Exception"
            print e
            return 2


if __name__ == "__main__":
    sys.exit(main())
