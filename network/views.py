from select import select
from django.shortcuts import render
#from pythonwifi.iwlibs import Wireless, getNICnames
from network.pywifi import connect_known_profile, known_profiles, new_profile_connection, scan_networks

def wificonfig (request):
    selected_wifi_ssid =""
    alert=""
    wrong_pwd = False
    check = True
    #Scan available networks
    Iface_result = scan_networks()
    
    list_known_profiles = known_profiles()
    

    
    #check wifi pwd for selected Wifi
    if request.method == 'POST' and 'wifi_list' in request.POST:
        selected_wifi_ssid = request.POST['wifi_list']
        request.session['ssid'] = selected_wifi_ssid
        #check if the selected wifi is known by the interface
        for profile in list_known_profiles:
            if selected_wifi_ssid == profile.ssid:
                if connect_known_profile(profile):
                    check = False
                    alert = "You're connected! because the network is known"
                    break
                else:
                    #if the password was changed the password input will be load and the alert will be displayed
                    alert = "connexion failed, try another password"
                    break
        wrong_pwd = check    
            #else:
    #Create new profile for new network by passing password and ssid
            
    if request.method == 'POST' and 'network_password' in request.POST:
        #print("selected wifi", request.session.get('ssid'))
        wrong_pwd = True
        new_pwd = request.POST['network_password']
        #print('new password: ', type(new_pwd))
        if new_profile_connection(new_pwd,request.session.get('ssid')):
            alert = "You're connected! after entering pwd"
            wrong_pwd = False

    context = {
        'ssid':selected_wifi_ssid,
        'results':Iface_result,
        'alert': alert,
        'wrong_pwd': wrong_pwd,
    }
    return render(request, 'config.html', context)
