How to Configure WiFi on BBB
============================

A very nice video tutorial is available at [Element14's website](https://www.element14.com/community/videos/23901/l/beaglebone-black-wireless-wi-fi-setup).

A command-line tool called 'connmanctl' can be used to configure the wifi interface. To check the status of each interface:

 $ connmanctl technologies


You can set up the wifi interface from the connmanctl's console:

 $ sudo connmanctl
 connmanctl > tether wifi disable
 connmanctl > enable wifi
 connmanctl > scan wifi
 connmanctl > services
 
 *AO FiOS-ORHGK           wifi_506583dd5c56_46694f532d4f5248474b_managed_psk
   ...
   < list of wifis>
   …
 
 connmanctl > agent on
 connmanctl > connect wifi_506583dd5c56_46694f532d4f5248474b_managed_psk

If the specified wifi host require authentication, the screen will propmpt to enter your password.
If you need to manually configure the wifi interface (e.g. IP, name server, etc), use a 'config' command:

 connmanctl > config wifi_506583dd5c56_46694f532d4f5248474b_managed_psk --ipv4 dhcp --nameserver 8.8.8.8

