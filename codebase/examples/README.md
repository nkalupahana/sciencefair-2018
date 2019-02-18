# Science Fair 2018 Codebase Examples

To use one of the files in the examples folder, just run it, making sure that the API path is set correctly in code!

### Enabling GPS socket on RPi

```
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/serial0 -F /var/run/gpsd.sock
```
