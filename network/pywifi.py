import pywifi
import time

wifi = pywifi.PyWiFi() #create Wifi Object
iface = wifi.interfaces()[0] #Intialize Interface
Name = iface.name()

#Scan the interface to display all networks around it
def scan_networks():
    iface.scan()
    time.sleep(6)
    return iface.scan_results()

#return list of profile object of all know networks
def known_profiles():
    return iface.network_profiles()

#create a profile for know network and connect to it using the interface
def connect_known_profile(profile):
    connect =pywifi.Profile()
    connect.ssid = profile.ssid
    connect.auth = pywifi.const.AUTH_ALG_OPEN
    connect.akm.append(pywifi.const.AKM_TYPE_NONE)
    return iface_connect(connect)

#connect the interface to a profile
def iface_connect(profile):
    status = False #set variable to false to check interface status
    known = False
    iface.disconnect()
    time.sleep(1)
    assert iface.status() in [pywifi.const.IFACE_DISCONNECTED, pywifi.const.IFACE_INACTIVE]
    print('iface disconnected')
    #iface.remove_all_network_profiles()
    profiles = known_profiles()
    for pf in profiles:
        if pf.ssid == profile.ssid:
            iface.connect(pf)
            known = True
    if not known:
        temp_profile = iface.add_network_profile(profile)
        time.sleep(5)
        profiles = known_profiles()
        for pf in profiles:
            if pf.ssid == profile.ssid:
                print('new profile added')
        iface.connect(temp_profile)
    time.sleep(5)
    assert iface.status() in [pywifi.const.IFACE_CONNECTED, pywifi.const.IFACE_CONNECTING], 'status is wrong'
    print('network on')
    status = True
    return status

#Connect to a new profile
def new_profile_connection(pwd, ssid):
    connect = pywifi.Profile()
    connect.ssid = ssid
    connect.auth = pywifi.const.AUTH_ALG_OPEN
    connect.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    connect.cipher = pywifi.const.CIPHER_TYPE_CCMP
    connect.key = pwd
    assert pywifi.const.AKM_TYPE_WPA2PSK in connect.akm
    assert pywifi.const.AUTH_ALG_OPEN in connect.auth
    print('ssid',connect.ssid)
    print('key',connect.key)
    return iface_connect(connect)
