# boblightwifi

0.1 ALPHA

boblightwifi is the integration of the ARILUX AL-LC01 / AL-LC2 RGB(W) Wifi LED Controller to boblight.
Other Wifi RGB Controller may also work.

This is a mixed fork of beville's flux_lex (https://github.com/beville/flux_led) - a python command line tool 
to control the Wifi RGB controller, and chriszero's newbobhue (https://gist.github.com/chriszero/8b354c5165b634966dc7), a boblight 
integration for Philips Hue.

The script is in ALPHA state. I'm usually not a python programmer! There is lot of debug code in it.

## boblight.conf
See the example boblight.conf. This file is usually placed in /etc/, but may be somewhere else in your installation.
Edit the path to the boblightwifi.py, and hostname/IP in the -H parameter.

To test/debug with boblightd, it is a good idea to stop the boblightd process and call it manually. Then you will see 
the output of the boblightwifi.py script.

## Known Issues
In my setup, I have stream timeouts every 5 to 10 minutes, sometimes more or less. In this case, the script closes the socket and reconnects. 
For some reason, in such a timeout situation the controller turns off LED for a fraction of a second, so it flickers, and after reconnect will continue. 
I don't know if this is an issue of my script, of the RGB controller or my wifi, but if someone has an idea, give me advice.

## More than one controller
I currently have tested with one RGB controller. Therefore, boblight.conf captures the full screen color to send it to one device.
For more than one devices, add that devices to boblight.conf with the same path but other host. For configuration of the zones please read boblight 
configuration wiki and google the web.

## DoTo
As the connection possibly drops because of RGB controller or Wifi overload, I try to limit the update speed to the controller.
My tries with the interval and rate options in boblight.conf did not show any difference. Possibly I can ignore some values that boblightd sends to the script.
 
