

### CF350BT

Easy@Home bluetooth s

### android reverse

#### setup adb

* install package
```
sudo pacman -S android-tools
```

* start server
```
adb start-server
```

* plug android device

* confirm phone access prompt

##### enable developer options

* settings -> about -> build number -> tap 5 times

##### obtain session capture

* discover log location
```
adb shell "cat /etc/bluetooth/bt_stack.conf | grep FileName"
```

* start with btsnoop_hci.log disabled
```
adb shell settings put secure bluetooth_hci_log 0
```

* truncate existing btsnoop_hci.log
```
adb shell rm -f /sdcard/btsnoop_hci.log
adb shell touch /sdcard/btsnoop_hci.log
```

* open/start log:
```
adb shell settings put secure bluetooth_hci_log 1
```

* stand on the scale, produce normal measurement session

* close/flush log:
```
adb shell settings put secure bluetooth_hci_log 0
```

* download generated btsnoop_hci.log
```
adb pull /sdcard/btsnoop_hci.log
```

#### wireshark

* apply `*.pcap` extension to `btsnoop_hci.log`

* apply packet filter by mac address
```
bluetooth.addr==88:1B:99:05:5B:59
```

* apply packet filter by bt protocol
```
bluetooth.addr==88:1B:99:05:5B:59 and btspp
```
