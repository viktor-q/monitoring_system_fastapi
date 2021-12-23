import os
import socket
from threading import Thread
import getmac
import json

with open("modules/pinger/vendors.json", "r") as j:
    vend_base = json.load(j)


def net_scanner():
    ip_online = []
    ip_and_name = {}

    def all_ip_in_net(ip):
        ipaddr = "192.168.1." + str(ip)
        #        ipaddr = "37.145.189." + str(ip)
        response = os.system("ping -c 1 " + ipaddr)
        if response == 0:
            ip_online.append(ipaddr)
            ip_mac = getmac.get_mac_address(ip=ipaddr)  # gething mac addr # getmac.PORT = 80

            if ip_mac is not None:
                mac_id = ip_mac.replace(":", "")[0:6]
                name_vendor = vend_base.get(mac_id)
            if ip_mac is None:
                name_vendor = None

            try:
                net_name = socket.gethostbyaddr(ipaddr)
                ip_and_name[ipaddr] = [net_name[0], ip_mac, name_vendor]
            except socket.herror:
                ip_and_name[ipaddr] = ["untitled", ip_mac, name_vendor]

    tasks = []
    for i in range(256):
        th = Thread(target=all_ip_in_net, args=(i,))
        tasks.append(th)

    for task in tasks:
        task.start()

    for task in tasks:
        task.join()

    return ip_and_name

# for row in net_scanner().items():
#    print(row)
# print(net_scanner())
