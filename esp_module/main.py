# from utime import sleep
# from utime import sleep_ms
# import os 
# import sys
import network
import urequests as requests


ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'


checksum=''
import program
try:
    from program import checksum as chksum
    checksum=chksum
except:
    checksum='ieury38'

# TODO: didn't work with http on LAN. some workarounds are needed
upd_url="http://192.168.1.105:5000/update?checksum="+str(checksum)
upd_url="https://88ff-103-166-58-98.ngrok.io/update?checksum="+str(checksum)
updt_ = False
    

def check_for_updates(upd_url):
    try:
        # print(upd_url)
        # print ('Checking for updates')
        response = requests.get(upd_url)
        if response.status_code==200:
            # print('There is an update available')
            return True
        else:
            # print('No update available')
            return False
    except:
        # print('Unable to reach the internet')
        return False


def update_program(upd_url):
    try:
        # print ('Downloading update')
        response = requests.get(upd_url)
        if response.status_code==200:
            txt=response.text
            # print('Verifying update')
            response2=requests.get(upd_url)
            if response2.status_code==200:
                if txt==response2.text:
                    # print('Update is valid')
                    # print('Starting update')

                    f = open("program.py","w")
                    f.write(txt)
                    f.flush()
                    f.close()

                    # print('Update complete')
                    
        else:
            # print('Update failed')
            return False
    except:
        # print('Unable to reach the internet')
        return False


conn = network.WLAN(network.STA_IF)
conn.active()
conn.active(True)
# conn.config(reconnects = 5)
conn.connect(ssid,password)

while not conn.isconnected():
  pass

## print board local IP address
# print(conn.ifconfig())


updt_ = check_for_updates(upd_url)

while updt_ == False:
    program.main()
    updt_ = check_for_updates(upd_url)

    


try:
    update_program(upd_url)
    # print('Rebooting')
    import machine
    machine.reset()
except:
    import machine
    machine.reset()

