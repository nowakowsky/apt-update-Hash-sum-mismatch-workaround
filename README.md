# Do not use this in production environment! 
## This is workaround for broken apt update (Hash sum mismatch)
This bug happens on debian-based systems like Kali linux, Ubuntu etc on Oracle VM.

You should use it only if - for some reason - you don't want to use "bcdedit /set hypervisorlaunchtype off".
This script runs apt-update and changes expected hashes with recived so you can use apt.

Python3.6+
