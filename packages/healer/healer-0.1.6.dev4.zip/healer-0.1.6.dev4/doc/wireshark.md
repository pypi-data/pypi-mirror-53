

### generic

https://wiki.wireshark.org/CaptureSetup/USB

sudo adduser $USER wireshark

modprobe usbmon

lsmod | grep usbmon

sudo setfacl -m u:$USER:r /dev/usbmon*

### archux

https://wiki.archlinux.org/index.php/Wireshark

sudo pacman -S wireshark-cli

